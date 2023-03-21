init -15 python:
    class ConsoleLogClass:
        def __init__(self,filename='consolelog',active=True):
            basedir=config.basedir
            self.filename=filename
            try:
                os.mkdir(basedir+'/debug/')
            except:
                pass
            F=open(basedir+'/debug/'+filename+'.txt','w') # Semi temporary - will replace with proper file making
            F.write("Log dump:\n")
            F.close()
        def printLine(self,text):
            basedir=config.basedir
            F=open(basedir+'/debug/'+self.filename+'.txt','a') # Semi temporary - will replace with proper file making
            F.write(text+'\n')
            F.close()
    try:
        F=open(basedir+'/debug/'+filename+'.txt','w') # Semi temporary - will replace with proper file making
        F.write("Log dump:\n")
        F.close()
        temp=True
    except:
        temp=False
    consolelog=ConsoleLogClass(active=temp)