from yaml import safe_load

def check(note, field):
    return field in note and note[field]

def process_notes(notes):
    print("[MARKDOWN] Started markdown processing")
    markdown = ""
    for vm in notes:
        ime = vm[0]
        markdown += f"## {ime}\n"

        if vm[1]:
            try:
                note = safe_load(vm[1])

                if type(note) is str:
                    raise TypeError

                err_msg = "PODATEK MANJKA"

                owner = note["owner"]                           if check(note, "owner") else err_msg
                admins = ', '.join(note['administrators'])      if check(note, "administrators") else err_msg
                users = ', '.join(note['users'])                if check(note, "users") else err_msg
                provides = ', '.join(note['provides'])          if check(note, "provides") else err_msg
                service = ', '.join(note['type_of_service'])    if check(note, "type_of_service") else err_msg
                dependencies = ', '.join(note['depends_on'])    if check(note, "depends_on") else err_msg
                desc = f"```\n{note['description']}\n```"       if check(note, "description") else err_msg
                auth = note['authentication']                   if check(note, "authentication") else err_msg
                last = note['last_update']                      if check(note, "last_update") else err_msg

                current = ""
                current += f"- Owner: `{owner}`\n"
                current += f"- Administrators: `{admins}`\n"
                current += f"- Users: `{users}`\n"
                current += f"- Provides: `{provides}`\n"
                current += f"- Service type: `{service}`\n"
                current += f"- Dependencies: `{dependencies}`\n"
                current += f"- Description:\n {desc}\n"
                current += f"- Authentication: `{auth}`\n"
                current += f"- Last update: `{last}`"

                markdown += current
                print(f"[MARKDOWN] {ime} added to the markdown file")
            except:
                print(f"[MARKDOWN] {ime} has a broken yaml format")
                markdown += "Broken yaml format:\n"
                markdown += f"```\n{vm[1]}\n```"
        else:
            markdown += "Virtualka/container nima polja notes"
            print(f"[MARKDOWN] {ime} has nothing inside \"notes\"")

        markdown += "\n***\n\n"

    print("[MARKDOWN] Markdown processing finished")
    return markdown
