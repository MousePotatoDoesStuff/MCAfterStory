default fs_temp=''

init -1 python:
    fs_console=ConsoleLogClass('FilesystemConsole')
    import os
    class FileSystem:
        def Refresh(self):
            raise NotImplementedError

        def GetCurrentDirFiles(self):
            raise NotImplementedError

        def GetCurrentDirFolders(self):
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
            self.files = []
            self.folders = []
            self.ext = extensions
            self.Refresh()
            return

        def Refresh(self):
            if len(self.ipl) != 0:
                self.files = []
                self.folders = []
                for e in os.listdir(self.initpath):
                    if os.path.isdir(self.initpath + '/' + e):
                        self.folders.append(e)
                    elif os.path.isfile(self.initpath + '/' + e):
                        if self.ext is not None:
                            res = ''
                            for f in self.ext:
                                if e[-len(f):] == f:
                                    res = f
                            if res == '':
                                continue
                        self.files.append(e)
            else:
                X = [chr(e) + ':' for e in range(65, 91)]
                self.folders = [e for e in X if os.path.exists(e)]
                self.files = []
            return

        def GetCurrentDirFiles(self):
            self.Refresh()
            if len(self.ipl) != 0:
                return self.files
            else:
                return []

        def GetCurrentDirFolders(self):
            self.Refresh()
            if len(self.ipl) != 0:
                return self.folders + ['..']
            else:
                return self.folders

        def JumpToDir(self, t_dir):
            if t_dir == '..':
                if len(self.ipl) != 0:
                    self.ipl.pop()
            else:
                if t_dir in self.folders:
                    self.ipl.append(t_dir)
            self.initpath = '/'.join(self.ipl)

        def GetDirPath(self):
            return self.initpath

        def GetFilePath(self, name):
            return self.initpath + '/' + name
    
    def FSUI_save_persistent(file):
        with open(file,'w') as F:
            pickle.dump(persistent,F)
        return
        
    def FSUI_load_persistent(file):
        F=open(file,'r') # Semi temporary - will replace with proper file making
        persistent=pickle.load(F)
        renpy.save_persistent() # Yeah, it seems contradictory.
        return
    
    def FSUI_make_new_file(extension):
        def fnfn():
            if not fs_temp:
                return
            fname=fs_temp+'.'
            renpy.hide_screen("fs_name_input")
            F=open(file,'w')
            F.close()
            return



screen fs_name_input(ok_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"
    key "K_RETURN" action [Play("sound", gui.activate_sound), ok_action]

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _('Change name'):
                style "confirm_prompt" # MCAS
                xalign 0.5

            input default sc_ene.curframe.tx[0]+'?' value VariableInputValue("fs_temp") length 20 # allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _"
            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action

label FilesystemUI(startdir,extensions,action=('Save',FSUI_save_persistent),data=persistent):
    scene black
    $ config.skipping = False
    $ config.allow_skipping = False
    $ allow_skipping = False
    python:
        rfs=RealFileSystem(startdir.replace('\\','/').split('/'),extensions)
        r_curfile=None
        r_is_curselected=False
        r_toggle=0
        while True:
            r_files=rfs.GetCurrentDirFiles()
            r_folders=rfs.GetCurrentDirFolders()
            r_files.sort()
            r_folders.sort()
            test_files = (r_files+['TODO']*10)[:9]+[str(len(r_files))]+['TODO']*10
            test_folders = (r_folders+['TODO']*10)[:9]+[str(len(r_folders))]+['TODO']*10

            ui.vbox() #This is outdated UI code to create a vbox. It adds things to the vbox until it hits a ui.close()
            ui.textbutton(action[0], clicked=ui.returns('0'+action[0]), style="poemgame_text", xpos=50, ypos=200, color='#BB0')
            ui.textbutton(action[0]+' and exit', clicked=ui.returns('0Both'), style="poemgame_text", xpos=50, ypos=250, color='#BB0')
            ui.textbutton('Exit', clicked=ui.returns('0Exit'), style="poemgame_text", xpos=50, ypos=300, color='#BB0')
            if action=='load':
                ui.textbutton('New file', clicked=ui.returns('0New'), style="poemgame_text", xpos=50, ypos=300, color='#BB0')
            ui.close()
            ui.text(rfs.GetDirPath(), style="poemgame_text", xpos=100, ypos=80, color='#BB0')
            ui.text(str(r_curfile)+';'+'NY'[r_is_curselected], clicked=ui.returns('0Save'), style="poemgame_text", xpos=100, ypos=120, color='#BB0')
            x = 200
            ui.vbox() #This is outdated UI code to create a vbox. It adds things to the vbox until it hits a ui.close()
            ystart=200
            for i in range(10):
                ui.textbutton(test_files[i], clicked=ui.returns('1'+test_files[i]), style="poemgame_text", xpos=x, ypos=i * 20 + ystart, color='#BB0')
            ui.close()
            x = 640
            ui.vbox()
            ystart=200
            for i in range(10):
                ui.textbutton(test_folders[i], clicked=ui.returns('2'+test_folders[i]), style="poemgame_text", xpos=x, ypos=i * 20 + ystart)
            ui.close()
            t = ui.interact()
            t_dec=int(t[0])
            t_val=t[1:]
            if t_dec==0:
                if t_val==action[0]:
                    fs_console.printLine(str(r_curfile)+';'+'YN'[r_is_curselected])
                    if r_is_curselected:
                        action[1](r_curfile)
                elif t_val=='Quit':
                    r_is_curselected=False
                    break
                elif t_val=='Both':
                    if r_is_curselected:
                        action[1](r_curfile)
                        renpy.utter_restart()
                elif t_val=='Exit':
                    break
            elif t_dec==1:
                r_curfile = rfs.GetFilePath(t_val)
                r_is_curselected=True
            elif t_dec==2:
                rfs.JumpToDir(t_val)
    return

label backup_persistent(startdir,extensions=['.mcasbkp']):
    call FilesystemUI(startdir,['.mcasbkp'],('Save',FSUI_save_persistent))
    return

label load_persistent(startdir,extensions=['.mcasbkp']):
    call FilesystemUI(startdir,['.mcasbkp'],('Load',FSUI_load_persistent))
    return
