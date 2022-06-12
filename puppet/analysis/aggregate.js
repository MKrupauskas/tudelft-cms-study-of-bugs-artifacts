import fs from 'fs/promises'

const iteration1 = {
	"configuration_management_system": "puppet",
	"global": {
		"symptoms": {
			"Unexpected Runtime Behavior": 14,
			"Misleading Report": 7,
			"Environment Related Error": 1,
			"Unexpected Dependency Behavior Error": 1
		},
		"root_causes": {
			"Execution Flow Bugs": 10,
			"Configuration Settings Bug": 4,
			"Error Handling & Reporting Bugs": 6,
			"Type-related Bugs": 3
		},
		"impact": {
			"Low": {
				"Memory management failure": 1,
				"CMS operation failure": 1,
				"Environment setup failure": 1,
				"Logs reporting failure": 2,
				"CMS crash": 1
			},
			"Medium": {
				"Network operations failure": 1,
				"Logs reporting failure": 2,
				"CMS operation failure": 5,
				"FileSystem operation failure": 2,
				"Environment setup failure": 1,
				"Parsing operation failure": 1
			},
			"High": {
				"Logs reporting failure": 3,
				"CMS operation failure": 1,
				"Network operations failure": 1
			}
		},
		"fixes": {
			"Change on assignment statements": 9,
			"Add method": 6,
			"Change branch statements": 7,
			"Change system structure": 3,
			"Change dependencies": 1,
			"Change return statement": 1,
			"Change method": 2
		},
		"system_dependency": {
			"dependent": 8,
			"independent": 15,
			"systems": {
				"linux/debian": 1,
				"macos": 2,
				"windows": 5,
				"linux/ubuntu16.04": 1,
				"linux/centos7": 1,
				"linux/centos6": 1
			}
		},
		"triggers": {
			"errors": {
				"Logic Errors": 7,
				"Programming Errors": 9,
				"Configuration Errors": 5,
				"Algorithmic Errors": 2
			},
			"characteristics": {
				"Environment setup": 2,
				"Standard Language Features": 11,
				"CLI commands": 10,
				"Dependency initialization": 2,
				"OS specific execution": 3,
				"Version specific execution": 1,
				"Network connections operations": 1
			}
		}
	}
}

const iteration2 = {
	"configuration_management_system": "puppet",
	"global": {
		"symptoms": {
			"Misleading Report": 5,
			"Unexpected Runtime Behavior": 11,
			"Unexpected Dependency Behavior Error": 2,
			"Environment Related Error": 2
		},
		"root_causes": {
			"Error Handling & Reporting Bugs": 5,
			"Execution Flow Bugs": 9,
			"Type-related Bugs": 3,
			"Configuration Settings Bug": 3
		},
		"impact": {
			"Low": {
				"Logs reporting failure": 1,
				"Security hazard": 1,
				"CMS operation failure": 2,
				"FileSystem operation failure": 1
			},
			"Medium": {
				"CMS operation failure": 5,
				"FileSystem operation failure": 2,
				"Network operations failure": 1,
				"Environment setup failure": 4,
				"Logs reporting failure": 3,
				"Memory management failure": 1
			},
			"High": {
				"CMS crash": 3,
				"CMS operation failure": 2,
				"Parsing operation failure": 1,
				"Environment setup failure": 1,
				"Network operations failure": 1,
				"Logs reporting failure": 1,
				"Memory management failure": 1,
				"FileSystem operation failure": 1
			}
		},
		"fixes": {
			"Change branch statements": 9,
			"Add method": 3,
			"Change on assignment statements": 9,
			"Change system structure": 4,
			"Change on data declaration/initialization": 4,
			"Change configuration": 4,
			"Change method": 2
		},
		"system_dependency": {
			"dependent": 4,
			"independent": 16,
			"systems": {
				"linux/centos7": 3,
				"windows": 3,
				"linux": 1,
				"ubuntu16.04": 1,
				"linux/centos6": 1
			}
		},
		"triggers": {
			"errors": {
				"Logic Errors": 7,
				"Algorithmic Errors": 4,
				"Programming Errors": 6,
				"Configuration Errors": 8
			},
			"characteristics": {
				"Standard Language Features": 14,
				"CLI commands": 13,
				"Network connections operations": 3,
				"Dependency initialization": 1,
				"Version specific execution": 4,
				"OS specific execution": 3,
				"Environment setup": 2
			}
		}
	}
}

const iteration3 = {
	"configuration_management_system": "puppet",
	"global": {
		"symptoms": {
			"Environment Related Error": 5,
			"Unexpected Runtime Behavior": 10,
			"Unexpected Dependency Behavior Error": 2,
			"Misleading Report": 3
		},
		"root_causes": {
			"Configuration Settings Bug": 6,
			"Execution Flow Bugs": 9,
			"Type-related Bugs": 2,
			"Error Handling & Reporting Bugs": 3
		},
		"impact": {
			"Low": {
				"Logs reporting failure": 2
			},
			"Medium": {
				"CMS operation failure": 7,
				"Logs reporting failure": 2,
				"Environment setup failure": 3,
				"Security hazard": 1,
				"Network operations failure": 1,
				"FileSystem operation failure": 2
			},
			"High": {
				"CMS crash": 4,
				"FileSystem operation failure": 3,
				"Network operations failure": 3,
				"Security hazard": 2,
				"CMS operation failure": 2,
				"Environment setup failure": 1
			}
		},
		"fixes": {
			"Add method": 4,
			"Change dependencies": 1,
			"Change configuration": 4,
			"Change system structure": 6,
			"Change return statement": 2,
			"Change branch statements": 7,
			"Change on data declaration/initialization": 1,
			"Change on assignment statements": 5,
			"Change method": 1
		},
		"system_dependency": {
			"dependent": 5,
			"independent": 15,
			"systems": {
				"linux/fedora22": 1,
				"linux/solaris10": 1,
				"linux/solaris": 1,
				"linux/redhat6": 1,
				"linux/redhat7": 1,
				"windows": 2
			}
		},
		"triggers": {
			"errors": {
				"Configuration Errors": 7,
				"Programming Errors": 5,
				"Algorithmic Errors": 6,
				"Logic Errors": 3
			},
			"characteristics": {
				"OS specific execution": 6,
				"Version specific execution": 8,
				"CLI commands": 12,
				"Environment setup": 3,
				"Standard Language Features": 10,
				"Network connections operations": 4
			}
		}
	}
}

function sumValues(accumulator, obj) {
	for (const [key, value] of Object.entries(obj)) {
		if (typeof value === 'object') {
			accumulator[key] = accumulator[key] ?? {}
			sumValues(accumulator[key], value)
			continue
		}
		if (typeof value === 'string') {
			accumulator[key] = value
			continue
		}
		accumulator[key] = (accumulator[key] ?? 0) + (value ?? 0)
	}
}

let aggregated = {}

sumValues(aggregated, iteration2)
sumValues(aggregated, iteration1)
sumValues(aggregated, iteration3)

fs.writeFile("aggregated.json", JSON.stringify(aggregated, null, 2))