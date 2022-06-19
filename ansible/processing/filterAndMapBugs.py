import json
import sys
import re

filename = sys.argv[1]
prDataFilename = sys.argv[2]

print(
    "Filtering issues from file {} and mapping with PRs from file {} ...".format(
        filename, prDataFilename
    )
)

total_count = 0
pr_count = 0
bug_count = 0
pr_label_count = 0
verified_count = 0
filtered_out_count = 0
pr_count_unmerged = 0
filtered_out_count_waiting = 0
support_core = 0


def mapIssues(data):
    bugIssues = dict()

    for ob in data:
        ob = ob["data"]
        if isValidBugIssue(ob):
            bugIssues[ob["number"]] = ob

    return bugIssues


def mapPRData(data):
    prData = dict()

    for ob in data:
        ob = ob["data"]
        prData[ob["number"]] = ob

    return prData


def mapFixes(data, mappedIssues, mappedPRData):
    issuesWithFixes = []

    for ob in data:
        ob = ob["data"]
        if "pull" in ob["html_url"]:
            if isValidBugPullRequest(ob) and "body" in ob and ob["body"] is not None:
                fixes = re.search(r"#(\d+)", ob["body"], re.IGNORECASE)

                if fixes is not None:
                    issueNumber = int(fixes.group(1))
                    if issueNumber in mappedIssues:
                        bugIssue = mappedIssues[issueNumber]
                        bugIssue["fix"] = ob
                        print("{}->{}".format(bugIssue["number"], ob["number"]))

                        if ob["number"] in mappedPRData:
                            print(
                                "Attaching PR data for PR number ".format(ob["number"])
                            )
                            bugIssue["fixData"] = mappedPRData[ob["number"]]

                        issuesWithFixes.append(bugIssue)

    return issuesWithFixes


def isValidBugPullRequest(ob):
    if "pull_request" not in ob:
        return False

    if ob["pull_request"]["merged_at"] is None:
        return False

    return True


def isValidBugIssue(ob):
    global total_count
    global pr_count
    global bug_count
    global pr_label_count
    global verified_count
    global filtered_out_count
    global pr_count_unmerged
    global filtered_out_count_waiting
    global support_core

    labelsMapped = list(map(lambda o: o["name"], ob["labels"]))
    total_count = total_count + 1

    if "bug" not in labelsMapped:
        return False

    if "issues" not in ob["html_url"]:
        return False

    if (
        "docs" in labelsMapped
        or "docsite" in labelsMapped
        or "docsite_pr" in labelsMapped
    ):
        filtered_out_count = filtered_out_count + 1
        return False

    if "waiting_on_contributor" in labelsMapped:
        filtered_out_count_waiting = filtered_out_count_waiting + 1
        return False

    if "has_pr" in labelsMapped:
        pr_label_count = pr_label_count + 1

    if "support:core" not in labelsMapped:
        return False

    support_core = support_core + 1

    if "verified" in labelsMapped:
        verified_count = verified_count + 1

    bug_count = bug_count + 1

    return True


with open(filename) as f, open(prDataFilename) as prDataFile:
    data = json.load(f)
    prData = json.load(prDataFile)

    mappedPRData = mapPRData(prData)

    mappedBugIssues = mapIssues(data)
    issuesWithFixes = mapFixes(data, mappedBugIssues, mappedPRData)

    print("Got {} valid bugs with fixes.".format(len(issuesWithFixes)))

    # TODO: prune data

    resultfile = open(
        "{}-filtered-mapped.json".format(filename.replace(".json", "")), "wt"
    )
    resultfile.write(json.dumps(issuesWithFixes))
    resultfile.close()


print("{} total issues.".format(total_count))
print("{} Bugs.".format(bug_count))
print("{} Bugs with PRs.".format(pr_count))
print("{} Verified bugs.".format(verified_count))
print("{} Bugs with the 'has_pr' label.".format(pr_label_count))
print(
    "{} Documentation Bugs Filtered out, leaving {}.".format(
        filtered_out_count, pr_count - filtered_out_count
    )
)
print("{} Unmerged PRs.".format(pr_count_unmerged))
print("{} support:core.".format(support_core))
