# Steps

## Creating Virtual Environment:

- Open the workspace folder
- type **`py -3 -m venv venv`** in the terminal
- press **`CTRL + SHIFT + P`** in the vscode and search for **`python: select interpreter`**
- Select **`Enter Interpreter Path`**
- Paste this **`.\venv\Scripts\python.exe`** and hit enter

## Activating Virtual Environment:

Paste this in the terminal:

### `venv\Scripts\activate.bat`

## Intsalling Dependencies:

Postgres SQL:
[https://www.enterprisedb.com/downloads/postgres-postgresql-downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
Download Correct version for your operating system.

after that paste this in the terminal:

## `pip install -r requirements.txt`

this will install all the requiremnts for the project.

## Starting the server

To start the server run **start.sh** from the terminal.
or if that doesnt work paste this in the terminal:

## `uvicorn app.main:app --reload --host 0.0.0.0`
