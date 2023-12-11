init -9 python:
    import os
    import pickle


    class EventDataRegistry:
        def __init__(self):
            self.events = dict()
            self.categories = dict()

        def easy_set(self, category, lbl, followup=[], ephemeral=False, name=None):
            name = lbl if name is None else name
            X = {'label': lbl,
                'category': category,
                'name': name,
                'followup': followup,
                'ephemeral': ephemeral
                }
            self.categories[category] = self.categories.get(category,set())|{lbl}
            self.events[lbl] = X
            return X
        
        def serial_easy_set(self,category,labels,names=None,ephemeral=False):
            L=[]
            n=len(labels)
            if n!=len(names):
                raise Exception("EventDataRegistry: name list size doesn't match label list size")
            for i in range(n):
                L.append(self.easy_set(category,labels[i],[],ephemeral,names[i]))
            for i in range(1,n):
                L[i-1]['followup']=[labels[i]]
            return L

        def get(self, lbl, dft=None):
            return self.events.get(lbl, dft)
        
        def list_events(self,category=None,checklist=None,criterion=None,nolink=True):
            X=list(self.events.keys()) if category is None else list(self.categories[category])
            X.sort()
            if criterion is not None:
                pass
            if checklist is not None:
                X=[el for el in X if el in checklist]
            if nolink:
                X=[el for el in X if not self.events[el].get('nolink',False)]
            return X
            
    EDR_MC=EventDataRegistry()
init -8 python:
    temp_savedir="\\".join([config.basedir,"game","saves","MC"])
    os.makedirs(temp_savedir, exist_ok=True)
    LOCAL=LocalSaves(temp_savedir)