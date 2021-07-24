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

def bookstack_creds(config):
    creds = {}
    creds["id"] = config.get("bookstack", "token_id")
    creds["secret"] = config.get("bookstack", "token_secret")
    creds["host"] = config.get("bookstack", "host")
    creds["port"] = config.get("bookstack", "port")
    creds["ssl"] = config.getboolean("bookstack", "ssl")
    creds["book"] = config.get("bookstack", "book_name")
    creds["page"] = config.get("bookstack", "page_name")

    return creds

def process_system(system, config, args):
    print(f"[STARTING] Started processing {system}")
    creds = read_credentials(config, system)
    if creds["platform"] == "esx":
        notes = esx.get_notes(creds)

    elif creds["platform"] == "proxmox":   
        notes = proxmox.get_notes(creds)

    else:
        raise SystemExit(f"[ERROR] Platform {creds['platform']} is not supported!")

    markdown = processor.process_notes(system, notes)

    if not args.output:
        creds = bookstack_creds(config)
        bookstack.upload(system, creds, markdown)
    else:
        print(f"[SAVING] Saving data to {args.output}")
        if os.path.isfile(args.output):
            file = open(args.output, "r+")
        else:
            file = open(args.output, "w+")

        previous = file.read()
        updated = processor.insert_system(system, previous, markdown)
        file.seek(0)
        file.write(updated)
        file.truncate()
        file.close()
        print(f"[SAVING] Saving completed")

    print(f"[FINISHED] Finished processing {system}")

args = get_args()

config = configparser.RawConfigParser()
config.read(args.file)

system = args.system
if system == "bookstack":
    raise SystemExit("[ERROR] This name is reserved for BookStack...")

if system == "all":
    for sys in config.sections():
        if sys != "bookstack":
            process_system(sys, config, args)

elif system in config:
    process_system(system, config, args)
else:
    raise SystemExit("[ERROR] There is no config entry for this system...")