#without replacement
import json
from random import choice
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Get N random numbers without replacement')
    parser.add_argument("n", help="n is the number of random number to sample")
    return parser.parse_args()


def sample_numbers():

    to_exclude = []
    with open("already_sampled.json", 'r') as f:
        to_exclude = json.load(f)
        to_exclude = set(to_exclude)

    args = get_args()
    sampled_numbers = []
    for i in range(int(args.n)):
        chosen_number = choice(list(set([x for x in range(1, 5897)]) - to_exclude)) #inclusive, exclusive
        to_exclude.add(chosen_number)
        sampled_numbers.append(str(chosen_number))


    with open("already_sampled.json", 'w') as f:
        # indent=2 is not needed but makes the file human-readable 
        # if the data is nested
        json.dump(list(to_exclude), f, indent=2) 

    print(" ".join(list(sampled_numbers)))

sample_numbers()
