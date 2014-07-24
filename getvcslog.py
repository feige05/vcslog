import os, sys
from apscheduler.scheduler import Scheduler
import vcslog

def job_function(ip, user, passwd, cmd):
    vcslog.GetLog(ip, user, passwd, cmd)

if __name__ == '__main__':
    dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
    dirname = os.path.join(dirname,'vcs.list')
    file = open(os.path.abspath(dirname), 'r')
    list = file.read()
    file.close()
    # Start the scheduler
    sched = Scheduler(daemonic=False)
    for host in list.split("\n"):
        if host.strip():
            ip, user, passwd, cmd = host.split("::")
            print "-- %s run:%s --" % (ip, cmd)
            sched.add_cron_job(job_function, minute='*/10', args=[ip, user, passwd, cmd])
    sched.start()
