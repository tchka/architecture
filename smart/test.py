import os

path = '/static/layout.css'
if path[0] == '/':
    path = path[1:]
dir = os.getcwd()
dir = os.path.split(dir)[0]

print (dir)

static_file = os.path.join(dir, path)

print(static_file)

if os.path.exists(static_file):
    with open(static_file, 'r') as f:
        file_content = f.read()

    extension = path.split('.')[-1]
    print(extension)
