from yaml import safe_load
import sys


def process_notes(notes):
    print("[MARKDOWN] Started markdown processing")
    markdown = ""
    for vm in notes:
        ime = vm[0]
        markdown += f"## {ime}\n"

        if vm[1]:
            try:
                note = safe_load(vm[1])

                err_msg = "PODATKA NI V YAMLu"

                owner = note["owner"] if "owner" in note else err_msg
                admins = ', '.join(note['administrators']) if "administrators" in note else err_msg
                users = ', '.join(note['users']) if "users" in note else err_msg
                provides = ', '.join(note['provides']) if "provides" in note else err_msg
                service = ', '.join(note['type_of_service']) if "type_of_service" in note else err_msg
                dependencies = ', '.join(note['depends_on']) if "depends_on" in note else err_msg
                desc = f"```\n{note['description']}\n```" if "description" in note else err_msg
                auth = note['authentication'] if "authentication" in note else err_msg
                last = note['last_update'] if "last_update" in note else err_msg

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
                markdown += "Broken yaml format\n"
                markdown += f"```\n{vm[1]}\n```"
        else:
            markdown += "Virtualka/container nima polja notes"
            print(f"[MARKDOWN] {ime} has nothing inside \"notes\"")

        markdown += "\n***\n\n"

    print("[MARKDOWN] Markdown processing finished")
    return markdown
