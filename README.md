# RVP-notes

## Uporaba

```
pip install -r requirements.txt
```

### ESX:
```
python3 main.py esx --host <HOST-IP> --user <USER> [--pwd <PASSWORD>] [--port <PORT>] [--nossl]
```

### PROXMOX:
```
python3 main.py proxmox --host <HOST-IP> --user <USER> [--pwd <PASSWORD>] [--port <PORT>] [--nossl]
```

Obvezni parametri: platforma (esx/proxmox), host ter user

Opcijski parametri: geslo, port ter nossl

V primeru, da ne podatke gesla pri parametrih, vas bo program interaktivno vprašal po njemu.