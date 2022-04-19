from pathlib import Path
from bottle import get, static_file, run, route
import sys


@get('/style.css')
def style_css():
  return static_file('style.css', root='html/style.css')


@route('<filepath:path>')
def serve_static_file(filepath):
    print(Path('./html' + filepath))
    if Path('./html' + filepath).is_file():
        file_name = Path(filepath).name
        root = './html' + str(Path(filepath).parent)
    else:
        file_name = 'index.html'
        root = './html' + str(Path(filepath))
    print(file_name, root)
    return static_file(file_name, root=root)


if __name__ == '__main__':
    run(host='localhost', port=8080)
