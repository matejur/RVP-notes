import atexit
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import sys
from .processor import VirtualMachine

def connect(args):
    instance = None

    print("[CONNECTING] Trying to connect to the ESX server...")
    try:
        if args["ssl"]:
            instance = SmartConnect(host=args["host"], user=args["user"], pwd=args["pwd"], port=args["port"])
        else:
            instance = SmartConnect(host=args["host"], user=args["user"], pwd=args["pwd"], port=args["port"], disableSslCertValidation=True)
            

        atexit.register(Disconnect, instance)
    
    except IOError as e:
        print("[ERROR] IOError", file=sys.stderr)

    except vim.fault.InvalidLogin as e:
        print("[ERROR] " + e.msg, file=sys.stderr)

    if not instance:
        raise SystemExit("[ERROR] Povezava z danimi podatki ni uspela!")

    print("[CONNECTED] Successfully connected!")
    return instance

def get_VMs(args):
    instance = connect(args)
    try:
        print("[RETRIEVING] Retrieving all ESX virtual machines")
        content = instance.RetrieveContent()

        container = content.rootFolder
        types = [vim.VirtualMachine]
        recursive = True

        container_view = content.viewManager.CreateContainerView(container, types, recursive)

        children = container_view.view
        print(f"[RETRIEVING] Successfully retrieved {len(children)} virtual machines")
        return children

    except Exception as e:
        print("[ERROR] " + e)
        raise SystemExit("[ERROR] Napaka pri pridobivanju VM-ov.")
            
def get_notes(args):
    vms = get_VMs(args)
    notes = []
    
    print("[READING] Reading notes from every VM")
    for vm in vms:
        discs = {}
        for storage in vm.storage.perDatastoreUsage:
            datastore = storage.datastore.info.name
            size = int(storage.committed / 1073741824)
            
            if datastore in discs:
                discs[datastore] += size
            else:
                discs[datastore] = size

        notes.append(VirtualMachine(vm.summary.config.name, vm.summary.config.annotation, vm.summary.config.memorySizeMB, vm.guest.ipAddress, discs))

    print("[READING] Successfully read all notes")

    return notes
