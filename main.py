import argparse
import os
from utils import esx, proxmox, processor, bookstack
import configparser 


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("system", help="System name from config file")
    parser.add_argument("file", help="Config file location")
    parser.add_argument("--output", help="Save to file instad of BookStack")

    return parser.parse_args()

def read_credentials(config, system):
    creds = {}
    creds["platform"] = config.get(system, "platform")
    creds["user"]= config.get(system, "user")
    creds["pwd"] = config.get(system, "pwd")
    creds["host"] = config.get(system, "host")
    creds["ssl"] = config.getboolean(system, "ssl")
    creds["port"] = config.get(system, "port")

    return creds

def get_bookstack_creds(config):
    creds = {}
    creds["id"] = config.get("bookstack", "token_id")
    creds["secret"] = config.get("bookstack", "token_secret")
    creds["host"] = config.get("bookstack", "host")
    creds["port"] = config.get("bookstack", "port")
    creds["ssl"] = config.getboolean("bookstack", "ssl")
    creds["book"] = config.get("bookstack", "book_name")
    creds["page"] = config.get("bookstack", "page_name")

    return creds

def process_system(system, creds, file_name, ticket, bookstack_creds):
    print(f"[STARTING] Started processing {system}")
    if creds["platform"] == "esx":
        notes = esx.get_notes(creds)

    elif creds["platform"] == "proxmox":   
        notes = proxmox.get_notes(creds, ticket)

    else:
        raise SystemExit(f"[ERROR] Platform {creds['platform']} is not supported!")

    markdown = processor.process_notes(system, notes)

    if not file_name:
        bookstack.upload(system, bookstack_creds, markdown)
    else:
        print(f"[SAVING] Saving data to {file_name}")
        if os.path.isfile(file_name):
            file = open(file_name, "r+")
        else:
            file = open(file_name, "w+")

        previous = file.read()
        updated = processor.insert_system(system, previous, markdown)
        file.seek(0)
        file.write(updated)
        file.truncate()
        file.close()
        print(f"[SAVING] Saving completed")

    print(f"[FINISHED] Finished processing {system}")

def main():
    args = get_args()

    config = configparser.RawConfigParser()
    config.read(args.file)

    bookstack_creds = get_bookstack_creds(config)

    system = args.system
    if system == "bookstack":
        raise SystemExit("[ERROR] This name is reserved for BookStack...")

    if (config.get(system, "type") == "cluster"):
        for node in config.get(system, "nodes").split(","):
            node = node.strip()

            if node in config:
                creds = read_credentials(config, node)
                ticket = proxmox.auth(creds)

                if ticket:
                    print(f"[FOUND] {node} is active, getting data...")
                    process_system(system, creds, args.output, ticket, bookstack_creds)
                    break
                else:
                    print(f"[ERROR] {node} is not active, trying next one...")
            else:
                print(f"[ERROR] {node} has no entry in the config file...")
        else:
            print(f"[ERROR] No node from the list is active")

    elif system in config:
        # To morm zlo spremenit ko dobim dostop do vCentra
        creds = read_credentials(config, system)
        
        if creds["platform"] == "proxmox":
            ticket = proxmox.auth(creds)
        elif creds["platform"] == "esx":
            ticket = None

        process_system(system, creds, args.output, ticket, bookstack_creds)
    else:
        raise SystemExit("[ERROR] There is no config entry for this system...")

if __name__ == "__main__":
    main()