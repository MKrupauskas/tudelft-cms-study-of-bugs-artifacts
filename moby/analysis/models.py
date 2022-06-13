symptoms = {
    "URB": "Unexpected Runtime Behavior",
    "URBCIBE": "Container Image Behavior Error",
    "URBCDNP": "Configuration does not parse as expected",
    "URBTM": "Target misconfiguration",
    "MR": "Misleading Report",
    "UDBE": "Unexpected Dependency Behavior Error",
    "PI": "Performance issue",
    "CFNF": "Feature/sub-feature non functional (module/non-core crash)",
    "CEC": "Execution crash",
    "CCP": "Configuration parsing crash",
    "CERE": "Environment Related Error"
}

root_causes = {
    "CILB": "Container Image Life-cycle Bug",
    "EHRB": "Error Handling & Reporting Bugs",
    "TRB": "Type-related Bugs",
    "MC": "Misconfiguration inside the codebase",
    "MCDV": "Misconfiguration of default values inside the codebase",
    "MCDP": "Misconfiguration of dependencies inside the codebase",
    "TMO": "Target machine operations",
    "TMOFS": "Target machine incorrect filesystem operations",
    "TMOD": "Target machine / remote host has dependency issues",
    "TMOFTMF": "Fetch target machine variable/facts failure",
    "TMOPI": "Target machine parsing issue",
    "TMOITE": "Target machine instruction translation error / Abstraction layer error",
    "CMO": "Controller machine operations",
    "CMOEP": "Controller machine executor has problems",
    "CMOCONP": "Controller machine connection has problems",
    "CMOPI": "Controller machine parsing issue"
}

impact = {
    "Low": "Low",
    "Medium": "Medium",
    "High": "High"
}

consequences = {
    "CNTOC": "Container operation crash",
    "SH": "Security hazard",
    "PD": "Performance degradation",
    "LOGRF": "Logs reporting failure",
    "TCF": "Target configuration failed",
    "TCFC": "Target CMS operation crash",
    "TCIA": "Target configuration inaccurate",
    "TCIN": "Target configuration incomplete",
    "CUX": "Confusing user experience"
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
    "FEC": "Fix execution component",
    "FPC": "Fix parser component",
    "FCC": "Fix connectivity component",
    "EEF": "Expand execution feature",
    "EPF": "Expand parser feature",
    "ECF": "Expand connectivity feature",
    "CDEP": "Change dependencies",
    "CSS": "Change system structure",
    "CCONF": "Change configuration",
    "DDM": "Displaying a diagnostic message to the user"
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
    "CLICCC": "Container command",
    "CLICDMO": "Dependency module operation",
    "ENVS": "Environment setup",
    "FDEPU": "Faulty Dependency Usage",
    "OSSE": "OS specific execution",
    "TC": "Test case",
    "SI": "Specific Invocation",
    "SITMCE": "Target machine control execution",
    "SIIMI": "Internal module invocation",
    "SICMI": "Custom module invocation",
    "SITMRP": "Target machine related parsing",
    "SICRP": "Config/Runbook Parsing"
}
