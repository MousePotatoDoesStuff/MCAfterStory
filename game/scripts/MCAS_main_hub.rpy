default persistent.auto_open=list() # DO NOT TOUCH THESE. YOU MIGHT BREAK SOMETHING.
default persistent.current_memory=None
default persistent.memdict=dict()
default persistent.questions=dict()
default persistent.dump_counter=0
default persistent.epiphany_stage=0

default MEM_old=0
default MEM_new=1
default MEM_debug=2

default main_hub_quick_menu=False

# Hello, player.
# Or perhaps even more - a fellow modder?
# Either way, thank you for taking the time to look at the code.
# Sorry for the mess.
# Signed, MousePotatoDoesStuff

init -10 python:
    class ConsoleLogClass:
        def __init__(self,filename='consolelog'):
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
    consolelog=ConsoleLogClass()

init -2 python:
    class SubmodData:
        def __init__(self, name, onInit=[], onLoad=[]):
            self.name=name
            self.onInit=onInit
            self.onLoad=onLoad
            return
    def SubmodMemory(name,path):
        if type(path)==str:
            path=[path]
        return ['submods','data',name]+path
    def LoadSubmods(MC,submod_list,autoload_list,logclass=None):
        for submod in submod_list.values():
            trace=[]
            memory=MC.load(['submods','data',submod.name],rempath=trace)
            if logclass is not None:
                logclass.printLine(submod.name)
                logclass.printLine(str(memory)+':'+str(trace)+':'+str(list(MC.load(trace[:-1]).keys())))
            if memory is None:
                logclass.printLine('Initialization: {}'.format(str(submod.onInit)))
                autoload_list.extend(submod.onInit)
                MC.save(['submods','data',submod.name])
            else:
                logclass.printLine('Loading: {}'.format(str(submod.onLoad)))
                autoload_list.extend(submod.onLoad)
    submods_available=dict()

init -1 python:
    def MakeJumpTo(dest):
        def X():
            renpy.jump(dest)
            return
        return X
    

image code_void:
    topleft
    "mod_assets/code_void.png"

screen main_hub_quick_menu():

    # Ensure this appears on top of other screens.
    zorder 100

    if main_hub_quick_menu:
        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 0.995

            textbutton _("Access memory") action MakeJumpTo('MC_hub_openmemory')
            textbutton _("Ask question") action MakeJumpTo('MC_hub_askquestion')
            textbutton _("Dump memory") action MakeJumpTo('dump_memory')
            textbutton _("Dev tools") action MakeJumpTo('MC_hub_devoptions')
            textbutton _("Reset") action MakeJumpTo('epip_reset')
            textbutton _("Exit") action MakeJumpTo('exit_to_menu')
            # textbutton _("") action MakeJumpTo('')

label dump_memory:
    $ MC.dump_memory([],str(persistent.dump_counter))
    $ persistent.dump_counter+=1
    jump MC_hub_menuloop

label epip_reset:
    call loading_screen("Resetting to start of epiphany...")
    $ persistent.epiphany_stage=1
    $ renpy.save_persistent()
    $ renpy.utter_restart()

label exit_to_menu:
    $ quick_menu=False
    call loading_screen("Saving data...")
    $ renpy.save_persistent()
    $ renpy.utter_restart()

#----------------------------------------------------------------------------------------------------------------------#
#                                                                                                                      #
#                                                    Main segment                                                      #
#                                                                                                                      #
#----------------------------------------------------------------------------------------------------------------------#

label jump_MC_epiphany: # This part initiates MC's memories.
    $ dump = len(str(persistent.memdict))
    python:
        var_time=datetime.datetime.now()
        MC=Entity_V0('MC',mc,memories=persistent.memdict)
        if persistent.epiphany_stage==1:
            persistent.memdict=dict()
            persistent.questions=dict()
            persistent.auto_open=[]
            for i in range(4):
                MC.save(membase([i]),{'ctime':var_time})
            persistent.auto_open.append((membase([4]),True)) # Instructs the loop to immediately load this label.
            persistent.epiphany_stage=2
            renpy.save_persistent()
    jump MC_start

label MC_start: # This part initiates the other stuff.
    python:
        renpy.config.window_title="MC After Story: Now with 18% less bugs!"
        if persistent.current_memory is not None:
            persistent.auto_open.append(persistent.current_memory)
            persistent.current_memory = None
        anticheat = persistent.anticheat
        chapter = 0
        _dismiss_pause = config.developer
        professor = "Professor"
        councilor = "Councilor"
        mc_name = persistent.mcname
        s_name = "Sayori"
        m_name = "Monika"
        n_name = "Natsuki"
        y_name = "Yuri"
    python:
        quick_menu = False
        main_hub_quick_menu = True
    $ style.say_dialogue = style.normal
    $ in_sayori_kill = None
    $ allow_skipping = False
    $ config.allow_skipping = False
    # Don't touch this segment below. I barely got it to work properly.
    $ dump = len(str(persistent.memdict))
    $ mc_name=persistent.mcname
    $ dump = len(str(persistent.memdict))
    if len(str(persistent.memdict))==2:
        $ persistent.memdict=MC.memories
    $ dump = len(str(persistent.memdict))
    $ renpy.save_persistent()
    $ MC.memories=persistent.memdict

    # $ MC.dump_memory(name=str(datetime.datetime.now()).replace(':','_'))
    # Okay, you're safe now.
    $ LoadSubmods(MC,submods_available,persistent.auto_open,consolelog)
    python:
        consolelog.printLine('Loaded openables:')
        for e in persistent.auto_open:
            consolelog.printLine(str(e))
        PlaceholderDialogue=[
            "So... what's the weather like?",
            "I don't have actual dialogue yet, this is just a proof-of-concept thing.",
            
        ]


label MC_hub_mainloop: # The main loop of the mod.
    # Don't touch this segment below. I barely got it to work properly.
    $ dump = len(str(persistent.memdict))
    $ mc_name=persistent.mcname
    $ dump = len(str(persistent.memdict))
    if len(str(persistent.memdict))==2:
        $ persistent.memdict=MC.memories
    $ dump = len(str(persistent.memdict))
    $ renpy.save_persistent()
    $ MC.memories=persistent.memdict

    # $ MC.dump_memory(name=str(datetime.datetime.now()).replace(':','_'))
    # Okay, you're safe now.
    if len(persistent.auto_open)!=0:
        $ persistent.current_memory=persistent.auto_open.pop()
        $ consolelog.printLine('Current memory: '+str(persistent.current_memory))
        $ var_path,eventCallType=persistent.current_memory
        if eventCallType in (0,2):
            menu:
                "Continue memory replay?"
                "Yes":
                    pass
                "No":
                    jump MC_hub_mainloop
        call call_event(var_path,eventCallType)
        $ persistent.current_memory=None
        jump MC_hub_mainloop
    play music coffee_and_sunlight
    scene code_void
    $ renpy.show("mc turned worr cm",[t33],zorder=3)
    $ wait_time=1
    # show mc turned worr at t33
label MC_hub_menuloop:
    $ quick_menu = False
    $ main_hub_quick_menu = True
    "[wait_time]...{w=[wait_time]}...{nw}"
    menu:
        "..."
        "1 second":
            $ wait_time=1
        "10 seconds":
            $ wait_time=10
        "1 minute":
            $ wait_time=60
        "10 minutes":
            $ wait_time=60*10
    jump MC_hub_menuloop

label MC_hub_openmemory:
    python:
        var_X=MC.load(['base','main'])
        if var_X is not None:
            var_Y=[]
            for var_k in var_X:
                var_E=var_X[var_k]
                var_Y.extend([[var_k,var_e] for var_e in var_E])
            var_n=len(var_Y)
            cho_menu_list=[]
            var_i=0
    if var_X is None:
        "Unable to access main memory."
        jump MC_hub_menuloop
    while var_i!=var_n:
        $ var_E=var_Y[var_i]
        $ var_label='MISSING_LABEL_IN_MEMORY'
        $ temp = 'Chapter {}, part {}'.format(var_E[0],var_E[1])
        $ cho_menu_list.append((temp,membase(var_E)))
        $ var_i+=1
    call adv_cho_menu_call(cho_menu_list,offer_return=True,disp_text="Access memory:")
    if cho_menu_result==-1:
        jump MC_hub_menuloop
    $ var_path=cho_menu_list[cho_menu_result][1]
    scene black
    "Loading memory...{w=1}{nw}"
    call call_event(var_path,False)
    scene black
    "Leaving memory...{w=1}{nw}"
    jump MC_hub_mainloop

label MC_hub_askquestion:
    $ cho_menu_result=None
    $ cho_menu_list=list(persistent.questions.items())
    $ consolelog.printLine("Question:")
    call adv_cho_menu_call(cho_menu_list,fit_size=3,offer_return=True)
    $ consolelog.printLine(str(cho_menu_list)+str(cho_menu_result))
    if cho_menu_result==-1:
        jump MC_hub_menuloop
    if cho_menu_result is None:
        jump MC_1_0_end
    $ var_path=persistent.questions.pop(cho_menu_list[cho_menu_result][0])
    call call_event(var_path,True)
    jump MC_hub_mainloop

label MC_hub_devoptions:
    $ cho_menu_result=None
    $ cho_menu_list=[('Script creator','scriptcreator')]
    call adv_cho_menu_call(cho_menu_list,fit_size=3,offer_return=True)
    if cho_menu_result==-1:
        jump MC_hub_menuloop
    if cho_menu_result is None:
        "No developer options available."
        jump MC_hub_menuloop
    $ var_path=cho_menu_list[cho_menu_result][1]
    call expression var_path
    jump MC_hub_mainloop

label MC_hub_debugmenu:
    # TODO implement method of calling any memory label
    return

label MISSING_LABEL_IN_MEMORY:
    show mc turned worr at t11
    mc "Strange. I don't remember a label for this entry..."
    return

label call_event(var_path=['base','main',0,0], eventCallType=1):
    # The universal label for calling events, whether first time or as memories.
    python:
        main_hub_quick_menu = False
        quick_menu = True
        var_value=None # Set all the variables
        cho_menu_list=[]
        cho_menu_result=None
        var_label=None
        fit_size=6
        var_label=MC.generate_memory_label(var_path)
        mem_path_traceback=[]
    $ var_data=MC.load(var_path,rempath=mem_path_traceback)
    if eventCallType!=0: # Call or test
        $ var_time=datetime.datetime.now()
        $ var_data=dict()
    else: # Memory
        if var_data is None:
            $ dump=str(mem_path_traceback)
            $ dump2=str(var_path)
            menu:
                "Error: Memory not found.\n Path: [dump2] Traceback: [dump]"
                "Close program":
                    jump exit_to_menu
                "Remove label from memory":
                    return
                "Raise exception":
                    $ raise Exception('MCAS: Manually raised memory access exception')
                    jump exit_to_menu
        $ var_time=var_data['ctime']
    $ mem_labeltest=renpy.has_label(var_label)
    if not mem_labeltest:
        $ diagnosis="Error: Label {} not found.Unable to determine cause of error.".format(var_label)
        if var_path[0]=='submods':
            if var_path[1]!='data':
                $ diagnosis="Error: Label {} not found.Unable to determine cause of error.".format(var_label)
            elif var_path[2] not in submods_available:
                $ diagnosis="Error: Submod "+var_path[2]+" is not installed."
        menu:
            "[diagnosis]"
            "Close program":
                jump exit_to_menu
            "Remove label drom memory":
                return
            "Raise exception":
                $ raise Exception('MCAS: Manually raised memory access exception')
                jump exit_to_menu
            
    $ allow_skipping = True
    $ config.allow_skipping = True
    $ consolelog.printLine('Calling memory {}'.format(var_label))


    call expression var_label


    $ allow_skipping = False
    $ config.allow_skipping = False
    if eventCallType!=0: # Not a memory
        call adv_cho_menu_call(cho_menu_list,fit_size)
        if eventCallType==1: # First true call (neither memory not test)
            python:
                var_data['final']=cho_menu_result
                var_data['ctime']=var_time
                MC.save(var_path,var_data)
    else: # Memory
        if len(cho_menu_list)!=0:
            python:
                if 'final' in var_data:
                    cho_menu_result=var_data['final']
                    event_var_display=cho_menu_list[cho_menu_result][0]
                else:
                    event_var_display="ERROR: MEMORY NOT FOUND"
            menu:
                "[event_var_display]":
                    pass
    if cho_menu_result is None:
        return
    $ var_call=cho_menu_list[cho_menu_result][1]
    $ eventCallType=cho_menu_list[cho_menu_result][2]
    if eventCallType!=0: # Call or test
        $ persistent.auto_open.append((var_call,eventCallType))
    return

label cho_menu_call(cho_menu_list=[('Example':MC_hub_mainloop)],offer_return=False,disp_text=None):
    # A simple variable-based menu call with an optional return button.
    $ cho_menu_size=len(cho_menu_list)
    if cho_menu_size==0:
        return
    python:
        temp=[(str(cho_menu_list[i][0]),i) for i in range(cho_menu_size)]
        if offer_return:
            temp.append(['Return',-1])
        if disp_text is not None:
            narrator(disp_text,interact=False)
        cho_menu_result=renpy.display_menu(temp)
    return

label adv_cho_menu_call(cho_menu_list=[('Example':MC_hub_mainloop)],fit_size=5,mode=0,is_loopable=False,offer_return=False,disp_text=None):
    # An advanced version of the above, offering multiple pages of choices.
    $ adv_cho_menu_size=len(cho_menu_list)
    if adv_cho_menu_size==0:
        return
    if adv_cho_menu_size<=fit_size:
        call cho_menu_call(cho_menu_list,offer_return,disp_text)
        return
    $ cho_index=0
    label adv_cho_menu_loop:
        python:
            adv_prefixes=[mode<1 and (is_loopable or cho_index>=fit_size),mode>-1 and (is_loopable or cho_index+fit_size<adv_cho_menu_size)]
            adv_cho_menu_list=[('Previous',None)][:adv_prefixes[0]]
            adv_cho_menu_list+=cho_menu_list[cho_index:cho_index+fit_size]
            adv_cho_menu_list+=[('Next',None)][:adv_prefixes[1]]
            if offer_return:
                adv_cho_menu_list.append(['Return',None])
        call cho_menu_call(adv_cho_menu_list)
        if cho_menu_result==0 and adv_prefixes[0]:
            $ cho_index=cho_index-fit_size if cho_index>=fit_size else adv_cho_menu_size-(adv_cho_menu_size%fit_size)
        elif cho_menu_result==fit_size+adv_prefixes[0]:
            $ cho_index=cho_index+fit_size if cho_index+fit_size<adv_cho_menu_size else 0
        elif offer_return and cho_menu_result==len(adv_cho_menu_list)-1:
            $ cho_menu_result=-1
            return
        else:
            $ cho_menu_result+=cho_index-adv_prefixes[0]
            return
        jump adv_cho_menu_loop

image loading_text = ParameterizedText(style="mcas_init_text", xalign=0.5, yalign=0.5)

label loading_screen(disp_text="Loading..."):
    scene black
    # show loading_text "[disp_text]"
    "[disp_text]{nw}"
    $ renpy.music.stop(fadeout=2)
    return

label MC_1_0_end:
    "Unfortunately, there are currently no more questions available."
    "You can, however, return to the point of epiphany and try answering the question differently."
    "You can also replay parts of your playthrough by choosing 'Access memory'."
    "I intend to add more content in the next update, which should hopefully happen next week."
    "Thank you for playing MC After Story 1.0!"
    "r/MCAfterStory is the official subreddit of this mod."
    "You can find the source code on https://github.com/MousePotatoDoesStuff/MCAfterStory"
    jump MC_hub_mainloop