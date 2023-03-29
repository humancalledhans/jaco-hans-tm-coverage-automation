# Setup

Python version used is 3.10.

Reproduce the virtual enviornment using the following commands (or similar):

1. Enter project directory

    `cd jaco-hans-tm-coverage-automation`

2. Create a virtual environment

    `py -3 -m venv tm-coverage-venv`

3. Activate it

    `source tm-coverage-venv/Scripts/activatee`

4. Run the pip install

    `pip install -r requirements.txt`

Connect the DB GUI such as MySQL Workbench with the following settings:

```
Connection Method: TCP/IP
Hostname: 103.6.198.226
Port: 3306
Username: oursspc1_db_extuser
Password: Ask for this
```

# Running

To run the development environment:

1. Connect the database
2. Activate the venv using the code editor

    `source tm-coverage-venv/Scripts/activate`

3. Run `thread_asgn.py` using the code editor or by running

    `py -3 thread_asgn.py`
