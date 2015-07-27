import time
import sys 
import ast

SCRIPT_PARAMETERS = {}

def main():
    print(sys.prefix)
    print("hello " + SCRIPT_PARAMETERS['name'])
    sys.stdout.write("out test")
    print >> sys.stderr, ("err test")
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(1)
    print("there")
    print(SCRIPT_PARAMETERS['name'])
    print(SCRIPT_PARAMETERS['age']) 

if __name__ == '__main__':
    
    # Load any passed parameters if present
    if len(sys.argv) > 1:
        SCRIPT_PARAMETERS=ast.literal_eval(sys.argv[1])
    else:
        SCRIPT_PARAMETERS['name']="No parameters passed"
        SCRIPT_PARAMETERS['age']=-1
    
    # Call main
    main()