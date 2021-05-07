from yaml import safe_load
import sys


def process_notes(platform, notes):
    print("[MARKDOWN] Started markdown processing")
    markdown = ""
    for vm in notes:
        ime = vm[0]
        note = safe_load(vm[1])

        try:
            current = ""
            current += f"- Owner: `{note['owner']}`\n"
            current += f"- Administrators: `{', '.join(note['administrators'])}`\n"
            current += f"- Users: `{', '.join(note['users'])}`\n"
            current += f"- Provides: `{', '.join(note['provides'])}`\n"
            current += f"- Service type: `{', '.join(note['type_of_service'])}`\n"
            current += f"- Dependencies: `{', '.join(note['depends_on'])}`\n"
            current += f"- Description:\n ```{note['description']}```\n"
            current += f"- Authentication: `{note['authentication']}`\n"
            current += f"- Last update: `{note['last_update']}`\n\n***\n\n"

            markdown += f"## {ime}\n"
            markdown += current
            print(f"[MARKDOWN] {ime} added to the markdown file")
        except Exception as e:
            print(f"[ERROR] {ime} wrong yaml format", file=sys.stderr)

    print("[MARKDOWN] Markdown processing finished")
    return markdown
