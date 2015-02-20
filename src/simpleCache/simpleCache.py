import datetime
import os, os.path, time


def checkSimpleCache(_location,_file):
    file = _location+_file+".txt"
    if(os.path.exists(file)):
        print "last modified: %s" % time.ctime(os.path.getmtime(file))
        last_mod = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(file)))
        today = datetime.date.today()
        #print last_mod
        #print today
        if( datetime.datetime.strptime(str(today),'%Y-%m-%d') == datetime.datetime.strptime(str(last_mod),'%Y-%m-%d') ):
            return True
        else:
            return False
    else:
        return False
    
def readSimpleCache(_location,_file):
    file = _location+_file+".txt"
    if(os.path.exists(file)):
        with open (file, "r") as myfile:
            data=myfile.read()
        return data
    else:
        return ""

def writeSimpleCache(_location,_file, html):
    file = _location+_file+".txt"
    with open(file, "w") as text_file:
        text_file.write(html)