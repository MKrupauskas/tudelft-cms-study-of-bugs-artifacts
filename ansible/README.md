# CSE3000 - A study of bugs in the Ansible configuration management system

This project contains the code for gathering, processing, and analysing bug data of the Ansible configuration management system.

The data fetching is implemented using Perceval. The processing and serialization is done in Python, and analysis is done in Python as well.



## Setup

1. Set up Python3 on your system: https://docs.python.org/3/using/index.html 
2. Run `./setup.sh`

## Fetching Bug Data

Fetching data is split into two sections, depending on which data you require.

### Fetching Issues

To fetch all issues from the Ansible Github project, run:

```
$ ./pullRawIssues.sh
```

This will produce a timestamped file in the `raw/` folder for you to explore.

### Fetching Pull Requests

To fetch all pull requests from the Ansible Github project, run:

```
$ ./pullRawPRs.sh
```

### Fetching All Data

To get all data, you can run this:

```
$ ./pullRawAll.sh
```

## Pre-processing Data

To pre-process the raw data to be readable by the analysis tools, use:

```
$ python3 processing/convertOutput.py raw/$RAW_FILENAME
```

This will produce an output JSON file in the same directory with the appendix `-out`.

## Analyzing Data

To run analysis on the data, use these tools:

### Producing a Summary

To create a summary from the pre-processed data, use:

```
$ python3 analysis/extractSummary.py raw/$PROCESSED_FILENAME
```

This will give an overview analysis of the bugs in the raw data.