init -11 python:
    import os
    import pickle


    class LocalSaves:
        def __init__(self, dirpath, extension='.dat', autoload=True):
            self.dirpath = dirpath
            self.data = dict()
            self.updated = set()
            self.extension = extension
            if autoload:
                self.load()

        def get(self, filename, key, default=None, def2=None, doubleDefault=False):
            if not doubleDefault:
                def2 = default
            if filename not in self.data:
                return default
            base = self.data[filename]
            ret = base.get(key, def2)
            return ret

        def load(self):
            files = os.listdir(self.dirpath)
            for f in files:
                if not os.path.isfile(self.dirpath + '/' + f):
                    continue
                if not f.endswith(self.extension):
                    continue
                F = open(self.dirpath + '/' + f, 'rb')
                X = pickle.load(F)
                F.close()
                name = X['__name__']
                self.data[name] = X
            return

        def delete_all_files(self):
            files = os.listdir(self.dirpath)
            for f in files:
                if not os.path.isfile(self.dirpath + '/' + f):
                    continue
                if not f.endswith(self.extension):
                    continue
                os.remove(self.dirpath + '/' + f)
            return

        def save(self, filename):
            if filename not in self.data:
                return False
            current = self.data[filename]
            filepath = self.dirpath + '/' + filename + self.extension
            print(filepath)
            F = open(filepath, 'w')
            F.close()
            F = open(filepath, 'wb+')
            pickle.dump(current, F)
            F.close()
            return True

        def save_more(self, save_all=False):
            cur = set(self.data.keys()) if save_all else self.updated
            for filename in cur:
                self.save(filename)
            self.updated = set()
            return

        def set(self, filename, key, value, overwrite=True, autosave=True):
            if not overwrite:
                if key in self.data:
                    return False
            if filename not in self.data.keys():
                current = {'__name__': filename}
                self.data[filename] = current
            else:
                current = self.data[filename]
            current[key] = value
            self.updated.add(filename)
            if autosave:
                if self.save(filename):
                    self.updated.remove(filename)
            return True