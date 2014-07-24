import savetomongo
import parselog
from logger import log
import pexpect


class GetLog():
    def __init__(self, ip, user, passwd, cmd):
        self.__ip = ip.strip()
        self.__user = user
        self.__passwd = passwd
        self.__cmd = cmd
        self.__data = self.dossh()
        self.__db = savetomongo.DB('10.98.4.8')
        
        if(isinstance(self.__data, str)):
            self.__db.connect()
            last = self.__db.getLast(self.__ip)
            try:
                P = parselog.Parse(self.__data, last, self.__ip)
                self.__data = P.getData()
                log.info('Get data Done ! ip : %s' % self.__ip)
            except Exception:
                self.__data = None
                
            if(self.__data):
                D = self.formatData()
                if(len(D[0])):
                    self.__db.saveTotal(self.__ip, self.getLast(D[1]))
                    self.__db.saveCalls(self.__ip, D[0])
            else:
                log.info('Not found new calls, ip : %s ,last : %s ' % (self.__ip, last))
                    
            self.__db.close()
            
    def getLast(self, L):
            L.sort()
            last = L[-1]
            l = len(L)
            for i, c in enumerate(L):
                if(i < l - 1 and L[i] != L[i + 1] - 1):
                    last = c
                    break
            return last
        
    def formatData(self):
            L = []
            K = []
            for key, value in self.__data.items():
                callId = int(key)
                value['ip'] = self.__ip
                value['callId'] = callId
                L.append(value)
                K.append(callId)
            return (L, K)
        
    def dossh(self):
        ret = -1
        ssh = pexpect.spawn('ssh %s@%s' % (self.__user, self.__ip))
        try:
            i = ssh.expect(['Password:', 'continue connecting(yes/no)?'])
            if i == 0:
                ssh.sendline(self.__passwd)
            elif i == 1:
                ssh.sendline('yes\n')
                ssh.expect('Password:')
                ssh.sendline(self.__passwd)
            ssh.expect('\nOK')
            print self.__cmd
            ssh.sendline(self.__cmd)
            ssh.expect('\nOK', timeout= -1)
            ret = ssh.before
            print '[%s] get xhistory calls done!' % self.__ip
            log.info('[%s] get xhistory calls done!' % self.__ip)
        except pexpect.EOF:
            print "EOF"
            log.warning('[%s]dossh error : EOF !' % (self.__ip))
            ret = -1
        except pexpect.TIMEOUT:
            print "TIMEOUT"
            log.warning('[%s]dossh error : TIMEOUT !' % (self.__ip))
            ret = -2
        finally:
            ssh.close()
        return ret
    
def job_function(ip, user, passwd, cmd):
    GetLog(ip, user, passwd, cmd)
