default persistent.auto_open=list() # DO NOT TOUCH THESE. YOU MIGHT BREAK SOMETHING.
default persistent.current_memory=None
default persistent.memdict=dict()
default persistent.questions=dict()
default persistent.dump_counter=0
default persistent.epiphany_stage=0

# Hello, player.
# Or perhaps even more - a fellow modder?
# Either way, thank you for taking the time to look at the code.
# Sorry for the mess.

image code_void:
    topleft
    "mod_assets/code_void.png"

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
                MC.save([i],{'ctime':var_time})
            persistent.auto_open.append(([4],True)) # Instructs the loop to immediately load this label.
            persistent.epiphany_stage=2
            renpy.save_persistent()
    jump MC_start

label MC_start: # This part initiates the other stuff.
    python:
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
    $ quick_menu = True
    $ style.say_dialogue = style.normal
    $ in_sayori_kill = None
    $ allow_skipping = False
    $ config.allow_skipping = False

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
        $ var_path,isFirstCall=persistent.current_memory
        if not isFirstCall:
            menu:
                "Continue memory replay?"
                "Yes":
                    pass
                "No":
                    jump MC_hub_mainloop
        call call_event(var_path,isFirstCall) from _call_call_event
        $ persistent.current_memory=None
        jump MC_hub_mainloop
    play music m1
    scene code_void
    show mc turned worr at t33
    menu:
        "Access memory":
            python:
                var_X=MC.load(['base','main'], useMempath=False)
                if var_X is not None:
                    var_Y=[]
                    for var_k in var_X:
                        var_E=var_X[var_k]
                        var_Y.extend([(var_k,var_e) for var_e in var_E])
                    var_n=len(var_Y)
                    cho_menu_list=[]
                    var_i=0
            if var_X is None:
                "Unable to access main memory."
                jump MC_hub_mainloop
            while var_i!=var_n:
                $ var_E=var_Y[var_i]
                $ var_label='MISSING_LABEL_IN_MEMORY'
                $ temp = 'Chapter {}, part {}'.format(var_E[0],var_E[1])
                $ cho_menu_list.append((temp,list(var_E)))
                $ var_i+=1
            call adv_cho_menu_call(cho_menu_list,offer_return=True) from _call_adv_cho_menu_call
            if cho_menu_result==-1:
                jump MC_hub_mainloop
            $ var_path=cho_menu_list[cho_menu_result][1]
            scene black
            "Loading memory...{w=1}{nw}"
            call call_event(var_path,False) from _call_call_event_1
            scene black
            "Leaving memory...{w=1}{nw}"
        "Ask question":
            $ cho_menu_result=None
            $ cho_menu_list=list(persistent.questions.items())
            call adv_cho_menu_call(cho_menu_list,fit_size=3,offer_return=True) from _call_adv_cho_menu_call_1
            if cho_menu_result==-1:
                jump MC_hub_mainloop
            if cho_menu_result is None:
                jump MC_1_0_end
            $ var_path=persistent.questions.pop(cho_menu_list[cho_menu_result][0])
            call call_event(var_path,True) from _call_call_event_1
        "Dump memory":
            $ MC.dump_memory([],str(persistent.dump_counter))
            $ persistent.dump_counter+=1
        "Reset to start of epiphany":
            call loading_screen("Resetting to start of epiphany...") from _call_loading_screen
            $ persistent.epiphany_stage=1
            $ renpy.save_persistent()
            $ renpy.utter_restart()
        "Exit to menu":
            call loading_screen("Saving data...") from _call_loading_screen_1
            $ renpy.save_persistent()
            $ renpy.utter_restart()

    jump MC_hub_mainloop

label MISSING_LABEL_IN_MEMORY:
    show mc turned worr at t11
    mc "Strange. I don't remember a label for this entry..."
    return

label call_event(var_path=['base','main',0,0], isFirstCall=True):
    # The universal label for calling events, whether first time or as memories.
    python:
        var_value=None # Set all the variables
        cho_menu_list=[]
        cho_menu_result=None
        var_label=None
        fit_size=6
        var_label=MC.generate_memory_label(var_path)
    if isFirstCall:
        $ var_time=datetime.datetime.now()
    else:
        $ var_data=MC.load(var_path)
        $ var_time=var_data['ctime']
    call expression var_label from _call_expression_11 # Call label
    if isFirstCall:
        call adv_cho_menu_call(cho_menu_list,fit_size) from _call_adv_cho_menu_call_2
        $ MC.save(var_path,{'final':cho_menu_result,'ctime':var_time})
    else:
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
    $ isFirstCall=cho_menu_list[cho_menu_result][2]
    if isFirstCall:
        $ persistent.auto_open.append((var_call,True))
    return

label cho_menu_call(cho_menu_list=[('Example':MC_hub_mainloop)],offer_return=False):
    # A simple variable-based menu call with an optional return button.
    $ cho_menu_size=len(cho_menu_list)
    if cho_menu_size==0:
        return
    python:
        temp=[(str(cho_menu_list[i][0]),i) for i in range(cho_menu_size)]
        if offer_return:
            adv_cho_menu_list.append(['Return',None])
        cho_menu_result=renpy.display_menu(temp)
    return

label adv_cho_menu_call(cho_menu_list=[('Example':MC_hub_mainloop)],fit_size=5,mode=0,is_loopable=False,offer_return=False):
    # An advanced version of the above, offering multiple pages of choices.
    $ adv_cho_menu_size=len(cho_menu_list)
    if adv_cho_menu_size==0:
        return
    if adv_cho_menu_size<=fit_size:
        call cho_menu_call(cho_menu_list) from _call_cho_menu_call
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
        call cho_menu_call(adv_cho_menu_list) from _call_cho_menu_call_1
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

label loading_screen(text="Loading..."):
    scene black
    # show loading_text "[text]"
    "[text]{nw}"
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