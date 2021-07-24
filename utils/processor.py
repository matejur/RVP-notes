from yaml import safe_load
from dataclasses import dataclass


@dataclass(order=True)
class VirtualMachine:
    name: str
    note: str
    memory: int
    ip: str
    diski: str

def check(note, field):
    return field in note and note[field]

def process_notes(system, notes):
    print("[MARKDOWN] Started markdown processing")
    markdown = f"<!-- SYSTEM START {system} -->\n\n"
    markdown += f"# {system}\n"
    for vm in sorted(notes):
        ime = vm.name
        markdown += f"### {ime}\n"

        if vm.note:
            try:
                note = safe_load(vm.note)

                if type(note) is str:
                    raise TypeError

                err_msg = "PODATEK MANJKA"

                owner = note["owner"]                           if check(note, "owner") else err_msg
                admins = ', '.join(note['administrators'])      if check(note, "administrators") else err_msg
                users = ', '.join(note['users'])                if check(note, "users") else err_msg
                provides = ', '.join(note['provides'])          if check(note, "provides") else err_msg
                service = ', '.join(note['type_of_service'])    if check(note, "type_of_service") else err_msg
                dependencies = ', '.join(note['depends_on'])    if check(note, "depends_on") else err_msg
                desc = note['description']                      if check(note, "description") else err_msg
                auth = note['authentication']                   if check(note, "authentication") else err_msg
                last = note['last_update']                      if check(note, "last_update") else err_msg

                current = ""
                current += f"- Owner: `{owner}`\n"
                current += f"- Administrators: `{admins}`\n"
                current += f"- Users: `{users}`\n"
                current += f"- Provides: `{provides}`\n"
                current += f"- Service type: `{service}`\n"
                current += f"- Dependencies: `{dependencies}`\n"
                current += f"- Description:\n ```\n{desc}\n```\n"
                current += f"- Authentication: `{auth}`\n"
                current += f"- Last update: `{last}`"

                markdown += current
                print(f"[MARKDOWN] {ime} added to the markdown file")

            except TypeError:
                print(f"[MARKDOWN] {ime} note is not a yaml format")
                markdown += "Polje notes ni v YAML formatu:\n"
                markdown += f"```\n{vm.note}\n```"

            except Exception as e:
                print(f"[MARKDOWN] {ime} broken yaml format")
                if hasattr(e, "context_mark"):
                    markdown += "Pri obdelavi YAMLa je prišlo do napake:\n"
                    markdown += f"```\n{e.context_mark}\n```\n"
                else:
                    markdown += "Pri obdelavi YAMLa je prišlo do neznane napake:\n"

                markdown += f"```\n{vm.note}\n```"

        else:
            markdown += "Virtualka/container nima polja notes"
            print(f"[MARKDOWN] {ime} has nothing inside \"notes\"")

        markdown += f"\n- RAM: `{vm.memory} MB`\n"
        if vm.ip:
            markdown += f"- IP: `{vm.ip}`\n"
        else:
            markdown += f"- IP: `VM ni prižgan`\n"

        if vm.diski:
            markdown += "- DISKI: \n"
            markdown += vm.diski

        markdown += "\n***\n\n"

    markdown += f"<!-- SYSTEM END {system} -->\n"
    print("[MARKDOWN] Markdown processing finished")
    return markdown

def insert_system(system, old, new):
    if not old:
        return "<p></p>" + new.strip()

    updated = ""

    split1 = old.split(f"<!-- SYSTEM START {system} -->")
    if (len(split1) == 2):
        split2 = split1[1].split(f"<!-- SYSTEM END {system} -->")
        updated = split1[0] + new + split2[1]
    else:
        updated = old + new

    return updated.strip()
