import requests
import sys

auth = {}
base_url = ""

def api_call(url):
    try:
        res = requests.get(url, headers=auth)
    except Exception as e:
        raise SystemExit("[ERROR] Povezava na BookStack z danimi podatki ni uspela!")
    
    if "error" in res.json():
        raise SystemExit("[ERROR] " + res.json()["error"]["message"])

    return res.json()

def update_content(system, page, new_contnet):
    old_page = api_call(f"{base_url}/api/pages/{page}")["html"]

    if not old_page:
        return "<p></p>" + new_contnet

    split1 = old_page.split(f"<!-- SYSTEM START {system} -->")
    if (len(split1) == 2):
        split2 = split1[1].split(f"<!-- SYSTEM END {system} -->")
        return "\n".join([split1[0], new_contnet, split2[1]])
    else:
        return "\n".join([old_page, new_contnet])

def update_page(system, book, page, content):
    print("[BOOKSTACK] Updating page...")
    url = f"{base_url}/api/pages/{page}"

    content = update_content(system, page, content)

    payload = {
        "book_id": book,
        "markdown": content
    }

    res = requests.put(url, headers=auth, data=payload)
    
    if res.status_code == 200:
        print("[BOOKSTACK] Page successfully updated!")
    else:
        print("[ERROR] " + res.json()["error"]["message"], file=sys.stderr)

def page_from_name(creds):
    books = api_call(f"{base_url}/api/books")

    book_id = -1
    for book in books["data"]:
        if book["name"] == creds["book"]:
            book_id = book["id"]
            break
    else:
        raise SystemExit(f"[ERROR] Book {creds['book']} was not found! Create it and try again...")

    pages = api_call(f"{base_url}/api/pages")
    for page in pages["data"]:
        if page["name"] == creds["page"] and page["book_id"] == book_id:
            return page["id"], page["book_id"]
    else:
        raise SystemExit(f"[ERROR] Page {creds['page']} was not found inside {creds['book']}! Create it and try again...")

def upload(system, creds, content):
    global auth, base_url
    auth = {"Authorization": f"Token {creds['id']}:{creds['secret']}"}
    base_url = f"http://{creds['host']}:{creds['port']}"

    print("[BOOKSTACK] Trying to connect to the BookStack wiki")

    page_id, book_id = page_from_name(creds)

    update_page(system, book_id, page_id, content)
