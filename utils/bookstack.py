import requests
import sys

auth = {}
base_url = ""

def update_page(book, chapter, page, content):
    print("[BOOKSTACK] Page already exists. Updating...")
    url = f"{base_url}/api/pages/{page}"

    payload = {
        "book_id": book,
        "chapter_id": chapter,
        "markdown": content
    }

    res = requests.put(url, headers=auth, data=payload)
    
    if res.status_code == 200:
        print("[BOOKSTACK] Page successfully updated!")
    else:
        print("[ERROR] " + res.json()["error"]["message"], file=sys.stderr)

def chapter_from_name(creds):
    url = f"{base_url}/api/chapters/"

    print("[BOOKSTACK] Trying to connect to the BookStack wiki")

    try:
        res = requests.get(url, headers=auth)
    except Exception as e:
        raise SystemExit("[ERROR] Povezava na BookStack z danimi podatki ni uspela!")
    
    if "error" in res.json():
        raise SystemExit("[ERROR] " + res.json()["error"]["message"])

    for chapter in res.json()["data"]:
        if chapter["name"] == creds["chapter"]:
            return chapter["id"]
    else:
        raise SystemExit(f"[ERROR] Chapter {creds['chapter']} was not found! Create it and try again...")



def upload(platform, creds, content):
    global auth, base_url
    auth = {"Authorization": f"Token {creds['id']}:{creds['secret']}"}
    base_url = f"http://{creds['host']}:{creds['port']}"

    chapter_id = chapter_from_name(creds)

    url = f"{base_url}/api/chapters/{chapter_id}"
    res = requests.get(url, headers=auth)

    for page in res.json()["pages"]:
        if page["name"] == platform:
            update_page(page["book_id"], page["chapter_id"], page["id"], content)
            break
    else:
        print("[BOOKSTACK] Creating new page...")
        url = f"{base_url}/api/pages"
        
        payload = {
            "chapter_id": chapter_id,
            "name": platform,
            "markdown": content
        }
        res = requests.post(url, headers=auth, data=payload)
    
        if res.status_code == 200:
            print("[BOOKSTACK] Successfully created new page")
        else:
            print("[ERROR] " + res.json()["error"]["message"], file=sys.stderr)
    
