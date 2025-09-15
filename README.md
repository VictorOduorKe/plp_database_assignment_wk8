# plp_database_assignment_wk8
# clone the repository
```bash
git clone https://github.com/VictorOduorKe/plp_database_assignment_wk8.git
cd plp_database_assignment_wk8
```
To run the program create virtual environment and install the following dependancies 
```bash
python3 -m venv venv
source venv/bin/activate
pip install mysql-connector-python
pip install dotenv
```
or run this in terminal

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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