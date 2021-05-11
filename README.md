# RVP-notes

## Uporaba

```
pip install -r requirements.txt

python3 main.py esx --file <pot/do/config>       # pridobi podatke iz ESX
python3 main.py proxmox --file <pot/do/config>   # pridobi podatke iz Proxmoxa
```

Config file mora biti sledeče oblike:
```
[esx]
user = <esx_username>
pwd = <esx_password>
host = <esx_host>
ssl = [True | False]
port = 443

[proxmox]
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
ssl = [True | False]               # tole še ni implementirano do konca
chapter_name = <chapter_name>      # v chapterju se bosta naredili strani "esx" in "proxmox"
```

