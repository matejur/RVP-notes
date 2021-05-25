# RVP-notes

## Uporaba

```
pip install -r requirements.txt

python3 main.py <system> <config_file>      # pridobi podatke sistema <system>
python3 main.py all <config_file>           # pridobi podatke vseh sistemov
```

## Config file
Vsak sistem mora imeti svoj vnos v config datoteki:
```
[<system>]                  # Takšno bo tudi ime strani na BookStacku
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
chapter_name = <chapter_name>       # v chapterju se bo naredila strani za vsak sistem
```

## Primer uporabe
Primer config datoteke za sistema "esx" in "proxmox" in uporaba programa:
```
[esx]
platform = esx
user = <esx_username>
pwd = <esx_password>
host = <esx_host>
ssl = [True | False]
port = 443

[proxmox]
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
chapter_name = <chapter_name>
```
```
python3 main.py esx config.txt      # prejme podatke sistema opisanega pod [esx]
python3 main.py proxmox config.txt  # prejme podatke sistema opisanega pod [proxmox]
python3 main.py all config.txt      # prejme podatke obeh sistemov
```

