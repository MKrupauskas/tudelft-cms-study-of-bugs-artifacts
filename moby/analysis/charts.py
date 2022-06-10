import json
# import matplotlib.pyplot as plt
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

# Initialize data
symptoms = {}
root_causes = {}

symptoms_root_causes = {}

impact = {
    "Low": {},
    "Medium": {},
    "High": {}
}
consequences = {}

fixes = {}
fixes_changes = {}

system_dependency = {
    "dependent": 0,
    "independent": 0,
    "systems": {
        "linux": 0,
        "windows": 0,
        "macos": 0
    }
}

triggers_errors = {}
triggers_characteristics = {}

# Read results files
iterations = 5
for iteration in range(1, iterations + 1):
    with open(f"./{results_folder}stats/iteration_{iteration}.json") as f:
        bugs = json.load(f)

        # Gather symptoms results
        for symptom, value in bugs["global"]["symptoms"].items():
            current_symptom_value = symptoms.get(symptom, 0)
            symptoms[symptom] = current_symptom_value + value

        # Gather symptoms results
        for cause, value in bugs["global"]["root_causes"].items():
            current_cause_value = root_causes.get(cause, 0)
            root_causes[cause] = current_cause_value + value

        # Gather root causes by symptoms
        for symptom, symptom_value in bugs["symptoms_root_causes"].items():
            symptom_obj = symptoms_root_causes.get(symptom, {})

            for cause, cause_value in symptom_value.items():
                current_cause_value = symptom_obj.get(cause, 0)
                symptom_obj[cause] = current_cause_value + cause_value

            symptoms_root_causes[symptom] = symptom_obj

        # Gather impact results
        for impact_level, impact_value in bugs["global"]["impact"].items():
            for consequence_key, consequence_value in impact_value.items():
                current_consequence_impact_value = impact[impact_level].get(consequence_key, 0)
                impact[impact_level][consequence_key] = current_consequence_impact_value + consequence_value

                current_consequence_value = consequences.get(consequence_key, 0)
                consequences[consequence_key] = current_consequence_value + consequence_value

        # Gather fixes results
        for fix_key, fix_value in bugs["global"]["fixes"].items():
            current_fix_value = fixes.get(fix_key, 0)
            fixes[fix_key] = current_fix_value + fix_value

            current_fix_changes_value = fixes_changes.get(fix_key, {"loc": 0, "files": 0})
            current_fix_changes_value["loc"] = current_fix_changes_value["loc"] + \
                                               bugs["fixes_changes"][fix_key]["loc"]
            current_fix_changes_value["files"] = current_fix_changes_value["files"] + \
                                                 bugs["fixes_changes"][fix_key]["files"]
            fixes_changes[fix_key] = current_fix_changes_value

        # Gather system dependency
        system_dependency["dependent"] += bugs["global"]["system_dependency"]["dependent"]
        system_dependency["independent"] += bugs["global"]["system_dependency"]["independent"]

        for os_system_key, os_system_value in bugs["global"]["system_dependency"]["systems"].items():
            if "linux" in os_system_key:
                system_dependency["systems"]["linux"] += os_system_value
            else:
                system_dependency["systems"][os_system_key] += os_system_value

        # Gather triggers errors
        for trigger_err_key, trigger_err_value in bugs["global"]["triggers"]["errors"].items():
            current_trigger_err_value = triggers_errors.get(trigger_err_key, 0)
            triggers_errors[trigger_err_key] = current_trigger_err_value + trigger_err_value

        # Gather triggers characteristics
        for trigger_char_key, trigger_char_value in bugs["global"]["triggers"]["characteristics"].items():
            current_trigger_char_value = triggers_characteristics.get(trigger_char_key, 0)
            triggers_characteristics[trigger_char_key] = current_trigger_char_value + trigger_char_value


# Plot symptoms
# plt.barh(list(symptoms.keys()), symptoms.values(), height=1/len(list(symptoms.keys())))
# plt.ylabel('Symptoms')
# plt.xlabel('Amounts')
# plt.title('Vehicles count')
# plt.show()
print("---------------- Symptoms ----------------")
print(json.dumps(symptoms, indent=4))
print()

# Plot root causes
# plt.barh(list(root_causes.keys()), root_causes.values(), height=1/len(list(root_causes.keys())))
# plt.show()
print("---------------- Root Causes ----------------")
print(json.dumps(root_causes, indent=4))
print()

# Plot root causes by symptoms
print(json.dumps(symptoms_root_causes, indent=4))
print()

# Plot impact and consequences
print("---------------- Impact & Consequences ----------------")
print(json.dumps(impact, indent=4))
print()
print(json.dumps(consequences, indent=4))
print()

# Plot fixes
print("---------------- Fixes ----------------")
print(json.dumps(fixes, indent=4))
print()
print(json.dumps(fixes_changes, indent=4))
print()

# System dependency
print("---------------- System Dependent ----------------")
print(json.dumps(system_dependency, indent=4))
print()

# Triggers
print("---------------- Triggers ----------------")
print(json.dumps(triggers_errors, indent=4))
print()
print(json.dumps(triggers_characteristics, indent=4))
print()
