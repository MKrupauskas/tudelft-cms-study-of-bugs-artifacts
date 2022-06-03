symptoms = {
    "ERE": {
        "name": "Environment Related Error",
        "description": "A bug involving this symptom manifests itself when the "
                       "CMS throws an error that is environment specific. "
                       "This concerns errors that are thrown, for example, on a Windows system rather than a Linux one."
    },
    "URB": {
        "name": "Unexpected Runtime Behavior",
        "description": "A bug related to this manifests itself when the CMS is executing its tasks."
    },
    "MR": {
        "name": "Misleading Report",
        "description": "Misleading reports appear when for a given program, "
                       "the CMS emits a false warning or a false error message."
    },
    "CIBE": {
        "name": "Container Image Behavior Error",
        "description": "This error is specific for container oriented systems. "
                       "It concerns bugs that manifest themselves in containerized applications "
                       "that are created using a CMS."
    },
    "UDBE": {
        "name": "Unexpected Dependency Behavior Error",
        "description": "A bug related to this shows up when there’s an error related to a dependency of the "
                       "CMS rather than the CMS itself."
    }
}

root_causes = {
    "TRB": {
        "name": "Type-related Bugs",
        "description": "This root cause relates to type errors thrown when the CMS executes its tasks"
    },
    "CSB": {
        "name": "Configuration Settings Bug",
        "description": "This relates to any wrong setup of methods from dependencies, "
                       "wrong dependency import, wrong dependency version."
    },
    "EFB": {
        "name": "Execution Flow Bugs",
        "description": "This relates to any faulty execution of statements in the code."
    },
    "CILB": {
        "name": "Container Image Life-cycle Bug",
        "description": "This relates to container oriented systems specifically and it concerns bugs that are "
                       "pertinent to an image expected life-cycle. "
                       "An image must behave as expected from its creation to its demotion."
    },
    "EHRB": {
        "name": "Error Handling & Reporting Bugs",
        "description": "A bug related to error handling & reporting is a bug where the CMS correctly identifies a "
                       "program error, but the implementation of the procedures for handling and reporting this error "
                       "does not produce the expected results."
    }
}

impact = {
    "Low": {
        "name": "Low",
        "description": "System works overall besides in specific edge cases."
    },
    "Medium": {
        "name": "Medium",
        "description": "System starts and works for the majority of cases but fails when performing one important task."
    },
    "High": {
        "name": "High",
        "description": "System won’t compile or start and it fails performing two or more important tasks."
    }
}

consequences = {
    "CNTC": {
        "name": "Container crash",
        "description": "A container created using the CMS crashes while performing its tasks."
    },
    "CNTCF": {
        "name": "Container creation failure",
        "description": "A container cannot be created using the CMS."
    },
    "CNTRF": {
        "name": "Container removal failure",
        "description": "A container cannot be removed using the CMS."
    },
    "SDF": {
        "name": "Service deployment failure",
        "description": "A service fails to be deployed."
    },
    "CNTFR": {
        "name": "Container forced restart",
        "description": "A container is forced to restart."
    },
    "CMSOF": {
        "name": "CMS operation failure",
        "description": "The CMS fails to perform an operation."
    },
    "NOF": {
        "name": "Network operations failure",
        "description": "A container created using the CMS crashes while performing its tasks."
    },
    "SH": {
        "name": "Security hazard",
        "description": "The bug introduces a security problem for the CMS."
    },
    "PD": {
        "name": "Performance degradation",
        "description": "The system performance is affected significantly."
    },
    "LOGRF": {
        "name": "Logs reporting failure",
        "description": "The system logging fails to provide information correctly."
    },
    "MMF": {
        "name": "Memory management failure",
        "description": "The system fails to manage memory properly."
    },
    "ENVSF": {
        "name": "Environment setup failure",
        "description": "The system fails to properly setup the environment in order to run seamlessly. "
    },
    "CMSC": {
        "name": "CMS crash",
        "description": "The CMS crashes while performing the operations."
    },
    "FSOF": {
        "name": "FileSystem operation failure",
        "description": "The file system operation fails to perform its task."
    },
    "POF": {
        "name": "Parsing operation failure",
        "description": "The parser fails to read an input correctly."
    }
}

fixes = {
    "CDDI": {
        "name": "Change on data declaration/initialization",
        "description": "Includes changes on data declaration, "
                       "for example a buggy 'int' type is converted to 'float' in the fix."
    },
    "CAS": {
        "name": "Change on assignment statements",
        "description": "Refers to bugs that led to a wrong value being assigned to a variable."
    },
    "AC": {
        "name": "Add class",
        "description": "A new object class is added."
    },
    "RC": {
        "name": "Remove class",
        "description": "An object class is removed."
    },
    "CC": {
        "name": "Change Class",
        "description": "An object class is modified in its name and/or inheritance."
    },
    "AM": {
        "name": "Add method",
        "description": "A new method is added."
    },
    "RM": {
        "name": "Remove method",
        "description": "A method is removed."
    },
    "CM": {
        "name": "Change method",
        "description": "A method is changes in its signature and/or inheritance."
    },
    "CLS": {
        "name": "Change loop statements",
        "description": "Includes mistakes in loops conditions, infinite loops or wrong loop termination."
    },
    "CBS": {
        "name": "Change branch statements",
        "description": "Refers to any changes to decision making statements such as 'if' and 'switch'."
    },
    "CRS": {
        "name": "Change return statement",
        "description": "Refers to changes to 'return' statements used to terminate a function and "
                       "return a specific value."
    },
    "CDEP": {
        "name": "Change dependencies",
        "description": "Includes fixes in the system dependencies (version upgrade, deletion, addition) and module "
                       "imports statements in the scripts."
    },
    "CSS": {
        "name": "Change system structure",
        "description": "Covers fixes that involved a refactoring of the project code. "
                       "This includes file and directories addition, removals, renaming and change of location."
    },
    "CCONF": {
        "name": "Change configuration",
        "description": "Covers fixes in the CMS configuration."
    }
}

system_dependent = {
    "true": {
        "name": "System dependent",
        "description": "The bug is system dependent."
    },
    "fasle": {
        "name": "System independent",
        "description": "There are similar bugs happening in other systems."
    }
}

triggers = {
    "LE": {
        "name": "Logic Errors",
        "description": "This relates to defects in logic, sequencing, or branching of a procedure."
    },
    "AE": {
        "name": "Algorithmic Errors",
        "description": "This error is identified when the implementation of an algorithm is wrong or "
                       "because a wrong algorithm was used."
    },
    "CE": {
        "name": "Configuration Errors",
        "description": "A configuration error is one of the major causes of a system failure."
    },
    "PE": {
        "name": "Programming Errors",
        "description": "This relates to declarations of a variable with an incorrect data type, out-of-bounds "
                       "array accesses, accesses to null references, and unchecked exceptions."
    }
}

characteristics = {
    "CLIC": {
        "name": "CLI commands",
        "description": "The bug can be triggered through CLI commands. The test contains CLI calls."
    },
    "ENVS": {
        "name": "Environment setup",
        "description": "The bug can be reproduced by specific setup in the service environment. "
                       "The test includes the setup of additional environment variables."
    },
    "DEPIN": {
        "name": "Dependency initialization",
        "description": "The bug can be reproduced by initializing a dependency in a faulty way."
    },
    "OSSE": {
        "name": "OS specific execution",
        "description": "The bug can be reproduced by running the CMS operations in the specific OS it occurred."
    },
    "SLF": {
        "name": "Standard Language Features",
        "description": "The test case contains standard language features."
    },
    "VSE": {
        "name": "Version specific execution",
        "description": "The bug can be reproduced by running the operation in the specific "
                       "CMS version it occurred from."
    },
    "NCO": {
        "name": "Network connections operations",
        "description": "The bug can be reproduced by running network connections operations."
    }
}
