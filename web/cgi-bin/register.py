#!/usr/bin/env python

import cgi, cgitb, os
from pathlib import Path

form = cgi.FieldStorage()

team_name = form.getvalue('teamName')

if team_name == None or len(team_name.strip()) == 0:
    print('HTTP/1.1 501 Not Implemented')
    exit(1)

absolute_path = os.path.dirname(__file__)
teamNamePath = Path(f'{absolute_path}/../res/ftp/teamNames.txt')
teamNamePath.touch(exist_ok = True)

with open(teamNamePath, 'r') as f:
    if any(map(lambda x: x == team_name, map(lambda x: x.strip(), f.readlines()))):
        print("Content-Type: text/html\n")
        print(f'''
        <!doctype html>
        <head>
            <title>Already exists</title>
        </head>
        <body>
            <h2>There is already a team with name '{team_name}'.</h2>
        </body>
        ''')
        exit(0)

with open(teamNamePath, 'a') as f:
    f.write(team_name+'\n')

print("Content-Type: text/html\n")
print(f'''
<!doctype html>
<head>
    <title>Success</title>
</head>
<body>
    <h2>Registration of team '{team_name}' is succesful.</h2>
</body>
''')
