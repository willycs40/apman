# ApMan
## Analytics Package Manager

### Introduction
ApMan is a python wrapper which can be used to call scripts (i.e. analytics such as customer churn, next best product) in a standardised and robust manner. 

Packages are constructed as a folder and configuration file containing all commands, parameters and virtual environments needed for the analytic. ApMan is then used to run these packages robustly, catching any handled or unhandled exceptions, as well as the package result and stout/stedd, and storing all this information in a central log.

### Creating a package

* Create a folder, named after the analytic e.g. churn (preferably within the 'packages' folder)

cd packages
mkdir churn

* Within this Create a virtual environment folder (venv) within this folder.
	virtualenv venv
* Activate this virtual environment, and install any necessary libraries.
	venv/Scripts/activate.bat
	pip install nltk
* Create a requirements file to store a record of any libraries installed.
	pip freeze > requirements.txt
* Create the analytic script:
	notepad script.py
* Create the package configuration file.
	notepad config

The config file should be a json dictionary such as the following:

{
    "id":"test",
    "description":"this is a test package",
    "timeout": 4,
    "command": "venv/Scripts/python script.py",
    "parameters": {"name":"Will", "age":28}
}

Parameter | Required | Description
----------|---------|-------------------------------
id | Yes | This is the package name, usually an acronym, and should match the package folder name
description | Yes | A fuller description of the package
timeout | Yes | The timeout, in seconds, of the package. ApMan will kill the package if it exceeds this time.
command | Yes | The command the package should run, relative to the configuration file path.
parameters | No | A json-formatted dictionary of parameters to pass to the command. Seperate to allow updating with dynamic parameters (e.g. timestamps) by ApMan.

### Running a package

* Packages can be run outside of apman simply by cd'ing to the config file directory, and running the command given in the configuration file 'command' parameter, followed optionally by the dictionary given in the 'parameters' parameter, surrounded by single quotes. e.g.
	venv/Script/python script.py '{"name":"Will","age":28}'

* One can test run packages using ApMan, by calling apman.py with the package configuration script as the first argument:
	python apman.py packages/test/config
* ApMan itself should run in a virtual environment, therefore the following syntax maybe preferable:
	../venv/Scripts/python apman.py packages/test/config