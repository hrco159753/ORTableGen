#!/usr/bin/python3

import random
import itertools

def generate(points:dict = None, teams:dict = None):
    teamsAquireArrayies = dict()
    for teamName, teamIndexArray in teams.items():
        teamAcquireArrayPerPoint = {
            pointName: list(map(lambda index: pointCharArray[index], teamIndexArray)) for pointName, pointCharArray in points.items() 
        }
        teamsAquireArrayies.update({teamName: teamAcquireArrayPerPoint})
    return teamsAquireArrayies

if __name__ == '__main__':
    import points
    import teams
    import json

    points = points.generate(mandatory_count = 5, optional_count = 5, char_array_length = 5)
    teams = teams.generate(team_names = ['One', 'Two', 'Three'], index_array_length = 5, max_index = 4)
    print(json.dumps(generate(points = points, teams = teams), indent = 4))