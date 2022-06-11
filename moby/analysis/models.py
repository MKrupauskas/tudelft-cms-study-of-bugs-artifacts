symptoms = {
    "ERE": "Environment Related Error",
    "URB": "Unexpected Runtime Behavior",
    "MR": "Misleading Report",
    "CIBE": "Container Image Behavior Error",
    "UDBE": "Unexpected Dependency Behavior Error"
}

root_causes = {
    "TRB": "Type-related Bugs",
    "CSB": "Configuration Settings Bug",
    "EFB": "Execution Flow Bugs",
    "CILB": "Container Image Life-cycle Bug",
    "EHRB": "Error Handling & Reporting Bugs",
    "TMOFS": "Incorrect filesystem operations"
}

impact = {
    "Low": "Low",
    "Medium": "Medium",
    "High": "High"
}

consequences = {
    "CNTC": "Container crash",
    "CNTCF": "Container creation failure",
    "CNTRF": "Container removal failure",
    "SDF": "Service deployment failure",
    "CNTFR": "Container forced restart",
    "CMSOF": "CMS operation failure",
    "NOF": "Network operations failure",
    "SH": "Security hazard",
    "PD": "Performance degradation",
    "LOGRF": "Logs reporting failure",
    "MMF": "Memory management failure",
    "ENVSF": "Environment setup failure",
    "CMSC": "CMS crash",
    "FSOF": "FileSystem operation failure",
    "POF": "Parsing operation failure"
}

fixes = {
    "CDDI": "Change on data declaration/initialization",
    "CAS": "Change on assignment statements",
    "AC": "Add class",
    "RC": "Remove class",
    "CC": "Change Class",
    "AM": "Add method",
    "RM": "Remove method",
    "CM": "Change method",
    "CLS": "Change loop statements",
    "CBS": "Change branch statements",
    "CRS": "Change return statement",
    "CDEP": "Change dependencies",
    "CSS": "Change system structure",
    "CCONF": "Change configuration"
}

system_dependent = {
    "true": "System dependent",
    "fasle": "System independent"
}

triggers = {
    "LE": "Logic Errors",
    "AE": "Algorithmic Errors",
    "CE": "Configuration Errors",
    "PE": "Programming Errors"
}

characteristics = {
    "CLIC": "CLI commands",
    "ENVS": "Environment setup",
    "DEPIN": "Dependency initialization",
    "OSSE": "OS specific execution",
    "SLF": "Standard Language Features",
    "VSE": "Version specific execution",
    "NCO": "Network connections operations"
}
