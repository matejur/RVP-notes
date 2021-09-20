import argparse
import os
from utils import esx, proxmox, processor, bookstack
import configparser 


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("system_name", help="System name from config file")
    parser.add_argument("file", help="Config file location")
    parser.add_argument("--output", help="Save to file instad of BookStack")

    return parser.parse_args()

def read_credentials(config, system_name):
    creds = {}
    creds["platform"] = config.get(system_name, "platform")
    creds["user"]= config.get(system_name, "user")
    creds["pwd"] = config.get(system_name, "pwd")
    creds["host"] = config.get(system_name, "host")
    creds["ssl"] = config.getboolean(system_name, "ssl")
    creds["port"] = config.get(system_name, "port")

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

def save_data(system_name, markdown, bookstack_creds, file_name):
    if not file_name:
        bookstack.upload(system_name, bookstack_creds, markdown)
    else:
        print(f"[SAVING] Saving data to {file_name}")
        if os.path.isfile(file_name):
            file = open(file_name, "r+")
        else:
            file = open(file_name, "w+")

        previous = file.read()
        updated = processor.insert_system(system_name, previous, markdown)
        file.seek(0)
        file.write(updated)
        file.truncate()
        file.close()
        print(f"[SAVING] Saving completed")

    print(f"[FINISHED] Finished processing {system_name}")

def process_system(system_name, creds, file_name, bookstack_creds, ticket):
    if not ticket:
        raise SystemExit("[ERROR] Povezava z danimi podatki ni uspela!")

    print(f"[STARTING] Started processing {system_name}")
    if creds["platform"] == "esx":
        notes = esx.get_notes(ticket)

    elif creds["platform"] == "proxmox":   
        notes = proxmox.get_notes(creds, ticket)

    else:
        raise SystemExit(f"[ERROR] Platform {creds['platform']} is not supported!")

    markdown = processor.process_notes(system_name, notes)

    save_data(system_name, markdown, bookstack_creds, file_name)

def main():
    args = get_args()

    config = configparser.RawConfigParser()
    config.read(args.file)

    bookstack_creds = get_bookstack_creds(config)

    system_name = args.system_name
    if system_name == "bookstack":
        raise SystemExit("[ERROR] This name is reserved for BookStack...")

    if system_name in config:
        if config.get(system_name, "type") == "cluster":
            for node in config.get(system_name, "nodes").split(","):
                node = node.strip()

                if node in config:
                    creds = read_credentials(config, node)
                    ticket = proxmox.auth(creds)

                    if ticket:
                        print(f"[FOUND] {node} is active, getting data...")
                        process_system(system_name, creds, args.output, bookstack_creds, ticket)
                        break
                    else:
                        print(f"[ERROR] {node} is not active, trying next one...")
                else:
                    print(f"[ERROR] {node} has no entry in the config file...")
            else:
                print(f"[ERROR] No node from the list is active")

        elif config.get(system_name, "type") == "vcenter":
            creds = read_credentials(config, system_name)

            ticket = esx.connect(creds)

            if ticket:
                process_system(system_name, creds, args.output, bookstack_creds, ticket)
            else:
                print("[ERROR] VCenter is not online, trying individual systems")
                notes = []
                for node in config.get(system_name, "nodes").split(","):
                    node = node.strip()

                    if node in config:
                        creds = read_credentials(config, node)
                        ticket = esx.connect(creds)

                        if ticket:
                            print(f"[FOUND] {node} is active, getting data...")
                            notes += esx.get_notes(ticket)
                        else:
                            print(f"[ERROR] {node} is not active, trying next one...")
                    else:
                        print(f"[ERROR] {node} has no entry in the config file...")
                
                if not notes:
                    print(f"[ERROR] No node from the list is active")
                
                markdown = processor.process_notes(system_name, notes)
                save_data(system_name, markdown, bookstack_creds, args.output)

        else:
            creds = read_credentials(config, system_name)
            
            if creds["platform"] == "proxmox":
                ticket = proxmox.auth(creds)
                process_system(system_name, creds, args.output, bookstack_creds, ticket)
            elif creds["platform"] == "esx":
                ticket = esx.connect(creds)
                process_system(system_name, creds, args.output, bookstack_creds, ticket)
            
    else:
        raise SystemExit("[ERROR] There is no config entry for this system_name...")

if __name__ == "__main__":
    main()