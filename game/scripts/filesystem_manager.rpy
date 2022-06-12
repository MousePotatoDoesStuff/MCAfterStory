init -1 python:
    import os


    class FileSystem:
        def Refresh(self):
            raise NotImplementedError

        def GetCurrentDir(self):
            raise NotImplementedError

        def JumpToDir(self, t_dir):
            raise NotImplementedError

        def GetDirPath(self):
            raise NotImplementedError

        def GetFilePath(self, name):
            raise NotImplementedError


    class RealFileSystem(FileSystem):
        def __init__(self, ipl, extensions):
            self.ipl = ipl
            self.initpath = '/'.join(ipl)
            self.files = os.listdir(self.initpath)
            self.ext = extensions
            return

        def Refresh(self):
            if len(self.ipl) != 0:
                self.files = []
                for e in os.listdir(self.initpath):
                    if os.path.isdir(self.initpath + '/' + e):
                        self.files.append(e)
                    elif os.path.isfile(self.initpath + '/' + e):
                        if self.ext is not None:
                            res = ''
                            for f in self.ext:
                                if e[-len(self.ext):] == f:
                                    res = f
                            if res == '':
                                continue
                        self.files.append(e)
            else:
                X = [chr(e) + ':' for e in range(65, 91)]
                self.files = [e for e in X if os.path.exists(e)]
            return

        def GetCurrentDir(self):
            self.Refresh()
            if len(self.ipl) != 0:
                return self.files + ['..']
            else:
                return self.files

        def JumpToDir(self, t_dir):
            if t_dir == '..':
                if len(self.ipl) != 0:
                    self.ipl.pop()
            else:
                if t_dir in self.files:
                    self.ipl.append(t_dir)
            self.initpath = '/'.join(self.ipl)

        def GetDirPath(self):
            return self.initpath

        def GetFilePath(self, name):
            return self.initpath + '/' + name