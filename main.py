import argparse
from getpass import getpass
from utils import esx, proxmox, processor


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=["esx", "proxmox"])
    parser.add_argument("--host", type=str, required=True)
    parser.add_argument("--user", type=str, required=True)
    parser.add_argument("--pwd", type=str, required=False)
    parser.add_argument("--port", type=str, required=False)
    parser.add_argument("--nossl", required=False, action="store_true")

    return parser.parse_args()


args = get_args()
platform = args.platform
args.ssl = not args.nossl

if not args.pwd:
    args.pwd = getpass()

if platform == "esx":
    if not args.port:
        args.port = 443

    notes = esx.get_notes(args)

elif platform == "proxmox":
    if not args.port:
        args.port = 8006
    
    notes = proxmox.get_notes(args)

processor.process_notes(platform, notes)
