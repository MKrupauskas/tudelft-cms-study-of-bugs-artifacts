import json
import sys

filename=sys.argv[1]

print("Loading file {} into DB...".format(filename))

total_count=0

with open(filename) as f:
    data = json.load(f)

    for ob in data:
        labelsMapped=list(map(lambda o: o["name"],ob["data"]["labels"]))

        total_count=total_count+1

        if "bug" not in labelsMapped:
            continue


        bug_count=bug_count+1
        print("=====")
        print("BUG TITLE: '{}', LABELS: {}".format(ob["data"]["title"],labelsMapped))
        if "pull_request" in ob["data"]:
            pr_count=pr_count+1
            print(ob["data"]["pull_request"]) 
        else:
            print("<No PR>")
        print("=====")

print("{} total issues serialized.".format(total_count))


