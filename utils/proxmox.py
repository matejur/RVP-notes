import requests

base_url = None

def auth(args):

    if args.nossl:
        requests.packages.urllib3.disable_warnings()

    global base_url
    base_url = f"https://{args.host}:{args.port}/api2/json"
    url = f"{base_url}/access/ticket"
    payload = f"username={args.user}&password={args.pwd}"

    res = requests.post(url, data=payload, verify=args.ssl)
    data = res.json()

    if not data["data"]:
        raise SystemExit("Povezava z danimi podatki ni uspela!")

    ticket = data["data"]["ticket"]

    return ticket

def get_notes(args):
    ticket = auth(args)
    cookie = {"PVEAuthCookie": ticket}
    url = f"{base_url}/cluster/resources"

    res = requests.get(url, cookies=cookie, params={"type": "vm"}, verify=args.ssl)
    data = res.json()

    notes = []
    
    for vm in data["data"]:
        url = f"{base_url}/nodes/{vm['node']}/qemu/{vm['vmid']}/config"

        res = requests.get(url, cookies=cookie, verify=args.ssl)
        data = res.json()
        
        if (data["data"]):
            note = (data["data"]["name"], data["data"]["description"])
            notes.append(note)
    
    return notes
    