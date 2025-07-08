import os
import re
import json
import yaml
from datetime import datetime

# extract YAML frontmatter as a raw string from a .md or .ipynb file
def get_frontmatter_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if filepath.endswith('.md'):
        match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL | re.MULTILINE)
        return match.group(1).strip() if match else None

    elif filepath.endswith('.ipynb'):
        try:
            nb = json.loads(content)
            for cell in nb.get('cells', []):
                if cell.get('cell_type') == 'markdown':
                    source = ''.join(cell.get('source', []))
                    match = re.search(r"^---\s*\n(.*?)\n---", source, re.DOTALL | re.MULTILINE)
                    if match:
                        return match.group(1).strip()
        except json.JSONDecodeError:
            pass

    return None

# given a key, parse YAML frontmatter to get value for a specific key
def get_frontmatter_value(fm_text, key):
    if not fm_text:
        return None
    try:
        data = yaml.safe_load(fm_text)
        return data.get(key)
    except yaml.YAMLError:
        print(f"No {key} found")
        return ""
 
def get_author_names(fm_text):
    authors = get_frontmatter_value(fm_text, "authors")
    if isinstance(authors, list):
        return [a['name'] for a in authors if isinstance(a, dict) and 'name' in a]
    return []

# return myst card  ( https://mystmd.org/guide/dropdowns-cards-and-tabs#cards )
def gen_card(file_path):
    fm_text = get_frontmatter_text(file_path)

    title = get_frontmatter_value(fm_text, "title")
    authors = get_author_names(fm_text)
    date = get_frontmatter_value(fm_text, "date")
    if date:
        date = date.strftime("%B %-d")
    intro = get_frontmatter_value(fm_text, "intro")

    card = f''':::{{card}}
:link: {file_path}
:header: {date}
'''
    # add footer if authors exist
    if len(authors) > 0:
        card += f':footer: {", ".join(authors)}\n'

    card += f'''
[**{title}**]({file_path})

{intro}
:::

'''
    return card

# return grid of cards based on blogs in a directory    ( https://mystmd.org/guide/dropdowns-cards-and-tabs#grids )
def gen_grid(dir_path):
    output = f"::::{{grid}} 1 1 2 2\n\n"

    entries = os.listdir(dir_path)
    # sort blogs from newest to oldest based off their filename
    files = sorted([entry for entry in entries if entry.endswith('.md') or entry.endswith('.ipynb')], reverse=True)

    for filename in files:
        output += gen_card(f'{dir_path}/{filename}')
        output += "\n"
    
    output += "::::\n"
    return output