import json
import os
import sys
import csv




with open("results/categorized.tsv") as categorizedFile:
    categorizedBugs = csv.reader(categorizedFile, delimiter="\t", quotechar='"')

    # For aggregating amounts
    results = dict()


    for categorizedBug in categorizedBugs:
        if len(row) == 0:
            print("Skipping iteration boundary")
            continue
        print(row)

        for bugUrl, fixUrl, symptomCode, rootCauseCode, impactSeverity, impactConsequence, codeFix, conceptualFix, systemDependency, triggerCause, triggerReproduction, operatingSystem in row:
            print(bugUrl, fixUrl, symptomCode, rootCauseCode, impactSeverity, impactConsequence, codeFix, conceptualFix, systemDependency, triggerCause, triggerReproduction, operatingSystem)
        


    # Write aggregation
    with open(f"results/categorization_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        print(json.dumps(results, indent=4))




