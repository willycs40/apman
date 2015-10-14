import time
import sys 
import ast
import logging
import sys

SCRIPT_PARAMETERS = {}

def main():

    logging.info(sys.prefix)
    logging.info("hello " + SCRIPT_PARAMETERS['name'])

    time.sleep(1)
    logging.debug("there")
    logging.info(SCRIPT_PARAMETERS['name'])

    sys.stdout.flush()
    sys.stderr.flush()
    
    logging.info('info testing')
    logging.error('error testing')

class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)

if __name__ == '__main__':
    
    # Load any passed parameters if present
    if len(sys.argv) > 1:
        SCRIPT_PARAMETERS=ast.literal_eval(sys.argv[1])
    else:
        SCRIPT_PARAMETERS['name']="No parameters passed"
        SCRIPT_PARAMETERS['age']=-1

    logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s|%(levelname)s|%(message)s',
       datefmt='%m/%d/%Y %I:%M:%S'
    )
 
    main()