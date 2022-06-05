import json
import sys
import random

filename=sys.argv[1]

sample_count=20

print("Sampling fixes from raw file {} ...".format(filename))

with open(filename) as f:
    data = json.load(f)

    picked = 0
    current = 0
    while picked < sample_count:

        ob = random.choice(data)
        current=current+1

        labelsMapped=list(map(lambda o: o["name"],ob["data"]["labels"]))

        if "docs" in labelsMapped or "docsite" in labelsMapped or "docsite_pr" in labelsMapped or "support:core" not in labelsMapped:
            continue
        
        if "waiting_on_contributor" in labelsMapped or "needs_revision" in labelsMapped:
            continue

        if "Fixes" not in ob["data"]["body"]:
            continue

        if "Bugfix" not in ob["data"]["body"]:
            continue
            
        if "user" in ob["data"]:
            del ob["data"]["user"]

        if "user_data" in ob["data"]:
            del ob["data"]["user_data"]

        if "comments_data" in ob["data"]:
            del ob["data"]["comments_data"]   
    
        picked=picked+1

        print("=====")
        print("FIX URL: '{}'".format(ob["data"]["html_url"]))
        #   print("ISSUE URL: '{}'".format(ob["data"]["issue_url"]))
        # print("PULL REQUEST URL: ",ob["data"]["pull_request"]["html_url"]) 
        # print("PULL REQUEST MERGED AT: ",ob["data"]["pull_request"]["merged_at"]) 
        print("=====")
