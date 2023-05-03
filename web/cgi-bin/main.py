#!/usr/bin/env python

import os
from pathlib import Path

absolute_path = os.path.dirname(__file__)
teamNamePath = Path(f'{absolute_path}/../res/ftp/teamNames.txt')
teamNamePath.touch(exist_ok = True)

with open(teamNamePath, 'r') as f:
    teamNames = list(filter(lambda x: len(x) != 0, map(lambda x: x.strip(), f.readlines())))

registeredTeamList = f'''
<ol type = "1">
    {''.join(map(lambda x: f'<li>{x}</li>', teamNames))}
</ol>''' if len(teamNames) > 0 else '<i><b>No teams yet.</b></i>'

print("Content-Type: text/html\n")
print(f'''
<!doctype html>
<head>
    <title>Main</title>
</head>
<body>
    <section>
        <a href="/res/static/Rules.html">Rules</a>
    </section>
    <section>
    <h2>Registration</h2>
    <hr>
    <form action="/cgi-bin/register.py" target="" method="POST">
         <label for="teamName">Team name:</label><br/>
         <input type="text" id="teamName" name="teamName" required><br/>
         <input type="submit" value="Submit">
    </form>
    </section>
    <section>
    <h2>Teams</h2>
    <hr>
        {registeredTeamList}
    </section>
</body>
''')