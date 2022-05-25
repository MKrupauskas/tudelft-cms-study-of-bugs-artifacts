import datetime
import mysql.connector
import os
import sys

from dateutil.tz import tzutc
from dotenv import load_dotenv
from perceval.backends.core.github import GitHub
from perceval.errors import RateLimitError
from data.utils import get_mysql_insert_query, get_start_date


# Load env variables
load_dotenv()
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# MySQL connection
connection = mysql.connector.connect(host=MYSQL_HOST, database=MYSQL_DB, user=MYSQL_USER, password=MYSQL_PASSWORD)
cursor = connection.cursor()

# Owner and repository names
(owner, repo) = GITHUB_REPO.split('/')

# Create a Git object, pointing to repo_url, using repo_dir for cloning
repo = GitHub(owner=owner, repository=repo, api_token=[GITHUB_TOKEN])

# Fetch all issues/pull requests as an iterator, and iterate it printing
# their number, and whether they are issues or pull requests
category = 0
if len(sys.argv) > 1:
    if sys.argv[1] == "issue":
        category = 0
    elif sys.argv[1] == "pull_request":
        category = 1
    else:
        raise ValueError("You can only provide 'issue' or 'pull_request' as arguments!")

CATEGORIES = ['issue', 'pull_request', 'repository']

keys_to_store = ['id', 'title', 'url', 'created_at', 'number', 'body', 'closed_at', 'comments', 'comments_url',
                 'labels', 'pull_request', 'state', 'commits', 'additions', 'deletions', 'changed_files',
                 'commits_data',  'updated_at']
synonyms = ["bug", "glitch", "error", "flaw", "failure", "bugfix"]

start_year, start_month, start_day, start_hours, start_minutes = get_start_date(CATEGORIES[category], cursor)
results = repo.fetch(category=CATEGORIES[category],
                     from_date=datetime.datetime(
                         start_year,
                         start_month,
                         start_day,
                         start_hours,
                         start_minutes,
                         tzinfo=tzutc()
                     ),
                     filter_classified=True)

inserted_records = 0

try:
    for item in results:
        data = item.get("data", None)
        if data:
            # Refine labels
            data["labels"] = list(map(lambda x: x["name"], data.get("labels", [])))

            # Fetch only bugs relevant data
            is_relevant = False
            for syn in synonyms:
                filtered_labels = list(filter(lambda x: syn in x, data["labels"]))

                if data["title"] is None or data["body"] is None:
                    is_relevant = False
                    break

                if len(filtered_labels) > 0 or syn in data["title"] or syn in data["body"]:
                    is_relevant = True
                    break

            # If issues are being analyzed, keep only the ones with a pull_request.
            if category == 0:
                if data.get("pull_request", None) is not None:
                    data["pull_request"] = data["pull_request"].get("url", None)
                if data.get("pull_request", None) is None:
                    is_relevant = False

            # Store relevant data only
            if is_relevant:
                data_dict = {}
                for key in keys_to_store:
                    if isinstance(data.get(key, None), list):
                        list_to_add = data.get(key, [])
                        data_dict[key] = ','.join(list_to_add)
                    else:
                        data_dict[key] = data.get(key, None)
                # Insert to MySQL
                try:
                    mySql_insert_query = get_mysql_insert_query(category)
                    cursor.execute(mySql_insert_query, tuple(data_dict.values()))
                    connection.commit()

                    inserted_records += 1
                    print(cursor.rowcount, f"Record inserted successfully into {CATEGORIES[category]} table")

                except mysql.connector.Error as error:
                    print("Failed to insert record into MySQL table {}".format(error))
except RateLimitError as err:
    print(err)

print(f"Inserted {inserted_records} items to the {CATEGORIES[category]} table.")

# Close connection to MySQL
if connection and connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")
