import os
import shutil
import pathlib
import markdown
from slugify import slugify
from markdown.extensions.toc import TocExtension


def spell_card(ctx, title=None, level=None, school=None, casting_time=None, distance=None, components=None, duration=None, classes=None):

    spell_html = '<div class="spellcard">\n'

    if title:
        spell_html += f'<p class="spellcard-title">{title}</p>\n'
    if str(level).isdigit():
        level = str(level) + ' уровень'
    if level or school:
        spell_html += f'<p class="spellcard-level-school">{", ".join([x for x in [level, school] if x is not None])}</p>\n'
    if casting_time:
        spell_html += f'<p class="spellcard-property"><b>Время накладывания:</b> {casting_time}</p>\n'
    if distance:
        spell_html += f'<p class="spellcard-property"><b>Дистанция</b>: {distance}</p>\n'
    if components:
        spell_html += f'<p class="spellcard-property"><b>Компоненты</b>: {components}</p>\n'
    if duration:
        spell_html += f'<p class="spellcard-property"><b>Длительность</b>: {duration}</p>\n'
    if classes:
        spell_html += f'<p class="spellcard-property"><b>Классы</b>: {classes}</p>\n'

    text_blocks = [f'<p class="spellcard-text">{line}</p>' for line in ctx.content.split('\n') if line != '']
    content = '\n'.join(text_blocks)

    spell_html += f'{content}\n</div>'

    return spell_html


MD_DIRECTORY = 'markdown'
HTML_DIRECTORY = 'docs'
CSS_FILENAME = 'style.css'
HTML_LANG = 'ru'
TOC = TocExtension(
    toc_depth='2-6',
    slugify=slugify,
    anchorlink=True
)
EXTENSIONS = [
    TOC,
    'customblocks'
]
EXT_CONFIGS = {
    'customblocks': {
        'generators': {
            'spell_card': spell_card
        }
    }
}

def generate_webpage(md_filename, path):
    main_page_rel = "".join(["../" for _ in range(len(path))])

    navigation_links = f'/ <a href="{main_page_rel}">Main page</a>'
    routes = []
    for i, route in enumerate(path):
        routes.append(route)
        navigation_links += f' / <a href="{"".join(["../" for _ in range(len(path) - i - 1)])}">{route}</a>'
    navigation_links = navigation_links.replace('href=""', 'href="#"')

    output = f'''<!DOCTYPE html> 
<html lang="{HTML_LANG}">
<head>
<meta charset="utf-8">
<title>{'Main page' if len(routes) == 0 else routes[-1]}</title>
<link rel="icon" type="image/x-icon" href="{main_page_rel}favicon.ico">
<link rel="stylesheet" type="text/css" href="{main_page_rel}{CSS_FILENAME}">
</head>
<body>
<p>{navigation_links}</p>
'''

    with open(md_filename, 'r', encoding='utf8') as f:
        md_in = f.read()
    html_out = markdown.markdown(md_in, extensions=EXTENSIONS, extension_configs=EXT_CONFIGS)
    html_out = html_out.replace('="/', f'="{main_page_rel}')
    output += html_out

    output += '''
</body>
</html>
'''

    return output


if __name__ == '__main__':
    shutil.rmtree(HTML_DIRECTORY, ignore_errors=True)

    os.makedirs(HTML_DIRECTORY, exist_ok=True)
    shutil.copy(CSS_FILENAME, os.path.join(HTML_DIRECTORY, CSS_FILENAME))
    shutil.copy('favicon.ico', os.path.join(HTML_DIRECTORY, 'favicon.ico'))

    for root, dirs, files in os.walk('markdown'):
        for file in files:

            root_file = os.path.join(root, file)
            new_path = os.path.join(HTML_DIRECTORY, *pathlib.Path(root).parts[1:])
            new_file = os.path.join(new_path, file)

            os.makedirs(new_path, exist_ok=True)

            if '.md' in file:
                webpage = generate_webpage(root_file, pathlib.Path(root).parts[1:])
                html_file = os.path.join(new_path, ''.join(file.split('.')[:-1]) + '.html')
                with open(html_file, 'w', encoding='utf8') as f:
                    f.write(webpage)
            else:
                shutil.copy(root_file, new_file)
