#!/usr/bin/python3

import random
import itertools

def generateNames(mandatory_count = None, optional_count = None, mandatory_letter = 'M', optional_letter = 'O'):

    assert mandatory_count != None
    assert optional_count != None

    return [
        f"{mandatory_letter}{i+1}" for i in range(mandatory_count)
    ] + [
        f"{optional_letter}{i+1}" for i in range(optional_count)
    ]

def generate(char_array_length = None, *args, **kwargs):
    assert char_array_length != None

    randomArrayGenerator = ( [chr(random.randint(ord('A'), ord('Z'))) for _ in range(char_array_length)] for _ in itertools.count())
    
    return { pointName: randomArray for pointName, randomArray in zip(generateNames(*args, **kwargs), randomArrayGenerator) }

if __name__ == '__main__':
    print(generateNames(mandatory_count = 1, optional_count = 2))
    print(generate(char_array_length = 5, mandatory_count = 1, optional_count = 2))