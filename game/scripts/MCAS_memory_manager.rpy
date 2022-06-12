init -1 python:
    def membase(L):
        return ['base','main',0,0][:4-len(L)]+L
    memcon=ConsoleLogClass('memcon')
    # This is where MC as an entity is defined (his memories, for now - which will ultimately define his identity).
    class Entity_V0: # A first step towards something greater, perhaps?
        def __init__(self, name, character=None, memories=dict()):
            self.name=name
            self.character=character
            self.memories=dict()
        def save(self, path,values=dict()): # Removed mempath
            current=self.memories
            for e in path:
                if e not in current:
                    current[e]=dict()
                current=current[e]
            current.update(values)
            return
        def load(self, path, cur_time=None, rempath=[]):
            current=self.memories
            for e in path:
                rempath.append(e)
                if e not in current:
                    return None
                current=current[e]
            if cur_time is not None and 'ctime' in current and current['ctime']>cur_time:
                rempath.append(None)
                return None
            return current
        def generate_memory_label(self, path, format=0):
            var_label="invalid_label"
            if format==0: # Base format for label generation: <submod_name>_<category>_<chapter>_<label-id> (with more than 4 levels of structure possible)
                path=path[:]
                if len(path)>=4:
                    if path[0]=='base':
                        path[0]=''
                    if path[1]=='main':
                        path[1]=''
                        path[2]='ch'+str(path[2])
                var_label='_'.join([str(var_e) for var_e in path if var_e!=''])
            elif format==1:
                pass
            return var_label
        def dump_memory(self, path=[], name='dump'):
            mem=self.load(path)
            F=open(basedir+'/debug/'+name+'.txt','w') # Semi temporary - replace with proper file making
            F.write(str(mem))
            F.close()
