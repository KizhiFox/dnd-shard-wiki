import markdown
import os
import shutil
import pathlib


MD_DIRECTORY = 'markdown'
HTML_DIRECTORY = 'docs'
CSS_FILENAME = 'style.css'


def generate_webpage(md_filename, path):
    navigation_links = '/ <a href="/dnd-shard-wiki">Main page</a>'
    routes = []
    for i, route in enumerate(path):
        routes.append(route)
        navigation_links += f' / <a href=dnd-shard-wiki/{"/".join(routes)}>{route}</a>'

    output = f'''<!DOCTYPE html> 
<html lang="en">
<head>
<meta charset="utf-8">
<link rel=”stylesheet” type=”text/css” href=”/dnd-shard-wiki/{CSS_FILENAME}”>
</head>
<body>
<p>{navigation_links}</p>
'''

    md_in = open(md_filename)
    output += markdown.markdown(md_in.read())
    md_in.close()

    output += '''
</body>
</html>
'''

    return output


if __name__ == '__main__':
    shutil.rmtree(HTML_DIRECTORY, ignore_errors=True)

    os.makedirs(HTML_DIRECTORY, exist_ok=True)
    shutil.copy(CSS_FILENAME, os.path.join(HTML_DIRECTORY, CSS_FILENAME))

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
