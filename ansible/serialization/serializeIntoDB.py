import json
import sys

import datetime
import mysql.connector
import os
import sys
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("HOST")
DB_USERNAME = os.getenv("USERNAME")
DB_PASSWORD = os.getenv("PASSWORD")
DB_DATABASE = os.getenv("DATABASE")

connection = mysql.connector.connect(host=DB_HOST, database=DB_DATABASE, user=DB_USERNAME, password=DB_PASSWORD)
cursor = connection.cursor()


keys_to_store = ['issue_id', 'pull_request_id', 'number', 'title', 'body', 'issue_url', 'pull_request_url', 'created_at', 'closed_at', 'updated_at', 'state', 'labels', 'comments', 'comments_url', 'commits', 'additions', 'deletions', 'changed_files', 'commits_data', 'bug_report_url', 'bug_fix_url']

insert_query = """
INSERT INTO `bugs_fixes` (`system`, `issue_id`, `pull_request_id`, `number`, `title`, `body`, `issue_url`, `pull_request_url`, `created_at`, `closed_at`, `updated_at`, `state`, `labels`, `comments`, `comments_url`, `commits`, `additions`, `deletions`, `changed_files`, `commits_data`, `bug_report_url`, `bug_fix_url`) 
VALUES
('ansible', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

filename=sys.argv[1]

print("Serializing bugs from filtered-mapped file {} ...".format(filename))

# TODO: assertions

inserted_count=0

with open(filename) as f:
    data = json.load(f)

    for ob in data:
        ob["issue_id"]=ob["number"]
        ob["pull_request_id"]=ob["fix"]["id"]
        ob["issue_url"]=ob["html_url"]
        ob["pull_request_url"]=ob["fix"]["html_url"]
        ob["labels"]=list(map(lambda o: o["name"],ob["labels"]))
        ob["bug_report_url"]=ob["html_url"]
        ob["bug_fix_url"]=ob["fix"]["html_url"]

        # TODO: get this data
        ob["additions"]=-1
        ob["deletions"]=-1
        ob["changed_files"]=-1
        ob["commits_data"]=""


        to_insert_dict = {}
        for key in keys_to_store:
            if isinstance(ob.get(key, None), list):
                list_to_add = ob.get(key, [])
                to_insert_dict[key] = ','.join(list_to_add)
            else:
                to_insert_dict[key] = ob.get(key, None)
        
        cursor.execute(insert_query, tuple(to_insert_dict.values()))
        connection.commit()

        inserted_count += 1


print("{} total bugs serialized into DB.".format(inserted_count))


if connection and connection.is_connected():
    cursor.close()
    connection.close()
