import json
import mysql.connector
import os
import sys

from analysis.models import symptoms, root_causes, impact, fixes, consequences, \
    system_dependent, triggers, characteristics
from dotenv import load_dotenv


# Load env variables
load_dotenv()
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# Define the system to retrieve information from
system = "moby"
table = "bugs_fixes_sample"
results_folder = ""
if len(sys.argv) > 1:
    if sys.argv[1] == "moby":
        system = "moby"
        table = "bugs_fixes_sample"
        results_folder = ""
    elif sys.argv[1] == "puppet":
        system = "puppet"
        table = "puppet"
        results_folder = "puppet/"
    else:
        raise ValueError("You can only provide 'moby' or 'puppet' as arguments!")

# Read iterations files
iteration = 1
if len(sys.argv) > 2:
    iteration = int(sys.argv[2])

with open(f"./{results_folder}iterations/iteration_{iteration}.tsv") as f:
    iterations = f.read().split("\n")

# MySQL connection
connection = mysql.connector.connect(host=MYSQL_HOST, database=MYSQL_DB, user=MYSQL_USER, password=MYSQL_PASSWORD)
cursor = connection.cursor(dictionary=True)

# Retrieve results from bugs sample
bugs = {}
try:
    select_query = f"SELECT * FROM {table} WHERE `symptoms` != '' AND `consequences` != '' " \
                   f"AND `iteration` = {iteration}"
    cursor.execute(select_query)
    result = cursor.fetchall()

    for idx, row in enumerate(result):
        bug_id = f"{system}_{row['number']}"

        bug_symptoms = symptoms[row['symptoms']]['name']
        bug_root_causes = root_causes[row['root_causes']]['name']

        bug_impact = row['impact']
        bug_consequences = []
        for consequence in row['consequences'].split(','):
            bug_consequences.append(consequences[consequence]['name'])

        if len(row['system_dependent']) == 0:
            bug_systems = []
            bug_dependency = False
        else:
            bug_systems = row['system_dependent'].split(',')
            bug_dependency = len(bug_systems) == 1

        bug_triggers_list = []
        for trigger in row['triggers'].split(','):
            bug_triggers_list.append(triggers[trigger]['name'])

        bug_characteristics_list = []
        for charact in row['characteristics'].split(','):
            bug_characteristics_list.append(characteristics[charact]["name"])

        bug_triggers = {
            "errors": bug_triggers_list,
            "characteristics": bug_characteristics_list
        }

        bug_fixes_list = []
        for fix in row['fixes'].split(','):
            bug_fixes_list.append(fixes[fix]['name'])

        bug_fixes = {
            "stats": {
                "commits": row.get('commits', None),
                "additions": row.get('additions', None),
                "deletions": row.get('deletions', None),
                "changed_files": row.get('changed_files', None)
            },
            "categories": bug_fixes_list
        }

        # Retrieve URLs
        bug_report_url = None
        bug_fix_url = None
        if len(iterations) > 0:
            iteration_urls = iterations[idx].split('\t')
            bug_report_url = iteration_urls[0]
            bug_fix_url = iteration_urls[1]

        bugs[bug_id] = {
            "configuration_management_system": system,
            "bug_report": bug_report_url,
            "bug_fix": bug_fix_url,
            "symptoms": bug_symptoms,
            "root_causes": {
                "category": bug_root_causes,
                "subcategory": ""
            },
            "impact": {
                "category": bug_impact,
                "subcategory": bug_consequences
            },
            "fixes": bug_fixes,
            "system_dependency": {
                "outcome": bug_dependency,
                "found": bug_systems
            },
            "triggers": bug_triggers
        }

    # Store results
    with open(f"./{results_folder}results/iteration_{iteration}.json", "w", encoding="utf-8") as f:
        json.dump(bugs, f, ensure_ascii=False, indent=4)
        print(json.dumps(bugs, indent=4))

except Exception as err:
    print(err)

print(f"Analysis of {system} completed.")
