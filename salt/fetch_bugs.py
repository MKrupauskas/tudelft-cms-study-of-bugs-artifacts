"""Fetch salt bugs.

"""
import argparse
import requests
import os
import json
from datetime import datetime
import re


# salt_labels = ["severity-critical", "severity-high"] #
exclude_labels = ["Documentation", "won't-fix", "Duplicate"]

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        u"\u2192"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def filter_responses(x):
    return ('pull_request' not in x) and not any(label['name'] in exclude_labels for label in x['labels'])  

# Rate limit is 5000 requests per hour
def get_data(descriptions, token): #descriptions = the directory where to put things in
    name = "salt"
    filter_func = filter_responses
    ghtoken = token.replace('\r', '')
    headers = {"Authorization": f"token {ghtoken}"}
    data = []
    statistics = {}
    page = 1
    max_per_request = 100
    temp_data = []
    while True:
        first = False
        base = "https://api.github.com/repos/saltstack/salt/issues"
        url = "{base}?state=closed&labels={labelsAnd}&per_page={pp}&page={p}".format(
            # milestone=13, #13 is the number of the milestone "Approved" in the salt repository milestone={milestone}&
            base=base,
            labelsAnd="Bug",#",".join(salt_labels),
            pp=max_per_request,
            p=page
        )
        response = requests.get(url, headers=headers).json()
        if not response:
            break
        temp_data = response
        filtered = list(filter(filter_func, temp_data))
        # if not filtered:
        #     break
        res = []
        for item in filtered:
            created = datetime.strptime(
                item['created_at'], "%Y-%m-%dT%H:%M:%S%z")
            resolution = datetime.strptime(
                item['closed_at'], "%Y-%m-%dT%H:%M:%S%z")
            passed = resolution - created
            reporter = item['user']['login']
            if item['assignee']:
                assignee = item['assignee']['login']
            else:
                assignee = ""
            comments = int(item['comments'])
            stats = {
                "created": str(created),
                "resolution": str(resolution),
                "passed": str(passed),
                "comments": comments,
                "reporter": reporter,
                "assignee": assignee,
                "reporter_is_assigned": reporter == assignee
            }
            statistics[name + '-' + str(item['number'])] = stats
            res.append(item['html_url'])
            # print(type(item['body']))
            description = item["body"]
            if isinstance(description, str) or isinstance(description, bytes):
                description = remove_emojis(item['body']) 
            description = description if description is not None else ""
            filename = name + '-' + str(item['number'])
            with open(os.path.join(descriptions, filename), 'w') as out:
                out.write(description)
        data.extend(res)
        page += 1
    return data, statistics


def get_args():
    parser = argparse.ArgumentParser(description='Fetch bugs from Salt.')
    parser.add_argument("output", help="File to save the bugs.")
    parser.add_argument("descriptions", help="Directory to save files with descriptions")
    parser.add_argument("statistics", help="File to save stats")
    parser.add_argument("token", help="Github token.")
    return parser.parse_args()



def fetch_bugs():
    args = get_args()
    os.makedirs(args.descriptions, exist_ok=True)

    # descriptions = "bug_descriptions"
    # output = "salt.txt"
    # statsjson = "salt.json"
    
    # os.makedirs(descriptions, exist_ok=True)
    data, statistics = get_data(args.descriptions, args.token)
    print("done with API calls now")
    print('writing data')
    directory, _ = os.path.split(args.output)
    stats_dir, _ = os.path.split(args.statistics)
    if directory:
        os.makedirs(directory, exist_ok=True)
    if stats_dir:
        os.makedirs(stats_dir, exist_ok=True)
    with open(args.output, 'w') as f:
        for url in data:
            f.write(url + "\n")
    with open(args.statistics, 'w') as f:
        json.dump(statistics, f, indent=4)
    print("Done!")
fetch_bugs()


# The code in this file is a modification of the code from https://github.com/hephaestus-compiler-project/types-bug-study-artifact/blob/master/LICENSE
# MIT License

# Copyright (c) 2021 Stefanos Chaliasos, Thodoris Sotiropoulos, Georgios-Petros Drosos, Charalambos Mitropoulos, Dimitris Mitropoulos, and Diomidis Spinellis

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.