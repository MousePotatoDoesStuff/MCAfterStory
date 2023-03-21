label quick_menu_choice(value=None):
    if type(value)!=int:
        $ value=m_index
    $ m_index=value # cannot be easily placed in a Python function, this is a cleaner solution
    $ quick_menu=m_index>=0
    return

init -10 python:
    class MenuEntry:
        def GetButton(self):
            raise NotImplementedError
    class MenuNotPage(MenuEntry):
        def __init__(self,tab_name,instruction):
            self.tab_name=tab_name
            self.instruction=instruction
        def GetButton(self):
            return self.tab_name,self.instruction
    class MenuPage(MenuEntry):
        def __init__(self,tab_name,menu_name=None):
            if menu_name is None:
                menu_name=tab_name.lower().replace(' ','_')
            self.tab_name=tab_name
            self.menu_name=menu_name
        def GetButton(self):
            return self.tab_name,[ShowMenu(self.menu_name), SensitiveIf(renpy.get_screen(self.menu_name) == None)]
    class MenuNavManager:
        def __init__(self):
            self.menus=dict()
            self.current=None
            return
        def Add(self,name,menu):
            self.menus[name]=menu
            if self.current is None:
                self.current=name
            return
        def Get(self,name):
            L=[]
            for el in self.menus[name]:
                e2=el[1].GetButton()
                L.append((el[0],e2[0],e2[1]))
            return L
        def GetCurrent(self):
            return self.Get(self.current)
        def SetCurrent(self,name):
            if name not in self.menus:
                raise Exception("Menu {} not available!".format(name))
            self.current=name
            return
    class SelectionList:
        def __init__(self,options):
            self.options=options
    def MakeOpenMenu(menuname,lbl=None,cond=None):
        lbl = menuname if lbl is None else lbl
        return (cond,MenuNotPage(menuname,ShowMenu(lbl)))
    #----------------------------------------------------------
    def ReenterName():
        if not player: return False
        LOCAL.set('names','MC', player)
        persistent.playername = player
        persistent.mcname = player
        mc_name = player
        renpy.hide_screen("name_input")
        renpy.jump_out_of_context("start")
        return True
    def FinishEnterName():
        if ReenterName():
            renpy.jump_out_of_context("start")
        return
    def SomeDataInput():
        renpy.hide_screen("text_input_scr")
        return
    def filter_buttons(options,k):
        return [e for e in options if e.lower()[:len(k)]== k.lower()]
    def MakeScreenHideFunction(screen_name):
        def fnc():
            renpy.hide_screen(screen_name)
            return
        return fnc
    def MakeCallMemoryFunction(lbl,memory=False,screen_name=None):
        X=EDR_MC.get(lbl)
        if X is not None:
            def fnc():
                renpy.call("run_memlabel",lbl,memory)
                renpy.hide_screen(screen_name)
        else:
            fnc=NullAction()
        return fnc
    #----------------------------------------------------------
    def create_MCAS_screens():
        pclambda=lambda:renpy.variant("pc")
        _main=[
            (None,MenuNotPage("Run program",
            If(persistent.playername, true=Start(), false=Show(screen="name_input", message="Username:", ok_action=Function(FinishEnterName)))
            )),
            (None, MenuPage("Settings","preferences")),
            (None, MenuPage("Credits","about"))
            
        ]
        _active=[
            (None,MenuPage("History")),
            (None,MenuPage("Memory"))
        ]
        _memory=[
            (None,MenuPage("History")),
            (None,MenuNotPage("End memory",[lambda:renpy.jump_out_of_context("universal_return")]))
        ]
        _hub=[
            (None,MenuPage("History")),
            (None,MenuPage("Run label")),
            (None,MenuPage("Open memory","memory")),
            (None,MenuNotPage("Main Menu",MainMenu()))
        ]
        SC=[
            (None, MenuPage("Settings","preferences")),
            (None, MenuPage("Credits","about"))
        ]
        _main+=SC
        _hub+=SC
        _active+=SC
        _memory+=SC
        PC=[
            (None,MenuNotPage(
                "Help",[Help("README.html"), Show(screen="dialog", message="The help file has been opened in your browser.", ok_action=Hide("dialog"))]
            )),
            (None,MenuNotPage(
                "Quit",Quit(confirm=not main_menu)
            ))
        ]
        if renpy.variant("pc"):
            _main+=PC
            _hub+=PC
        final=MenuNavManager()
        final.Add("main",_main)
        final.Add("hub",_hub)
        final.Add("active",_active)
        final.Add("memory",_memory)
        return final
    def create_MCAS_quickmenus():
        _main=[
            MakeOpenMenu('History'),
            MakeOpenMenu('Memory','memory'),
            MakeOpenMenu("Run label","run_label"),
            (None,MenuNotPage('Auto',Preference("auto-forward", "toggle"))),
            MakeOpenMenu('Settings','preferences'),
            (None,MenuNotPage('Restart',renpy.utter_restart))
        ]
        _hub=_main
        final=MenuNavManager()
        final.Add("main",_main)
        final.Add("hub",_hub)
        final.Add("active",[])
        final.Add("memory",[])
        return final
    menu_navmanager=create_MCAS_screens()
    quickmenu_navmanager=create_MCAS_quickmenus()

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.8

        spacing gui.navigation_spacing

        for (cond,name,act) in menu_navmanager.GetCurrent():

            if cond is None or cond():
                textbutton _(name) action act

screen quick_menu():
    zorder 100
    if quick_menu:
        vbox:
            style_prefix "quick"
            yalign 0.995
            for (cond,name,act) in quickmenu_navmanager.GetCurrent():
                if cond is None or cond():
                    frame:
                        textbutton _(name) action act

screen main_hub_quick_menu():

    # Ensure this appears on top of other screens.
    zorder 100

    if m_index==1:
        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 0.995
            textbutton _("Enter text") action Show(screen="text_input_scr", message="Please enter data", ok_action=MakeScreenHideFunction('text_input_scr'))
            textbutton _("Select") action Show(screen="selection_scr", message="Select")
            # textbutton _("Access memory") action MakeJumpTo('MC_hub_openmemory')
            # textbutton _("Ask question") action MakeJumpTo('MC_hub_askquestion')
            # textbutton _("Dev tools") action MakeJumpTo('MC_hub_devoptions')
            textbutton _("Restart") action renpy.utter_restart

screen old_quick_menu():

    # Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        # Add an in-game quick menu.
        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 0.995

            textbutton _("History") action ShowMenu('history')
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            # textbutton _("Enter text") action Show(screen="text_input_scr", message="Please enter data", ok_action=MakeScreenHideFunction('text_input_scr'))
            # textbutton _("Select") action Show(screen="selection_scr", message="Select")
            #textbutton _("Save") action ShowMenu('save')
            #textbutton _("Load") action ShowMenu('load')
            #textbutton _("Q.Save") action QuickSave()
            #textbutton _("Q.Load") action QuickLoad()
            textbutton _("Settings") action ShowMenu('preferences')
            textbutton _("Restart") action renpy.utter_restart