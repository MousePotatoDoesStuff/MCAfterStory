init python:

    class Entity_V0:
        def __init__(self, name, character=None, memorypath=['base','main',0,0],memories=dict()):
            self.name=name
            self.character=character
            self.memorypath=memorypath
            self.mpl=len(memorypath)
            self.memories=dict()
        def save(path,values=dict()):
            pl=len(path)
            if pl<self.mpl:
                path=self.memorypath[:self.mpl-pl]+path
            current=self.memories
            for e in path:
                if e not in current:
                    current[e]=dict()
                current=current[e]
            current.update(values)
            return
        def load(path):
            pl=len(path)
            if pl<self.mpl:
                path=self.memorypath[:self.mpl-pl]+path
            current=self.memories
            for e in path:
                if e not in current:
                    return None
                current=current[e]
            return current
        def generate_memory_label(path, format):
            var_label="invalid_label"
            if format==0: # Base format for label generation: <submod_name>_<category>_<chapter>_<label-id> (with more than 4 levels of structure possible)
                pl=len(path)
                if pl<self.mpl:
                    path=self.memorypath[:self.mpl-pl]+path
                if path[0]=='base':
                    path[0]=''
                if path[1]=='main':
                    path[1]=''
                    path[2]='ch'+str(path[2])
                var_label='_'.join([str(var_e) for var_e in path if var_e!=''])
            return var_label

label mem_initiate: # Initiate MC's memory system.
    python:
        persistent.memories=dict()
        var_X=dict()
        persistent.memories['base']=var_X
        var_Y=dict()
        var_X['main']=var_Y
        var_Y=dict()
        var_X['choices']=var_Y
    return

label mem_save(var_path,var_values=dict()): # Save values to memory.
    python:
        if len(var_path)<4:
            var_path=['base','main',0,0][:4-len(var_path)]+var_path
        var_current=persistent.memories
        for var_e in var_path:
            if var_e not in var_current:
                var_current[var_e]=dict()
            var_current=var_current[var_e]
        var_current.update(var_values)
    return

label mem_load(var_path,load_var_dict=False): # Load value from memory.
    python:
        if len(var_path)<4:
            var_path=['base','main',0,0][:4-len(var_path)]+var_path
        var_value=(False,None)
        var_current=persistent.memories
        for var_e in var_path:
            if var_e not in var_current:
                var_value=(False,True)
                break
            var_current=var_current[var_e]
        if var_value[1] is None:
            var_value=(True,var_current)
    return

label mem_to_label(var_path=['base','main',0,0], format=0): # Generate Ren'Py label from memory path.
    python:
        var_label="invalid_label"
        if format==0: # Base format for label generation: <submod_name>_<category>_<chapter>_<label-id> (with more than 4 levels of structure possible)
            if len(var_path)<4:
                var_path=['base','main',0,0][:4-len(var_path)]+var_path
            if var_path[0]=='base':
                var_path[0]=''
            if var_path[1]=='main':
                var_path[1]=''
                var_path[2]='ch'+str(var_path[2])
            var_label='_'.join([str(var_e) for var_e in var_path if var_e!=''])
    return

label mem_dump(var_path=[], filepath="dump.txt"): # Dump part of memory or the whole thing.
    python:
        var_value=(False,None)
        var_current=persistent.memories
        for var_e in var_path:
            if var_e not in var_current:
                var_value=(False,True)
                break
            var_current=var_current[var_e]
        if var_value[1] is None:
            var_value=(True,var_current)
        if var_value[0]:
            var_res=str(var_value[1])
        else:
            var_res='This memory path does not exist.'
        F=open(basedir+'/'+str(dump_counter)+filepath,'w') # Semi temporary - replace with proper file making
        dump_counter+=1
        F.write(var_res)
        F.close()
    return
