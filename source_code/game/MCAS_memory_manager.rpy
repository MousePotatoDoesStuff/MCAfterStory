init -1 python:
    # This is where MC as an entity is defined (his memories, for now - which will ultimately define his identity).
    class Entity_V0: # A first step towards something greater, perhaps?
        def __init__(self, name, character=None, memorypath=['base','main',0,0],memories=dict()):
            self.name=name
            self.character=character
            self.memorypath=memorypath
            self.mpl=len(memorypath)
            self.memories=dict()
        def save(self, path,values=dict(), useMempath=True): # TODO: DRY up mempath
            pl=len(path)
            if pl<self.mpl and useMempath:
                path=self.memorypath[:self.mpl-pl]+path
            current=self.memories
            for e in path:
                if e not in current:
                    current[e]=dict()
                current=current[e]
            current.update(values)
            return
        def load(self, path, useMempath=True, cur_time=None):
            pl=len(path)
            if pl<self.mpl and useMempath:
                path=self.memorypath[:self.mpl-pl]+path
            current=self.memories
            for e in path:
                if e not in current:
                    return None
                current=current[e]
            if cur_time is not None and 'ctime' in current and current['ctime']>cur_time:
                return None
            return current
        def generate_memory_label(self, path, format=0, useMempath=True):
            var_label="invalid_label"
            if format==0: # Base format for label generation: <submod_name>_<category>_<chapter>_<label-id> (with more than 4 levels of structure possible)
                pl=len(path)
                if pl<self.mpl and useMempath:
                    path=self.memorypath[:self.mpl-pl]+path
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
            mem=self.load(path, useMempath=False)
            F=open(basedir+'/'+name+'.txt','w') # Semi temporary - replace with proper file making
            F.write(str(mem))
            F.close()
