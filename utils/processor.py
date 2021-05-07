from yaml import safe_load
import sys


def process_notes(platform, notes):
    print("[MARKDOWN] Started markdown processing")
    with open(f"{platform}.md", "w") as f:
        for vm in notes:
            ime = vm[0]
            note = safe_load(vm[1])

            try:
                markdown = ""
                markdown += f"- Owner: `{note['owner']}`\n"
                markdown += f"- Administrators: `{', '.join(note['administrators'])}`\n"
                markdown += f"- Users: `{', '.join(note['users'])}`\n"
                markdown += f"- Provides: `{', '.join(note['provides'])}`\n"
                markdown += f"- Service type: `{', '.join(note['type_of_service'])}`\n"
                markdown += f"- Dependencies: `{', '.join(note['depends_on'])}`\n"
                markdown += f"- Description:\n ```{note['description']}```\n"
                markdown += f"- Authentication: `{note['authentication']}`\n"
                markdown += f"- Last update: `{note['last_update']}`\n\n***\n\n"

                f.write(f"## {ime}\n")
                f.write(markdown)
                print(f"[MARKDOWN] {ime} added to the markdown file")
            except Exception as e:
                print(f"[ERROR] {ime} wrong yaml format", file=sys.stderr)

    print("[MARKDOWN] Markdown processing finished")
