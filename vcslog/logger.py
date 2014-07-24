'''
Created on 2014-5-7

@author: feige05
'''
import os, sys, logging
from logging.handlers import TimedRotatingFileHandler

class Log(object):
    '''
    classdocs
    '''
    def __init__(self, filename="vcs"):
        '''
        Constructor
        '''
        self.log = logging.getLogger(filename)
        dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
        dirname = os.path.join(dirname, 'log')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            
        logfile = os.path.abspath(os.path.join(dirname, filename))
        
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        fileTimeHandler = TimedRotatingFileHandler(logfile, "D", 1)
        
        fileTimeHandler.suffix = "%Y%m%d.log"
        logging.basicConfig(level=logging.INFO)
        fileTimeHandler.setFormatter(formatter)
        self.log.addHandler(fileTimeHandler)
        
    def getLog(self):
            return self.log

log = None

if(not log):
    log = Log().getLog()
