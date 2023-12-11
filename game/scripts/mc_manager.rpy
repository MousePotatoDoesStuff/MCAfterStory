init -10 python:
    import pickle

    import datetime
    import bisect

    TESTDATE = datetime.datetime(2029, 1, 1, 0, 0, 0, 0)

    initial_labels=[]
    autocall_labels=[]

    class Memory:
        def __init__(self, initialTime, initialData):
            self.current = 1
            self.data = [(initialTime,0,initialData)]
            return

        def get_index_eg(self, timestamp):
            return bisect.bisect_left(self.data, (timestamp, self.current, None))

        def get_index_gt(self, timestamp):
            return bisect.bisect_right(self.data, (timestamp, self.current, None))
        
        def wipe_future(self, timestamp, keep_present=True):
            self.data=self.data[:bisect.bisect_left]
            return

            
        def pop_future(self, timestamp, keep_present=True):
            X=self.data[0[1]]
            RES=[]
            while True:
                e=self.data.pop()
                if e[0]<timestamp or keep_present and e[0]==timestamp:
                    self.data.append(e)
                    return RES[::-1]
                else:
                    RES.append(e)
            self.data.append((timestamp,0,X))
            return RES[::-1]


        def update(self, timestamp, data=None, preservePast=False):
            L=[]
            while self.data[-1][0]<timestamp:
                _=self.data.pop()
                if preservePast:
                    L.append()
            self.data.append((timestamp, self.current, data))
            self.current += 1
            return

        def retrieveLast(self, timestamp=None):
            if len(self.data) == 0:
                return None
            if timestamp is None:
                return self.data[-1]
            location = self.get_index_gt(timestamp)
            if location == 0:
                return None
            return self.data[location - 1]

        def deleteRecent(self, recentTimestamp, preserveNow=True):
            if len(self.data) == 0:
                return False
            ind = self.get_index_gt(recentTimestamp) if preserveNow else self.get_index_eg(recentTimestamp)
            while True:
                X = self.data.pop()
                if X[0] < recentTimestamp or preserveNow and X[0] == recentTimestamp:
                    self.data.append(X)
                    break
            return len(self.data) == 0


    class MemoryManager:
        def __init__(self, backup=None):
            if backup is None:
                backup = dict()
            self.memories = backup
            return

        def create_memory(self, name, timestamp, data, serial=False, override=False):
            if serial:
                if name in self.memories:
                    X = self.memories.get(name)
                    X: Memory
                    X.update(timestamp, data, override)
                else:
                    X = Memory(timestamp, data)
                    self.memories[name] = X
                return True
            else:
                if override or name not in self.memories:
                    X = Memory(timestamp, data)
                    self.memories[name] = X
                    return True
                else:
                    return False

        def retrieve_memory(self, name):
            return self.memories.get(name, None)


    class DokiEntity:
        def __init__(self):
            self.status = MemoryManager()
            self.memories = MemoryManager()
            self.clock = RealTime()
            self.available_labels=set(initial_labels)
            self.persistent_queue=autocall_labels # Things that persist over restarts, e.g. the main storyline.
            self.ephemeral_queue=list() # Things that are lost with 
            return

        def save(self, filename):
            F = open(filename, 'wb')
            pickle.dump({
                'status':self.status,
            'memories':self.memories,
            'clock':self.clock,
            'queue':self.persistent_queue
            }, F)
            F.close()
            return

        def load(self, filename):
            F = open(filename, 'rb')
            T = pickle.load(F)
            self.status=T.get('status',self.status)
            self.memories=T.get('memories',self.memories)
            self.clock=T.get('clock',self.clock)
            self.persistent_queue=T.get('queue',self.persistent_queue)
            F.close()
            return
        
        def create_memory(self, *args):
            return self.memories.create_memory(*args)

        def retrieve_memory(self, *args):
            return self.memories.retrieve_memory(*args)
        
        def apply_to_queue(self,lbl,ephemeral=False,priority=1):
            if type(lbl)!=list:
                lbl=[lbl]
            if ephemeral:
                self.ephemeral_queue.extend(lbl)
            else:
                self.persistent_queue.extend(lbl)
            return
        
        def get_from_queue(self):
            if len(self.ephemeral_queue)!=0:
                return (self.ephemeral_queue.pop(),True)
            if len(self.persistent_queue)!=0:
                return (self.persistent_queue.pop(),False)
            return None
        
        def add_available_label(self,el):
            if len(el)<2:
                raise Exception("Input doesn't have enough data(only {}, not 2)!".format(len(el)))
            lbl,name=el[0],el[1]
            if type(lbl)!=str:
                raise Exception("Label is of type {}, needs to be string!".format(type(lbl)))
            if type(name)!=str:
                raise Exception("Name is of type {}, needs to be string!".format(type(name)))
            self.available_labels.add(el)
            return
        
        def add_multiple_available_labels(self,lbls):
            for el in lbls:
                self.add_available_label(el)
            return




    
    def generate_clock():
        meta_mem=mc_str.status.retrieve_memory('meta')
        meta_altered=False
        meta=None
        last_timestamp=mc_str.clock.getTime()
        last_index=-1
        if meta_mem is not None:
            (last_timestamp,last_index,meta)=meta_mem.retrieveLast()
        if meta is None:
            meta=dict()
            meta_altered = True
        if 'clock' in meta:
            clock=meta['clock']
        else:
            clock=mc_str.clock
            meta_altered = True
            meta['clock']=clock
        if meta_altered:
            mc_str.status.create_memory('meta',clock.getTime(),meta)
        return

