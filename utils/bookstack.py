import requests
import sys

def update_page(book, chapter, page, content, auth, base_url):
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



def upload(platform, creds, content):
    auth = {"Authorization": f"Token {creds['id']}:{creds['secret']}"}
    base_url = f"http://{creds['host']}:{creds['port']}"

    url = f"{base_url}/api/chapters/{creds['chapter']}"

    res = requests.get(url, headers=auth)
    
    for page in res.json()["pages"]:
        if page["name"] == platform:
            update_page(page["book_id"], page["chapter_id"], page["id"], content, auth, base_url)
            break
    else:
        print("[BOOKSTACK] Creating new page...")
        url = f"{base_url}/api/pages"
        
        payload = {
            "chapter_id": creds["chapter"],
            "name": platform,
            "markdown": content
        }
        res = requests.post(url, headers=auth, data=payload)
        
        if res.status_code == 200:
            print("[BOOKSTACK] Successfully created new page")
        else:
            print("[ERROR] " + res.json()["error"]["message"], file=sys.stderr)
    
