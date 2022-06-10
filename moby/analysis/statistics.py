import json
import sys


# Define the system to retrieve information from
system = "moby"
results_folder = ""
if len(sys.argv) > 1:
    if sys.argv[1] == "moby":
        system = "moby"
        results_folder = ""
    elif sys.argv[1] == "puppet":
        system = "puppet"
        results_folder = "puppet/"
    else:
        raise ValueError("You can only provide 'moby' or 'puppet' as arguments!")

# Read results files
iteration = 1
if len(sys.argv) > 2:
    iteration = int(sys.argv[2])

with open(f"./{results_folder}results/iteration_{iteration}.json") as f:
    bugs = json.load(f)

# Initialize stats object to gather insights
stats = {
    "symptoms": {},
    "root_causes": {},
    "impact": {
        "Low": {},
        "Medium": {},
        "High": {}
    },
    "fixes": {},
    "system_dependency": {
        "dependent": 0,
        "independent": 0,
        "systems": {}
    },
    "triggers": {
        "errors": {},
        "characteristics": {}
    }
}

stats_symptom_causes = {}

fixes_changes = {}

# Gather statistics
for bug in bugs.items():
    # Symptoms
    current_symptom_amount = stats["symptoms"].get(bug[1]["symptoms"], 0)
    stats["symptoms"][bug[1]["symptoms"]] = current_symptom_amount + 1

    # Root causes
    current_root_causes_amount = stats["root_causes"].get(bug[1]["root_causes"]["category"], 0)
    stats["root_causes"][bug[1]["root_causes"]["category"]] = current_root_causes_amount + 1

    # Interpolate symptoms and root causes
    if bug[1]["symptoms"] not in stats_symptom_causes.keys():
        stats_symptom_causes[bug[1]["symptoms"]] = {}

    current_symptom_root_cause_amount = stats_symptom_causes[bug[1]["symptoms"]]\
        .get(bug[1]["root_causes"]["category"], 0)
    stats_symptom_causes[bug[1]["symptoms"]][bug[1]["root_causes"]["category"]] = current_symptom_root_cause_amount + 1

    # Impact
    for impact_category in bug[1]["impact"]["subcategory"]:
        current_impact_amount = stats["impact"][bug[1]["impact"]["category"]].get(impact_category, 0)
        stats["impact"][bug[1]["impact"]["category"]][impact_category] = current_impact_amount + 1

    # Fixes
    for fix_category in bug[1]["fixes"]["categories"]:
        current_fixes_amount = stats["fixes"].get(fix_category, 0)
        stats["fixes"][fix_category] = current_fixes_amount + 1

        current_fix_changes_value = fixes_changes.get(fix_category, {"loc": 0, "files": 0})
        current_fix_changes_value["loc"] = current_fix_changes_value["loc"] + \
                                             bug[1]["fixes"]["stats"]["additions"] + \
                                             bug[1]["fixes"]["stats"]["deletions"]
        current_fix_changes_value["files"] = current_fix_changes_value["files"] + \
                                             bug[1]["fixes"]["stats"]["changed_files"]
        fixes_changes[fix_category] = current_fix_changes_value

    # System dependency
    if bool(bug[1]["system_dependency"]["outcome"]):
        stats["system_dependency"]["dependent"] += 1
    else:
        stats["system_dependency"]["independent"] += 1

    for os_system in bug[1]["system_dependency"]["found"]:
        current_system_amount = stats["system_dependency"]["systems"].get(os_system, 0)
        stats["system_dependency"]["systems"][os_system] = current_system_amount + 1

    # Triggers
    for trigger in bug[1]["triggers"]["errors"]:
        current_error_amount = stats["triggers"]["errors"].get(trigger, 0)
        stats["triggers"]["errors"][trigger] = current_error_amount + 1

    for characteristic in bug[1]["triggers"]["characteristics"]:
        current_characteristic_amount = stats["triggers"]["characteristics"].get(characteristic, 0)
        stats["triggers"]["characteristics"][characteristic] = current_characteristic_amount + 1

# Set global stats
all_stats = {
    "configuration_management_system": system,
    "global": stats,
    "symptoms_root_causes": stats_symptom_causes,
    "fixes_changes": fixes_changes
}

# Store results
with open(f"./{results_folder}stats/iteration_{iteration}.json", "w", encoding="utf-8") as f:
    json.dump(all_stats, f, ensure_ascii=False, indent=4)
    print(json.dumps(all_stats, indent=4))
