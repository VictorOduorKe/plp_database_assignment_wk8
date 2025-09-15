# plp_database_assignment_wk8

To run the program create virtual environment and install the following dependancies
```bash
python3 -m venv venv
source venv/bin/activate
pip install mysql-connector-python
pip install dotenv
```
# create .env file in the root directory with the following attributes and the values
```bash
HOST=localhost
USER=root
PASSWORD=Your_password
DATABASE=school_mgt
PORT=3306
```

Login to worknbench and run the following command
```bash
CREATE DATABASE IF NOT EXISTS school_mgt;
```
to run the project in terminal according to the python version you are using
```bash
python3 test.py
```