#!/usr/bin/python3

import random
import itertools

def generate(team_names = None, index_array_length = None, max_index = None):
    assert team_names != None
    assert index_array_length != None
    assert max_index != None

    radnom_index_array_generator = ( [random.randint(0, max_index) for _ in range(index_array_length)] for _ in itertools.count() )
    return {
        teamName: randomIndexArray for teamName, randomIndexArray in zip(team_names, radnom_index_array_generator)
    }

if __name__ == '__main__':
    print(generate(team_names = ['One', 'Two', 'Three'], index_array_length = 4, max_index = 4))