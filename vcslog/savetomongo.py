'''
Created on 2014-5-6

@author: feige05
'''
from pymongo import Connection
from logger import log

class DB(object):
    '''
    Save to MongoDB.
    '''
    
    def __init__(self, host='localhost', db="vcslog"):
        '''
        Constructor
        '''
        self.host = host
        self.db = db
        
    def connect(self):
        self.__con = Connection(host=self.host)
        self.__db = self.__con[self.db]
        log.info('[%s] mongodb connected.' % self.host)
        
    def saveTotal(self, ip, last):
        has = self.__db.Total.find_one({"ip":"%s" % ip})
        if(has):
            has['last'] = last
            self.__db.Total.save(has)
        else:
            self.__db.Total.insert(dict(ip="%s" % ip, last="%s" % last))
        log.info('[%s] mongodb seve Total done ! ip: %s , last: %s' % (self.host, ip, last))
        
    def saveCalls(self, ip, List):
        self.__db.Calls.insert(List)
        log.info('[%s] mongodb seve Calls done ! ip: %s , len: %s' % (self.host, ip, len(List)))
        
    def getLast(self, ip):
        last = False
        has = self.__db.Total.find_one({"ip":"%s" % ip})
        if(has):
            last = has['last']
        return last
    
    def close(self):
        self.__con.close()
        log.info('[%s] mongodb closed.' % self.host)
