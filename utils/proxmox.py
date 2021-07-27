from utils.processor import VirtualMachine
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

def add_disk_type(discs, type, number, data):
    for i in range(number):
            if f"{type}{i}" in data:
                try:
                    storage = data[f"{type}{i}"].split(":")[0]
                    size = int(data[f"{type}{i}"].split("size=")[1][:-1])

                    if storage in discs:
                        discs[storage] += size
                    else:
                        discs[storage] = size
                except:
                    pass
    
    return discs

def get_discs(vm_data, type):
    discs = {}
    if type == "qemu":
        discs = add_disk_type(discs, "sata", 6, vm_data)
        discs = add_disk_type(discs, "scsi", 31, vm_data)
        discs = add_disk_type(discs, "virtio", 16, vm_data)
        discs = add_disk_type(discs, "ide", 4, vm_data)

    if type == "lxc":
        storage = vm_data["rootfs"].split(":")[0]
        size = int(vm_data["rootfs"].split("size=")[1][:-1])
        discs[storage] = size

        discs = add_disk_type(discs, "mp", 256, vm_data)

    return discs

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
        if vm["type"] == "qemu":
            url = f"{base_url}/nodes/{vm['node']}/qemu/{vm['vmid']}/config"
        elif vm["type"] == "lxc":
            url = f"{base_url}/nodes/{vm['node']}/lxc/{vm['vmid']}/config"

        res = requests.get(url, cookies=cookie, verify=args["ssl"])
        vm_data = res.json()
        if (vm_data["data"]):
            vm_data = vm_data["data"]
            ime = vm_data["name"] if "name" in vm_data else vm_data["hostname"]
            note = vm_data["description"] if "description" in vm_data else None
            memory = vm_data["memory"] if "memory" in vm_data else None

            ip = "IP naslovov LXC containerjev še nisem uspel dobiti"
            disks = "Work in progress"

            if vm["type"] == "qemu":
                url = f"{base_url}/nodes/{vm['node']}/qemu/{vm['vmid']}/agent/network-get-interfaces"
                res = requests.get(url, cookies=cookie, verify=args["ssl"])
                try:
                    ip = res.json()["data"]["result"][1]["ip-addresses"][0]["ip-address"]
                except:
                    ip = "VM nima qemu-guest-agenta oziroma ni prižgana"

            discs = get_discs(vm_data, vm["type"])

            notes.append(VirtualMachine(ime, note, memory, ip, discs))
            
    print("[READING] Successfully read all notes")
    
    return notes
