# RVP-notes

## Uporaba

```
pip install -r requirements.txt

python3 main.py <system_name> <config_file>       # pridobi podatke sistema <system>
python3 main.py all <config_file>                 # pridobi podatke vseh sistemov
```

## Config file
Vsak sistem mora imeti svoj vnos v config datoteki:
```
[<system_name>]             # Takšno bo tudi ime odseka na BookStack strani
platform = [esx | proxmox] 
user = <username>           # Pri proxmoxu mora vsebovati tudi realm (e.g. matej@pam)
pwd = <password>
host = <host>
ssl = [True | False]        # Preverjanje ssl certifikatov
port = <port>
```

Config datoteka mora prav tako vsebovati podatke za povezavo na BookStack:
```
[bookstack]
token_id = <bookstack_api_id>
token_secret = <bookstack_api_secret>
host = <bookstack_host>
port = 6875
ssl = [True | False]
book_name = <book_name>     # Podatki se bodo shranili na strani <page_name> v knjigi <book_name>
page_name = <page_name>     # Book in page morate ustvariti sami
```

## Shranjevanje v datoteko

Z uporabo stikala `--output <file>` se bodo podatki zapisali v datoteko namesto na BookStack. Kakor pri BookStacku se bo datoteka ob naslednjem klicanju programa ustrezno posodobila in ne bo izgubila podatkov drugih sistemov.

```
python3 main.py <system_name> <config_file> --output <file>
```

## Primer uporabe
Primer config datoteke za sistema "esx_sistem" in "proxmox_sistem" in uporaba programa:
```
[esx_sistem]
platform = esx
user = <esx_username>
pwd = <esx_password>
host = <esx_host>
ssl = [True | False]
port = 443

[proxmox_sistem]
platform = proxmox
user = <proxmox_username>
pwd = <proxmox_password>
host = <proxmox_host>
ssl = [True | False]
port = 8006

[bookstack]
token_id = <bookstack_api_id>
token_secret = <bookstack_api_secret>
host = <bookstack_host>
port = 6875
ssl = [True | False]               
book_name = <book_name>
page_name = <page_name>
```
```
python3 main.py esx_sistem config.txt       # prejme podatke sistema opisanega pod [esx_sistem]
python3 main.py proxmox_sistem config.txt   # prejme podatke sistema opisanega pod [proxmox_sistem]
python3 main.py all config.txt              # prejme podatke obeh sistemov
```

