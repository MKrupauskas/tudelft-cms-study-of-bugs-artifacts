import json
import sys

filename=sys.argv[1]

print("Serializing file "+filename)

# Contains the output json file
resultfile = open("{}-out.json".format(filename), 'wt')

data = []
with open(filename) as f:
    for line in f:
        data.append(json.loads(line))

resultfile.write(json.dumps(data))
resultfile.close()