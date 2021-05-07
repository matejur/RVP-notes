import atexit
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

def connect(args):
    instance = None

    try:
        if args.nossl:
            instance = SmartConnect(host=args.host, user=args.user, pwd=args.pwd, port=args.port, disableSslCertValidation=True)
        else:
            instance = SmartConnect(host=args.host, user=args.user, pwd=args.pwd, port=args.port)

        atexit.register(Disconnect, instance)
    
    except IOError as e:
        print(e)

    except vim.fault.InvalidLogin as e:
        print(e.msg)

    if not instance:
        raise SystemExit("Povezava z danimi podatki ni uspela!")

    return instance

def get_VMs(args):
    instance = connect(args)
    try:
        content = instance.RetrieveContent()

        container = content.rootFolder
        types = [vim.VirtualMachine]
        recursive = True

        container_view = content.viewManager.CreateContainerView(container, types, recursive)

        children = container_view.view

        return children

    except Exception as e:
        print(e)
        raise SystemExit("Napaka pri pridobivanju VM-ov.")
            
def get_notes(args):
    vms = get_VMs(args)

    notes = []

    for vm in vms:
        note = (vm.summary.config.name, vm.summary.config.annotation)
        notes.append(note)
    
    return notes
    