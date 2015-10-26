import subprocess
import threading
from datetime import datetime

class ScriptRunner(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout
        self.script_timed_out = False
        self.script_exceptioned = False
        self.out = ''
        self.err = ''
        self.start_timestamp = None
        self.end_timestamp = None
            
    def run(self):
        self.p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (self.out, self.err) = self.p.communicate()
        self.p.wait()
        if self.p.returncode > 0:
            self.script_exceptioned = True

    def run_script(self):
        # self.start causes self.run to be called (in a different process). 
        # self.join passes when the execution finishes, or after the timeout
        self.start_timestamp = datetime.now()
        self.start()
        self.join(self.timeout)

        # if the thread is still alive at this point, then the timeout must have hit.
        # terminate kills the thread, use join to wait until that's happened, and then log the timeout
        if self.is_alive():
            self.p.terminate()    
            self.join()
            self.script_timed_out = True

        self.end_timestamp = datetime.now()