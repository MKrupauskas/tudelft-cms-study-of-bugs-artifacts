# CSE3000 Research Project: "Studying bugs in the Salt Configuration Management System"

This repository contains scripts used in the paper "Studying bugs in the Salt Configuration Management System"


The purpose of this repository is to make it possible to reproduce the bug data gathered for the paper: "Studying bugs in the Salt Configuration Management System". Moreover to be transparent in the methods used to collect the bug data 

<!-- #Table of Contents -->

<!-- #TODO (Overview of directories and files) :explain the folders in the repository -->

# Requirements
* A Unix-like operating system (tested on Ubuntu).
* Python version **3.8+**.

# Getting started 
How to clone this repository
To get the bug data collected for this project and the bug collection scripts, you can clone this repository. Afterwards enter the directory, where you are able to optionally run the scripts
```bash
git clone https://github.com/BryanHeee/cse3000bugstudycode.git ~/cse3000bugstudycode
cd ~/cse3000bugstudycode
```

# Setting it up 
The instructions in this step is optional. Follow the instructions below if you want to run the scripts for collecting the bugs. 

In the root directory of the [this repository you've cloned](#Getting-started) open a terminal and install the following `apt` packages:
```bash
apt install curl jq git diffstat cloc
```

In the root directory create a python virtual environment and install the packages necessary for running the scripts:
```bash
virtualenv .env
source .env/bin/activate
pip install requests mysql-connector-python
```

## Running scripts to collect bug data

To fetch the bugs from the [Salt repository](https://github.com/saltstack/salt), run `fetch.sh`.  
```bash
./fetch.sh <name of the directory where you want bug data to be installed> $GHTOKEN
```
`$GHTOKEN` is a Github access token necessary for running `fetch.sh`. You can get instructions on how to generate your own Github access token [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). Afterwards, you can set it as an environment variable by executing the following in a terminal at the root directory:  
```bash
export GHTOKEN=<your own Github access token>
```

`fetch.sh` is a script which executes:
- `fetch_bugs.py` to fetch bugs from the [Salt repository](https://github.com/saltstack/salt), 
- `clone.sh` to clone the [Salt repository](https://github.com/saltstack/salt) and 
- `find_fixes.sh` to filter out the bugs without an explicit fix

## Storing bug data in a MySQL database
This step is optional. Execute the instructions below if you want to store the bug data in a MySQL database. Otherwise the bug data collected for this research project can be found in the `saltwithfixes.txt` file which resides in the root of the directory. 

First, install MySQL, if you do not have it installed yet. You can install MySQL Workbench (recommended) [here](https://dev.mysql.com/downloads/workbench/).

Once installed create a database by executing the SQL statements found in `bugdataschema.sql` which resides in the 'mysqlDB' subdirectory.

The next step is to set the environment variables, open up the terminal in the root directory and execute the following:

```bash
export HOST=<where your database is hosted e.g. localhost>
export DATABASE=<Name of the database, should be `cse3000saltbugdb` if `bugdataschema.sql` was executed>
export USER=<your MySQL username>
export PASSWORD=<your MySQL password>
export BUGSFILE=<name of the file containing bugs and fixes e.g. `saltfixes.txt` which is the output of `fetch.sh`>
```

Finally run the command below to store the bugs in the database:
```bash
python3 insert_in_db.py $HOST $DATABASE $USER $PASSWORD $BUGSFILE $GHTOKEN
```

