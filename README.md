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
user = 
pwd = 
host = 
ssl = 
port = 

[proxmox]
user = 
pwd = 
host = 
ssl = 
port = 
```

