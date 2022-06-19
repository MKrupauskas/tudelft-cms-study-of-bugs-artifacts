import json
import sys

filename = sys.argv[1]

print("Serializing file " + filename)

# Contains the output json file
resultfile = open("{}-out.json".format(filename), "wt")

data = []
with open(filename) as f:
    for line in f:
        try:
            data.append(json.loads(line))
        except:
            print("Failed loading line")

resultfile.write(json.dumps(data))
resultfile.close()
