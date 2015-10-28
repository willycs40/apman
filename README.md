## ApMan (Analytics Package Manager)

[![Build Status](https://travis-ci.org/willycs40/apman.svg?branch=master)](https://travis-ci.org/willycs40/apman)

### Description
ApMan is a python wrapper which can be used to call other python applications (e.g. analytics packages like a customer churn model) in a standardised, robust, and logged manner - and email notifications in the event of an issue. 

When ApMan is used to run a package:
 * The initiation of the package is recorded to a central log
 * The package is run in a seperate process, started by ApMan
 * Typically, inside this process, a package dedicated python virtual environment is activated, and then the package work is done.
 * If the package goes over a pre-configured package timeout, the process is killed, and the timeout result is recorded to the central log.
 * If the package causes an unhandled exception, the process is killed, and the exception result recorded to the central log.
 * On successful completion, the success result is recorded to the central log.
 * In all cases, all logging (stdout/stderr) from the package is also recorded to the central log.
 * Finally, in the event of timeout or exception (or on success, if so configured) ApMan emails the configured recipients.

### Creating a package
 * Packages are constructed as Python applications, with an additional 'apman' configuration file. 
 * It is also expected and supported that each package should have a requirements.txt file which can be used to build a dedicated virtual environment. The apman config is then updated to direct ApMan to use this environment on execution.

### ApMan Config file
The config file should be a json dictionary such as the following:

{
    "id":"test",
    "description":"this is a test package",
    "timeout": 4,
    "command": "venv/Scripts/python script.py",
    "notify-success": True
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

* Once installed, ApMan can be called using the 'apman_run.py' command line tool.
* To run a package call 'apman_run.py config_file'.
