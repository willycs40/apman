import subprocess
import threading
import sys
import json

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

    # Get config script location
    try:
        config_path = sys.argv[1]
    except:
        print("master.py expects the path to a configuration script as the first argument")
        raise
    
    # Load config object
    try:
        with open(config_path,'r') as file:
            config = json.load(file)
    except:
        print("Error loading configuration script. Check path and that script is valid json")
        raise
    
    # Load config parameters
    try:
        package_name = config['name']
        script_path = config['script']
        script_parameters = config['parameters']
        timeout = config['timeout']
    except:
        print("Error loading config settings. Please check config file is complete.")   
        raise

    # Begin script execution
    print("Starting package: {}".format(package_name))
    
    # Call the script thread
    script_thread = RunScript(['python', script_path, str(script_parameters)], timeout)
    script_thread.Run()
    
    print("Packaged execution finished.")
    
    if script_thread.script_timed_out == True:
        print('Script timed out')
    elif script_thread.script_exceptioned == True:
        print("Script raised an exception")
    else:
        print("Script finished successfully")
        
    print("Output:",script_thread.out)
    print("Errors:",script_thread.err)
        
if __name__ == '__main__':
    main()
