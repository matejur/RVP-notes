import requests
import sys

base_url = None

def auth(args):

    print("[CONNECTING] Trying to connect to the Proxmox server...")
    if not args["ssl"]:
        requests.packages.urllib3.disable_warnings()

    global base_url
    base_url = f"https://{args['host']}:{args['port']}/api2/json"
    url = f"{base_url}/access/ticket"
    payload = {
        "username": args['user'],
        "password": args['pwd']
    }

    res = requests.post(url, json=payload, verify=args["ssl"])
    data = res.json()

    if not data["data"]:
        raise SystemExit("[ERROR] Povezava z danimi podatki ni uspela!", file=sys.stderr)

    ticket = data["data"]["ticket"]
    print("[CONNECTED] Successfully connected!")
    return ticket

def get_notes(args):
    ticket = auth(args)
    cookie = {"PVEAuthCookie": ticket}
    url = f"{base_url}/cluster/resources"

    print("[RETRIEVING] Retrieving all Proxmox virtual machines")
    res = requests.get(url, cookies=cookie, params={"type": "vm"}, verify=args["ssl"])
    data = res.json()
    print(f"[RETRIEVING] Successfully retrieved {len(data['data'])} virtual machines")
    
    print("[READING] Reading notes from every VM")
    notes = []

    for vm in data["data"]:
        url = f"{base_url}/nodes/{vm['node']}/qemu/{vm['vmid']}/config"

        res = requests.get(url, cookies=cookie, verify=args["ssl"])
        vm_data = res.json()

        if (vm_data["data"]):
            note = (vm_data["data"]["name"], vm_data["data"]["description"] if "description" in vm_data["data"] else None)
            notes.append(note)
            
    print("[READING] Successfully read all notes")
    
    return notes
