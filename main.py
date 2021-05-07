import argparse
from utils import esx, proxmox, processor, bookstack
import configparser 


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=["esx", "proxmox"])
    parser.add_argument("--file")

    return parser.parse_args()

def read_credentials(platform, file):
    config = configparser.ConfigParser()
    config.read(file)

    creds = {}
    creds["user"]= config.get(platform, "user")
    creds["pwd"] = config.get(platform, "pwd")
    creds["host"] = config.get(platform, "host")
    creds["ssl"] = config.getboolean(platform, "ssl")
    creds["port"] = config.get(platform, "port")

    return creds

def bookstack_creds(file):
    config = configparser.ConfigParser()
    config.read(file)

    creds = {}
    creds["id"] = config.get("bookstack", "token_id")
    creds["secret"] = config.get("bookstack", "token_secret")
    creds["host"] = config.get("bookstack", "host")
    creds["port"] = config.get("bookstack", "port")
    creds["ssl"] = config.getboolean("bookstack", "ssl")
    creds["chapter"] = config.get("bookstack", "chapter_id")

    return creds


args = get_args()
platform = args.platform
creds = read_credentials(platform, args.file)

if platform == "esx":
    notes = esx.get_notes(creds)

elif platform == "proxmox":   
    notes = proxmox.get_notes(creds)

markdown = processor.process_notes(platform, notes)

creds = bookstack_creds(args.file)

bookstack.upload(platform, creds, markdown)