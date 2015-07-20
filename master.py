import subprocess
import threading
import sys
import json
import os
import shlex

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class RunScript(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout
        self.script_timed_out = False
        self.script_exceptioned = False
        self.out = ''
        self.err = ''
            
    def run(self):
        self.p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (self.out, self.err) = self.p.communicate()
        self.p.wait()
        if self.p.returncode > 0:
            self.script_exceptioned = True

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            self.join()
            self.script_timed_out = True

def main():

    # Print Diagnostic Information
    print("Running ApMan with python executable location: {}".format(sys.prefix))

    print("Loading package...")
    print('    Reading package configuration...')
    # Get package configuration file location
    try:
        package_path = sys.argv[1]
    except:
        print("Program expects the path to a configuration script as the first argument")
        raise
        
    # Load package configuration file
    try:
        with open(package_path,'r') as file:
            package = json.load(file)
    except:
        print("Error loading the package configuration script. Check the supplied path and verify is valid json (could use http://jsonlint.com/).")
        raise
    
    # Check all required parameters are present in the configuration
    required_parameters = ['id','name','command', 'timeout']
    missing_parameters = []
    for param in required_parameters:
        if param not in package:
            missing_parameters.append(param)
    if len(missing_parameters)>0:
        raise Exception("Parameters {} missing from package configuration".format(str(missing_parameters)))
    
    # Get config path and work from there...
    package['absolute_path'] = os.path.abspath(package_path)
    package['directory'] = os.path.dirname(package['absolute_path'])
    
    print("    Switching to package directory... {}".format(package['directory']))   
    
    # Work from package directory
    with cd(package['directory']):

        # Begin script execution
        print("    Starting package ({}), with time-out ({} seconds), command ({})".format(package['id'],package['timeout'],package['command']))
        print("    Running..."),
        
        # Split the package command, add on the parameters, if they exist, then kick off the thread
        command = shlex.split(package['command'])
        if 'parameters' in package:
            command.append(str(package['parameters']))
        script_thread = RunScript(command, package['timeout'])
        script_thread.Run()
        
        print("done")

        if script_thread.script_timed_out == True:
            print('    Script timed out')
        elif script_thread.script_exceptioned == True:
            print("    Script raised an exception")
        else:
            print("    Script finished successfully")
            
        print("Output:",script_thread.out)
        print("Errors:",script_thread.err)
        
if __name__ == '__main__':
    main()
