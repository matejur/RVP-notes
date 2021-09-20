# RVP-notes

## Uporaba

```
pip install -r requirements.txt

python3 main.py <system_name> <config_file>       # pridobi podatke sistema <system>
```

## Config file
Vsak sistem mora imeti svoj vnos v config datoteki:
```
[<system_name>]             # Takšno bo tudi ime odseka na BookStack strani
type = node
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

## Proxmox cluster

```
[proxmox]
type = cluster
nodes = proxmox1, proxmox2      # seveda lahko naštejete poljubno število sistemov

[proxmox1]
type = node
... podatki za proxmox1 ...

[proxmox2]
type = node
... podatki za proxmox2 ...

... preostali podatki ...
```
`python3 main.py proxmox config.txt` - program bo sprva preveril dostopnost `proxmox1`, če je dostopen bo vse podatke prejel iz njega, v nasprotnem primeru bo preveril dostopnost `proxmox2`

## VCenter

```
[vcenter]
type = vcenter
nodes = esx1, esx2              # seveda lahko naštejete poljubno število sistemov
platform = esx
user = <vcenter_user>           # vključno z domeno
pwd = <vcenter_password>
host = <vcenter_host>
ssl = [True | False]
port = 443

[esx1]
type = node
... podatki za esx1 ...

[esx2]
type = node
... podatki za esx2 ...

... preostali podatki ...
```
`python3 main.py vcenter config.txt` - program bo sprva preveril dostopnost `vcentra`, če je dostopen bo vse podatke prejel iz njega, v nasprotnem primeru bo preveril dostopnost vseh ESX sistemov navedenih pod `nodes`, ter združil podatke iz njih.


## Primer uporabe
Primer config datoteke za sistema "esx_sistem" in "proxmox_sistem" in uporaba programa:
```
[esx_sistem]
type = node
platform = esx
user = <esx_username>
pwd = <esx_password>
host = <esx_host>
ssl = [True | False]
port = 443

[proxmox_sistem]
type = node
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

## VCenter example

```
[vcenter]
type = vcenter
nodes = esx1, esx2
platform = esx
user = <vcenter_username>
pwd = <vcenter_password>
host = <vcenter_host>
ssl = [True | False] 
port = 443

[esx1]
type = node
platform = esx
user = <esx1_username>
pwd = <esx1_password>
host = <esx1_host_>
ssl = [True | False] 
port = 443

[esx2]
type = node
platform = esx
user = <esx2_username>
pwd = <esx2_password>
host = <esx2_host_>
ssl = [True | False] 
port = 443
```

```
python3 main.py vcenter config.txt          # podatki se shranijo pod imenom vcenter
```

## Proxmox cluster example

```
[proxmox]
type = cluster
nodes = proxmox1, proxmox2

[proxmox1]
type = node
platform = proxmox
user = <proxmox1_username>
pwd = <proxmox1_password>
host = <proxmox1_host>
ssl = [True | False] 
port = 8006

[proxmox2]
type = node
platform = proxmox
user = <proxmox2_username>
pwd = <proxmox2_password>
host = <proxmox2_host>
ssl = [True | False] 
port = 8006
```

```
python3 main.py proxmox config.txt          # podatki se shranijo pod imenom proxmox
```