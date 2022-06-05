import json
import sys
import random

filename=sys.argv[1]

sample_count=20

print("Sampling issues for raw file {} ...".format(filename))

with open(filename) as f:
    data = json.load(f)

    picked = 0

    while picked < sample_count:

        ob = random.choice(data)

        labelsMapped=list(map(lambda o: o["name"],ob["data"]["labels"]))

        if "bug" not in labelsMapped:
            continue

        if "docs" in labelsMapped or "docsite" in labelsMapped or "docsite_pr" in labelsMapped or "support:core" not in labelsMapped:
            continue
        
        if "waiting_on_contributor" in labelsMapped or "needs_revision" in labelsMapped:
            continue

        if "pull_request" not in ob["data"]:
            continue

        if "/issues/" not in ob["data"]["pull_request"]["html_url"]:
            continue

        picked=picked+1
  
        print("=====")
        print("SAMPLE #{}.".format(picked))
        print("BUG TITLE: '{}'".format(ob["data"]["title"]))
        print("BUG LABELS: '{}'".format(labelsMapped))
        print("BUG URL: '{}'".format(ob["data"]["html_url"]))
        print("PULL REQUEST URL: ",ob["data"]["pull_request"]["html_url"]) 
        print("PULL REQUEST MERGED AT: ",ob["data"]["pull_request"]["merged_at"]) 
        print("=====")
