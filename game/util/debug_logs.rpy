init -10 python:
    class ConsoleLogClass:
        def __init__(self,filename='consoleLogMain',active=True):
            basedir=config.basedir
            self.filename=filename
            F=open(basedir+'/debug/'+filename+'.txt','w') # Semi temporary - will replace with proper file making
            F.write("Log dump:\n")
            F.close()
        def printLine(self,text):
            basedir=config.basedir
            F=open(basedir+'/debug/'+self.filename+'.txt','a') # Semi temporary - will replace with proper file making
            F.write(text+'\n')
            F.close()
    consoleLogMain=ConsoleLogClass()
