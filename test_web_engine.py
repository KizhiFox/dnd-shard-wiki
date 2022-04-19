from pathlib import Path
from bottle import get, static_file, run, route
import sys


@get('/style.css')
def style_css():
  return static_file('style.css', root='./docs')


@route('<filepath:path>')
def serve_static_file(filepath):
    print(Path('./docs' + filepath))
    if Path('./docs' + filepath).is_file():
        file_name = Path(filepath).name
        root = './docs' + str(Path(filepath).parent)
    else:
        file_name = 'index.html'
        root = './docs' + str(Path(filepath))
    print(file_name, root)
    return static_file(file_name, root=root)


if __name__ == '__main__':
    run(host='localhost', port=8080)
