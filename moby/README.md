# CSE3000-RP-Report
CSE3000 Research Project data analysis script.

#### Requirements

| Name | Link |
|---|---|
| Python 3.7+ | [Pyhton Download and install](https://www.python.org/downloads/) |
| PyCharm IDE (recommended) | [PyCharm installation](https://www.jetbrains.com/pycharm/download/) |
| MySQL | [MySQL download and install](https://www.mysql.com/downloads/) |
| MySQL WorkBench (recommended) | [MySQL WorkBench download and install](https://dev.mysql.com/downloads/workbench/) |

## Create the bugs database

### 1. Setup the Database

To use the scripts we first need to setup the database. You can use the script **"db/step1_create_db_tables.sql"** and import it directly into your MySQL. 

### 2. Run the scripts

#### Clone

Clone this repo to your local machine using 
```
https://github.com/MattiaBonfanti-CS/CSE3000-RP-Report.git
```

#### Create Virtual Environment (venv)
Move to the project folder and run in your terminal:
```
# Create virtualenv, make sure to use python3
$ virtualenv -p python3 venv
# Activate venv
$ source venv/bin/activate
```
Alternatively:
* Open the project with PyCharm (either Pro or CE)  or your favorite Python IDE
* Select python3 as project interpreter

#### Setup local environment variables
Create a ".env" file in the root folder of the project with the following variables:
```
GITHUB_REPO=owner/name
GITHUB_TOKEN=your_token
MYSQL_HOST=your_mysql_host_address
MYSQL_DB=cse3000
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
```

#### Install Requirements
Move to  the project folder and run in your terminal:
```
pip install -r requirements.txt
```

#### Run
Move to the "data" folder in the project and run in your terminal:
```
# Find and store issues to the database
python main.py
# or
python main.py issue

# Find and store pull_requests to the database
python main.py pull_request
```  

### 3. Streamline results and clean data

- After the information about issues and pull requests is stored in the respective tables, we need to merge the results in order to create a centralized record of bugs with a fix. This step can be accomplished by running the script **"db/step2_join_results.sql"** in your MySQL.  
- The final step of the data gathering process is the deletion of the false positives in the final bugs table. Running the script **"db/step3_remove_false_positives.sql"** will remove the following:
  - False positives with no files changes.
  - Entries without descriptions as they won’t offer much information for our analysis to be performed properly.
  - Entries without labels as they won’t offer much information for our analysis to be performed properly.

## Perform bugs analysis

## Notes  
- You should keep the .gitignore updated file to make sure that any OS-specific and IDE-specific files do not get pushed to the repo (e.g. .idea).  
