import json
import os
import sys
import csv


with open("results/categorized.tsv") as categorizedFile:
    categorizedBugs = csv.reader(categorizedFile, delimiter="\t", quotechar='"')

    # For aggregating amounts
    results = {
        "symptoms": {},
        "root_causes": {},
        "impact_severities": {},
        "impact_consequences": {},
        "code_fixes": {},
        "conceptual_fixes": {},
        "system_dependencies": {},
        "system_dependencies_systems": {},
        "trigger_causes": {},
        "trigger_reproductions": {},
    }

    for categorizedBug in categorizedBugs:
        if len(categorizedBug) == 0:
            print("Skipping iteration boundary")
            continue

        (
            bugUrl,
            fixUrl,
            symptomCode,
            rootCauseCode,
            impactSeverity,
            impactConsequence,
            codeFix,
            conceptualFix,
            systemDependency,
            triggerCause,
            triggerReproduction,
            *rest,
        ) = categorizedBug

        print(
            bugUrl,
            fixUrl,
            symptomCode,
            rootCauseCode,
            impactSeverity,
            impactConsequence,
            codeFix,
            conceptualFix,
            systemDependency,
            triggerCause,
            triggerReproduction,
            rest,
        )

        results = results.get(key, default=None)

    # Write aggregation
    with open(f"results/categorization_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        print(json.dumps(results, indent=4))
