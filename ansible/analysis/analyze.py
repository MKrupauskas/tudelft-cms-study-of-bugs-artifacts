import json
import os
import sys
import csv

totalCount=0

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

        totalCount=totalCount+1

        (
            bugUrl,
            fixUrl,
            symptom,
            rootCause,
            impactSeverity,
            impactConsequence,
            codeFix,
            conceptualFix,
            systemDependency,
            triggerCause,
            triggerReproduction,
            *rest,
        ) = categorizedBug

        # Aggregate counts
        results["symptoms"][symptom] = results["symptoms"].get(symptom, 0) + 1
        results["root_causes"][rootCause] = results["root_causes"].get(rootCause, 0) + 1
        results["impact_severities"][impactSeverity] = results["impact_severities"].get(impactSeverity, 0) + 1
        results["impact_consequences"][impactConsequence] = results["impact_consequences"].get(impactConsequence, 0) + 1
        results["code_fixes"][codeFix] = results["code_fixes"].get(codeFix, 0) + 1
        results["conceptual_fixes"][conceptualFix] = results["conceptual_fixes"].get(conceptualFix, 0) + 1
        results["system_dependencies"][systemDependency] = results["system_dependencies"].get(systemDependency, 0) + 1
        results["trigger_causes"][triggerCause] = results["trigger_causes"].get(triggerCause, 0) + 1
        results["trigger_reproductions"][triggerReproduction] = results["trigger_reproductions"].get(triggerReproduction, 0) + 1

        #results["system_dependencies_systems"][symptom] = results["system_dependencies_systems"].get(symptom, 0) + 1


    # Write aggregation
    with open(f"results/categorization_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        print(json.dumps(results, indent=4))

    print("Wrote aggregation for {} bugs.".format(totalCount))