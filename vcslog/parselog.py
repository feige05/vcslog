'''
Created on 2014-5-6

@author: feige05
'''
import datetime, os, sys
import yaml
import re
from logger import log

class Parse(object):
    '''
    classdocs
    '''

    def __init__(self, data, last=False, ip=''):
        '''
        Constructor
        '''
        self.__data = data
        self.__last = last
        self.__ip = ip
        if(self.__clear()):
            p = re.compile(r'(\s{13,})(\d+):\n')
            self.__data = p.sub(r'\1- Id: \2\n', self.__data)
            p = re.compile(r'(\s{13,})(\d+):\s')
            self.__data = p.sub(r'\1- ', self.__data)
            p = re.compile(r'(Duration|Allocated|Requested):\s"(\d+)"')
            self.__data = p.sub(r'\1: \2 ', self.__data)
            self.__parseYaml()
        
    def __removeHeadAndTail(self):
        try:
            ii = self.__data.index('     Call:')
            i = self.__data.rindex('*l/end')
            self.__data = self.__data[ii + 10:i]
            return True
        except:
            print 'xhistory calls document is incomplete!'
            return False
        
    def __clear(self):
        if(self.__removeHeadAndTail()):
            if(self.__last):
                m = self.__data.rfind('\n       %s:' % self.__last)
                if(m > 0):
                    self.__data = self.__data[m:]
            return True
        else:
            return False
        
    def __parseYaml(self):
        try:
            self.__data = yaml.load(self.__data)
            log.info('Parse Yaml done! ip: %s' % (self.__ip))
            if(self.__last):
                if(self.__last in self.__data):
                    del self.__data[self.__last]
                    log.info('Delete last callId done! ip: %s, last: %s' % (self.__ip, self.__last))
                else:
                    log.warning('Not found last callId, ip: %s, last: %s' % (self.__ip, self.__last))
        except Exception, e:
            log.warning('Parse Yaml Error! ip: %s', self.__ip)
            print Exception, ":", e
            self.__saveFile()
        
    def __saveFile(self):
        dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
        dirname = os.path.join(dirname, 'log')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        name = os.path.join(dirname, 'yaml_%s_%s.log' % (self.__ip, datetime.datetime.now()))
        filelog = open(name, 'w')
        filelog.write(self.__data)
        filelog.close()
        self.__data = None
            
    def getData(self):
        return self.__data
