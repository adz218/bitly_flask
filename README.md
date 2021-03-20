## Installation
This project requires Python 3 with the module `venv` installed.

```
$ cd flask_app
$ python3 -m venv venv

On Windows:
$ py -3 -m venv venv

Install requirements:
pip install -r requirements.txt
```

## Start local server
Simply run 
```
./app.py
```
NOTE: you will have to change shebang path to python.exe on line 1 of app.py
`http://localhost:5000` should direct you to the landing page


## Usage
Please use `curl` to access the specification endpoint
```
curl -H "Authorization: <token>" http://localhost:5000/v4/user/average
```
