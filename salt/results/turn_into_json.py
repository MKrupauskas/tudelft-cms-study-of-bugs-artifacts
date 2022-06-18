import json
from pathlib import Path

filename =["saltiteration1.txt", "saltiteration2.txt", "saltiteration3.txt", "saltiteration4.txt", "saltiteration5.txt"]

def createJSONs(filepaths, output) :
    alllines = []
    for fp in filepaths:
        p = Path(__file__).with_name(fp)
        with p.open('r') as file:
            lines = file.readlines()
            alllines.extend([line.rstrip() for line in lines])
    
    bugs = {}
    for line in alllines:
        bug = {}
        urls = line.split(",")
        bugname = "salt_" + urls[0].split("/")[-1]
        bug["configuration_management_system"] = "salt"
        bug["bug_report"] = urls[0]
        bug["bug_fix"] =  urls[1]

        bug["symptoms"] = ""

        bug["root_causes"] = ""

        bug["impact"] = {
            "severity": "", #low medium high
            "category": ""
        }

        bug["fixes"] =  {
            "code_fix": "",
            "conceptual_fix": ""
        }

        bug["system_dependency"] =  {
            "outcome": False,
            "found": []
        }

        bug["triggers"] =  {
            "errors": "",
            "characteristics": []
        }

        bug["notes"] = ""

        bugs[bugname] = bug
    
    w = Path(__file__).with_name(output)
    with w.open('w') as f:
        # indent=2 is not needed but makes the file human-readable 
        # # if the data is nested
        json.dump(bugs, f, indent=2) 





Categories = {
    "symptoms" : {
        "URB" : "Unexpected Runtime Behavior (URB)",
        "URBCIBE" : "Container Image Behavior Error (URBCIBE)", 
        "URBCDNP" : "Configuration does not parse as expected (URBCDNP)", 
        "URBTM" : "Target misconfiguration (URBTM)",
        "MR": "Misleading Report (MR)", 
        "UDBE" : "Unexpected Dependency Behavior Error (UDBE)",
        "PI" : "Performance issue (PI)",
        "CFNF" : "Feature/sub-feature non functional (module/non-core crash) (CFNF)", 
        "CEC" : "Execution crash (CEC)",
        "CCP" : "Configuration parsing crash (CCP)",
        "CERE" : "Environment Related Error (CERE)"
    },
    "root_causes" : {
        "EHRB" : "Error Handler & Reporter Bugs (EHRB)",
        "MC" : "Misconfiguration inside the codebase (MC)",
        "MCDV": "Misconfiguration of default values inside the codebase (MCDV)",
        "MCDP": "Misconfiguration of dependencies inside the codebase (MCDP)",
        "TMO": "Target machine operations (TMO)",
        "TMOFS": "Incorrect filesystem operations (TMOFS)",
        "TMOD": "Target machine / remote host has dependency issues (TMOD)",
        "TMOFTMF": "Fetch target machine variable/facts failure (TMOFTMF)",
        "TMOPI": "Parsing issue (TMOPI)",
        "TMOITE": "Instruction translation error / Abstraction layer error (TMOITE)",
        "CMO": "Controller machine operations (CMO)",
        "CMOEP": "Executor has problems (CMOEP)",
        "CMOCONP": "Connection has problems (CMOCONP)",
        "CMOPI": "Parsing issue (CMOPI)"
    },
    "impact" : {
        "Low" : "Low", 
        "Medium" : "Medium",
        "High" : "High",
        "SH" : "Security hazard (SH)",
        "PD" : "Performance degradation (PD)",
        "LOGRF" : "Logs reporting failure (LOGRF)",
        "TCF" : "Target configuration failed (TCF)",
        "TCFC" : "CMS operation crash (TCFC)",
        "TCIA" : "Target configuration inaccurate (TCIA)",
        "TCIN" : "Target configuration incomplete (TCIN)",
        "CUX" : "Confusing user experience (CUX)",
    },
    "fixes": {
        "CDDI" : "Change on data declaration/initialization (CDDI)",
        "CAS" : "Change on assignment statements (CAS)",
        "AC" : "Add class (AC)",
        "RC" : "Remove class (RC)",
        "CC" : "Change class (CC)",
        "AM" : "Add method (AM)",
        "RM" : "Remove method (RM)",
        "CM" : "Change method (CM)",
        "CLS" : "Change loop statements (CLS)",
        "CBS" : "Change branch statements (CBS)",
        "CRS" : "Change return statement (CRS)",
        "IM" : "Invoke a method (IM)",
        "FEC" : "Fix execution component (FEC)",
        "FPC" : "Fix parser component (FPC)",
        "FCC" : "Fix connectivity component (FCC)",
        "EEF" : "Expand execution feature (EEF)",
        "EPF" : "Expand parser feature (EPF)",
        "ECF" : "Expand connectivity feature (ECF)",
        "CDEP" : "Change dependencies (CDEP)",
        "CSS" : "Change system structure (CSS)",
        "CCONF" : "Change configuration (CCONF)",
        "DDM" : "Displaying a diagnostic message to the user (DDM)"
    },
    "triggers" : {
        "LE": "Logic Errors (LE)",
        "AE": "Algorithmic Errors (AE)",
        "CE": "Configuration Errors (CE)",
        "PE": "Programming Errors (PE)",
        "CLIC": "CLI commands (CLIC)",
        "CLICDMO": "Dependency module operation (CLICDMO)",
        "ENVS": "Environment setup (ENVS)",
        "FDEPU": "Faulty Dependency Usage (FDEPU)",
        "OSSE": "OS specific execution (OSSE)",
        "TC": "Test case (TC)",
        "SI": "Specific Invocation (SI)",
        "SITMCE": "Target machine control execution (SITMCE)",
        "SIIMI": "Internal module invocation (SIIMI)",
        "SICMI" : "Custom module invocation (SICMI)",
        "SITMRP" : "Target machine related parsing (SITMRP)",
        "SICRP" : "Config/Runbook Parsing (SICRP)"
    }
}


def insert_in_json(jsonfilename, resultsfilename):
    loaddict = {}
    # jsonfilename = "bug_analysis_results.json"
    p = Path(__file__).with_name(jsonfilename)
    with p.open('r') as f:
        loaddict = json.load(f)
    
    rl = []
    p = Path(__file__).with_name(resultsfilename)
    with p.open('r') as file:
        lines = file.readlines()
        rl = [line.rstrip() for line in lines]
    
    notinserted = []
    for rline in rl:
        res = list(map(lambda x: x.strip(), rline.split("|")))
        issue = "salt_" + res[0]
        if issue in loaddict:
            try: 
                loaddict[issue]["symptoms"] = Categories["symptoms"].get(res[1]) if res[1] in Categories["symptoms"] else ""
                # rc = res[2].split()
                loaddict[issue]["root_causes"] = Categories["root_causes"].get(res[2]) if res[2] in Categories["root_causes"] else ""
                # loaddict[issue]["root_causes"]["subcategory"]= res[2]
            
                impact = res[3].split()
                loaddict[issue]["impact"]["severity"] = Categories["impact"].get(impact[0]) if impact[0] in Categories["impact"] else ""
                loaddict[issue]["impact"]["category"] = Categories["impact"].get(impact[1]) if impact[1] in Categories["impact"] else ""
                # loaddict[issue]["impact"]["subcategory"] = impact[1]
            
                fixes = res[4].split()
                loaddict[issue]["fixes"]["code_fix"] = Categories["fixes"].get(fixes[0]) if fixes[0] in Categories["fixes"] else ""
                loaddict[issue]["fixes"]["conceptual_fix"] = Categories["fixes"].get(fixes[1]) if fixes[1] in Categories["fixes"] else ""
            
                system = res[5].split()
                loaddict[issue]["system_dependency"]["outcome"] = True if system[0]=="Y" else False
                if system[0] == "Y":
                    loaddict[issue]["system_dependency"]["found"].append(system[1])
            
                triggers = res[6].split()
                loaddict[issue]["triggers"]["errors"] = Categories["triggers"].get(triggers[0]) if triggers[0] in Categories["triggers"] else ""
                loaddict[issue]["triggers"]["characteristics"].extend(list(map(lambda x: Categories["triggers"].get(x), triggers[1:])))
            except Exception as e:
                notinserted.append(issue)
        else: 
            notinserted.append(issue)
    w = Path(__file__).with_name(jsonfilename)
    with w.open('w') as f:
        # indent=2 is not needed but makes the file human-readable 
        # # if the data is nested
        json.dump(loaddict, f, indent=2) 
    print(notinserted)



def aggregate(input, output):
    loaddict = {}
    # jsonfilename = "bug_analysis_results.json"
    p = Path(__file__).with_name(input)
    with p.open('r') as f:
        loaddict = json.load(f)

    statsdict = {
        "symptoms" : {
            "Unexpected Runtime Behavior (URB)" : 0,
            "Container Image Behavior Error (URBCIBE)" : 0, 
            "Configuration does not parse as expected (URBCDNP)" : 0, 
            "Target misconfiguration (URBTM)" : 0,
            "Misleading Report (MR)" : 0, 
            "Unexpected Dependency Behavior Error (UDBE)" : 0,
            "Performance issue (PI)" : 0,
            "Feature/sub-feature non functional (module/non-core crash) (CFNF)" : 0, 
            "Execution crash (CEC)" : 0,
            "Configuration parsing crash (CCP)" : 0,
            "Environment Related Error (CERE)" : 0
        },
        "root_causes" : {
            "Error Handler & Reporter Bugs (EHRB)": 0,
            "Misconfiguration inside the codebase (MC)": 0,
            "Misconfiguration of default values inside the codebase (MCDV)": 0,
            "Misconfiguration of dependencies inside the codebase (MCDP)": 0,
            "Target machine operations (TMO)": 0,
            "Incorrect filesystem operations (TMOFS)": 0,
            "Target machine / remote host has dependency issues (TMOD)": 0,
            "Fetch target machine variable/facts failure (TMOFTMF)": 0,
            "Parsing issue (TMOPI)": 0,
            "Instruction translation error / Abstraction layer error (TMOITE)": 0,
            "Controller machine operations (CMO)": 0,
            "Executor has problems (CMOEP)": 0,
            "Connection has problems (CMOCONP)": 0,
            "Parsing issue (CMOPI)": 0
        },
        "impact" : {
            "Low" :0, 
            "Medium" :0,
            "High" :0,
            "Security hazard (SH)" :0,
            "Performance degradation (PD)" :0,
            "Logs reporting failure (LOGRF)" :0,
            "Target configuration failed (TCF)" :0,
            "CMS operation crash (TCFC)" :0,
            "Target configuration inaccurate (TCIA)" :0,
            "Target configuration incomplete (TCIN)" :0,
            "Confusing user experience (CUX)" :0,
        },
        "fixes" : {
            "Change on data declaration/initialization (CDDI)": 0,
            "Change on assignment statements (CAS)": 0,
            "Add class (AC)": 0,
            "Remove class (RC)": 0,
            "Change class (CC)": 0,
            "Add method (AM)": 0,
            "Remove method (RM)": 0,
            "Change method (CM)": 0,
            "Change loop statements (CLS)": 0,
            "Change branch statements (CBS)": 0,
            "Change return statement (CRS)": 0,
            "Invoke a method (IM)": 0,
            "Fix execution component (FEC)": 0,
            "Fix parser component (FPC)": 0,
            "Fix connectivity component (FCC)": 0,
            "Expand execution feature (EEF)": 0,
            "Expand parser feature (EPF)": 0,
            "Expand connectivity feature (ECF)": 0,
            "Change dependencies (CDEP)": 0,
            "Change system structure (CSS)": 0,
            "Change configuration (CCONF)": 0,
            "Displaying a diagnostic message to the user (DDM)": 0
        },
        "system_dependency" : {
            True: 0,
            False: 0,
            "systems" : []
        },
        "triggers" : {
            "Logic Errors (LE)" : 0,
            "Algorithmic Errors (AE)" : 0,
            "Configuration Errors (CE)" : 0,
            "Programming Errors (PE)" : 0,
            "CLI commands (CLIC)" : 0,
            "Dependency module operation (CLICDMO)" : 0,
            "Environment setup (ENVS)" : 0,
            "Faulty Dependency Usage (FDEPU)" : 0,
            "OS specific execution (OSSE)" : 0,
            "Test case (TC)" : 0,
            "Specific Invocation (SI)" : 0,
            "Target machine control execution (SITMCE)" : 0,
            "Internal module invocation (SIIMI)" : 0,
            "Custom module invocation (SICMI)" : 0,
            "Target machine related parsing (SITMRP)" : 0,
            "Config/Runbook Parsing (SICRP)" : 0
        }
    }


    # notrep = []
    for key, value in loaddict.items():
        statsdict["symptoms"][value.get("symptoms")] += 1

        statsdict["root_causes"][value["root_causes"]] += 1

        statsdict["impact"][value.get("impact")["severity"]] += 1
        statsdict["impact"][value.get("impact")["category"]] += 1
        
        statsdict["fixes"][value.get("fixes")["code_fix"]] += 1

        if value.get("fixes")["conceptual_fix"] != "":
            statsdict["fixes"][value.get("fixes")["conceptual_fix"]] += 1

        statsdict["system_dependency"][value.get("system_dependency")["outcome"]] += 1
        statsdict["system_dependency"]["systems"].extend(value.get("system_dependency")["found"])

        if value.get("triggers").get("errors") != "":
            statsdict["triggers"][value.get("triggers")["errors"]] += 1
        for reproduce in value.get("triggers")["characteristics"]:
            statsdict["triggers"][reproduce] +=1
            # try: 
            #     statsdict["triggers"][reproduce] +=1
            # except Exception as e:
            #     notrep.append((key, reproduce))
    
    # print("this is notrep : {}".format(notrep))

    # statsdict["system_dependency"]["systems"] = list(set(statsdict["system_dependency"]["systems"]))
    w = Path(__file__).with_name(output)
    with w.open('w') as f:
        # indent=2 is not needed but makes the file human-readable 
        # # if the data is nested
        json.dump(statsdict, f, indent=2) 
    # print(notinserted)


def cross_category_info(inputfilename, outputfilename):
    loaddict = {}
    p = Path(__file__).with_name(inputfilename)
    with p.open('r') as f:
        loaddict = json.load(f)
    outputdict = {
        "symptom-root_cause":{},
        "root_cause-consequence":{},
        "impact-consequence":{},
        "fix-root_cause":{},
        "root_cause-symptom": {}
    }

    for key, value in loaddict.items():
        # print(value)
        symptom = value.get("symptoms", None)
        # print("this is the symptom {}".format(symptom))
        root_cause = value.get("root_causes", None)
        impact = value.get("impact").get("severity")
        consequence = value.get("impact").get("category")
        fix = value.get("fixes").get("conceptual_fix")
        
        if outputdict["symptom-root_cause"].get(symptom, None) is None:
            outputdict["symptom-root_cause"][symptom] = {}
        if outputdict["root_cause-consequence"].get(root_cause, None) is None:
            outputdict["root_cause-consequence"][root_cause] = {}
        if outputdict["impact-consequence"].get(impact, None) is None:
            outputdict["impact-consequence"][impact] = {}
        if outputdict["fix-root_cause"].get(fix, None) is None:
            outputdict["fix-root_cause"][fix] = {}
        if outputdict["root_cause-symptom"].get(root_cause, None) is None:
            outputdict["root_cause-symptom"][root_cause] = {}   



        if outputdict["symptom-root_cause"][symptom].get(root_cause, None) is None:
            outputdict["symptom-root_cause"][symptom][root_cause] = 0
        if outputdict["root_cause-consequence"][root_cause].get(consequence, None) is None:
            outputdict["root_cause-consequence"][root_cause][consequence] = 0
        if outputdict["impact-consequence"][impact].get(consequence, None) is None:
            outputdict["impact-consequence"][impact][consequence] = 0
        if outputdict["fix-root_cause"][fix].get(root_cause, None) is None:
            outputdict["fix-root_cause"][fix][root_cause] = 0
        if outputdict["root_cause-symptom"][root_cause].get(symptom, None) is None:
            outputdict["root_cause-symptom"][root_cause][symptom] = 0

        outputdict["symptom-root_cause"][symptom][root_cause] +=1
        outputdict["root_cause-consequence"][root_cause][consequence] +=1
        outputdict["impact-consequence"][impact][consequence] +=1
        outputdict["fix-root_cause"][fix][root_cause] +=1
        outputdict["root_cause-symptom"][root_cause][symptom] +=1

    w = Path(__file__).with_name(outputfilename)
    with w.open('w') as f:
        # indent=2 is not needed but makes the file human-readable 
        # # if the data is nested
        json.dump(outputdict, f, indent=2) 
    # print(notinserted)


createJSONs(filename, "bug_analysis_results.json")
insert_in_json("bug_analysis_results.json", "results.txt")
aggregate("bug_analysis_results.json", "salt_aggregated_results.json")
cross_category_info("bug_analysis_results.json", "cross_category_info.json")