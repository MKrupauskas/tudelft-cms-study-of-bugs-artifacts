import json
import sys
import random

filename=sys.argv[1]

filenameAlreadySampled=sys.argv[2]


sample_count=20
output_raw=True

print("Sampling fixes from filtered-mapped file {} ...".format(filename))

# TODO: assertions

with open(filename) as f, open(filenameAlreadySampled) as alreadySampled:
    data = json.load(f)

    picked = 0
    while picked < sample_count:
        ob = random.choice(data)

        if ob["number"] in alreadySampled or ob["fix"]["number"] in alreadySampled:
            print("Skipping already sampled ",ob["number"])
            continue

        picked=picked+1

        if output_raw:
            print("{} {}".format(ob["html_url"],ob["fix"]["html_url"]))
        else:
            print("=====")
            print("ISSUE URL: '{}'".format(ob["html_url"]))
            print("FIX URL: '{}'".format(ob["fix"]["html_url"]))
            print("=====")
