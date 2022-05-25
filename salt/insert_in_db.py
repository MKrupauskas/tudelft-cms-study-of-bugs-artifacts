import mysql.connector
import argparse
import requests

issue_keys = ['id', 'title', 'html_url', 'created_at', 'number',
 'closed_at', 'comments', 'comments_url', 'labels', 'state', 'updated_at'
  ]   
pr_keys = ['id', 'title', 'html_url', 'created_at', 'number', 'closed_at', 'updated_at', 'merged_at', 'merge_commit_sha', 
'comments', 'comments_url', 'labels', 'state', 'commits', 'additions', 'deletions', 'changed_files' 
] 

# commit_keys = ['html_url', 'sha'
# ]


def get_mysql_insert_query(bug_data_type):
    if bug_data_type == "pr":
        return """INSERT salt_pr (
                            pull_request_id, title, url, created_at, number, closed_at, updated_at, merged_at, merge_commit_sha, comments, comments_url, labels, state, commits, additions, deletions, changed_files, commits_data, attempts_to_fix_issue_number, CMS
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    elif bug_data_type == "issue":
        return """INSERT salt_issue (
                            issue_id, title, url, created_at, number, closed_at, comments, comments_url, labels, state, updated_at, CMS
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    else: # bugdatatype is commit:
        return """INSERT salt_commit (
                            url, commit_id_used_to_get_JSON, attempts_to_fix_issue_number, CMS
                            ) VALUES (%s, %s, %s, %s) """


def get_json(search_id, bug_data_type, github_token):
    headers = {"Authorization": f"token {github_token}", 
    "Accept": "application/vnd.github.v3+json"}
    if bug_data_type == "pr":
        pr_url = f"https://api.github.com/repos/saltstack/salt/pulls/{search_id}"
        all_commits_in_pr_url = f"https://api.github.com/repos/saltstack/salt/pulls/{search_id}/commits"
        pr_json = requests.get(pr_url, headers=headers).json()
        pr_commits_json = requests.get(all_commits_in_pr_url, headers=headers).json()
        ret = []
        
        for keys in pr_keys:
            if keys == "labels":
                ls = pr_json.get("labels", None)
                if not ls:
                    ret.append("")
                else:
                    labelslist = []
                    for obj in ls:
                        labelslist.append(obj.get("name", None))
                    ret.append(",".join(labelslist))
            else:
                ret.append(pr_json.get(keys, None))
        
        if not pr_commits_json:
            ret.append("");
        else:
            shalist = []
            for obj in pr_commits_json:
                shalist.append(obj.get("sha", None))
            ret.append(",".join(shalist))
        
        return ret
    elif bug_data_type == "issue":
        url = f"https://api.github.com/repos/saltstack/salt/issues/{search_id}"
        issuejson = requests.get(url, headers=headers).json()
        ret = []
        for keys in issue_keys:
            if keys == "labels":
                labelslist = issuejson.get("labels", None)
                if not labelslist:
                    ret.append("")
                else:
                    labels = []
                    for obj in labelslist:
                        labels.append(obj.get("name", None))
                    ret.append(",".join(labels))
            else:
                ret.append(issuejson.get(keys, None))    
        return ret
    else:
        return [f"https://api.github.com/repos/saltstack/salt/commits/{search_id}", search_id]


def get_args():
    parser = argparse.ArgumentParser(description='Store bugs in MySQL database')
    parser.add_argument("host", help="host of the database in which to insert bug data")
    parser.add_argument("database", help="name of the databse in which the bug data will be stored")
    parser.add_argument("username", help="username, which is used to connect ot the database")
    parser.add_argument("password", help="password corresponding to the username provided, used to connect to the database")
    parser.add_argument("filenamewithbugs", help="filename of the txt file of bugs and fixes that resides in the root of the folder")
    parser.add_argument("token", help="Github token.")
    return parser.parse_args()

def main():
    args = get_args()
    ghtoken = args.token.rstrip()

    connection = mysql.connector.connect(host=args.host, database=args.database,\
        user=args.username,password=args.password)
    cursor = connection.cursor()
    
    lines =None
    with open(args.filenamewithbugs, 'r') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    with open("error.log", 'w') as logerr:
        for line in lines:
            data = line.split(",")
            issue = data[0]
            fixes = data[1].split(" ")
            issue_number = issue.split("/")[-1]

            try:
                issue_query = get_mysql_insert_query("issue")
                issue_list = get_json(issue_number, "issue", ghtoken)
                issue_list.append("salt")
                cursor.execute(issue_query, tuple(issue_list))
                connection.commit()
            except mysql.connector.Error as error:
                errmsg = []
                errmsg.append("problem at issue insertion")
                errmsg.append("problem at issue number {}".format(issue_number))
                errmsg.append("Failed to insert record into MySQL table {}".format(error))
                logerr.write("/n".join(errmsg))
            except Exception as e:
                logerr.write("Failed to insert record into MySQL table {}\n".format(str(e)))

            for fix_url in fixes:
                split = fix_url.split("/")
                search_id = split[-1]
                if "commit" in split:
                    try:
                        commit_query = get_mysql_insert_query("commit")
                        commit_list = get_json(search_id, "commit", ghtoken)
                        commit_list.append(int(issue_number))
                        commit_list.append("salt")
                        cursor.execute(commit_query, tuple(commit_list))
                        connection.commit()
                    except mysql.connector.Error as error: 
                        errmsg = []
                        errmsg.append("this insert failed {}".format(commit_list))
                        errmsg.append("problem at commit insertion")
                        errmsg.append("Failed to insert record into MySQL table {}".format(error))
                        errmsg.append("----------------------------------------------------")
                        logerr.write("\n".join(errmsg))
                    except Exception as e:
                        logerr.write("Failed to insert record into MySQL table {} \n".format(str(e)))
                else:
                    try: 
                        pr_query = get_mysql_insert_query("pr")
                        pr_list = get_json(search_id, "pr", ghtoken)
                        pr_list.append(int(issue_number))
                        pr_list.append("salt")
                        cursor.execute(pr_query, tuple(pr_list))
                        connection.commit()
                    except mysql.connector.Error as error: 
                        errmsg = []
                        errmsg.append("this is the insert query: {}".format(pr_query))
                        errmsg.append("problem at pull request insertion")
                        errmsg.append("pr_list size is : {}".format(len(pr_list)))
                        errmsg.append("pr_list contents: {}".format(pr_list))
                        errmsg.append("Failed to insert record into MySQL table {}".format(error))
                        print("Failed to insert record into MySQL table {}\n".format(error))
                        logerr.write("\n".join(errmsg))
                    except Exception as e:
                        logerr.write("Failed to insert record into MySQL table {} \n".format(str(e)))

    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        print("Done!")

main()


# The code in this file is modified from the main.py from https://github.com/MattiaBonfanti-CS/CSE3000-RP-Report.git

# MIT License

# Copyright (c) 2022 Mattia Bonfanti

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
