import os
import shutil
import pathlib
import markdown
from markdown.extensions.toc import TocExtension


MD_DIRECTORY = 'markdown'
HTML_DIRECTORY = 'docs'
CSS_FILENAME = 'style.css'


def generate_webpage(md_filename, path):
    main_page_rel = "".join(["../" for _ in range(len(path))])

    navigation_links = f'/ <a href="{main_page_rel}">Main page</a>'
    routes = []
    for i, route in enumerate(path):
        routes.append(route)
        navigation_links += f' / <a href="{"".join(["../" for _ in range(len(path) - i - 1)])}">{route}</a>'

    output = f'''<!DOCTYPE html> 
<html lang="en">
<head>
<meta charset="utf-8">
<title>{'Main page' if len(routes) == 0 else routes[-1]}</title>
<link rel="icon" type="image/x-icon" href="{main_page_rel}/favicon.ico">
<link rel="stylesheet" type="text/css" href="{main_page_rel}{CSS_FILENAME}">
</head>
<body>
<p>{navigation_links}</p>
'''

    with open(md_filename, 'r', encoding='utf8') as f:
        md_in = f.read()
    md_in.replace('="/', f'="{main_page_rel}')
    output += markdown.markdown(md_in, extensions=[TocExtension(toc_depth='2-6')])

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
