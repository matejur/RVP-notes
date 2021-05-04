from yaml import safe_load


def process_notes(notes):
    for note in notes:
        data = safe_load(note)
        print(data)
