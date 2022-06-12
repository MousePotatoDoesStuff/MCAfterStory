default persistent.auto_open=list()
default persistent.memories=dict()
default persistent.current_memory=None

image code_void:
    topleft
    "mod_assets/code_void.png"

label jump_MC_epiphany:
    # Start 
    if persistent.epiphany_stage==1:
        call mem_initiate # Initializes MC's memory system and saves the intro.
        call mem_save([0])
        call mem_save([1])
        call mem_save([2])
        call mem_save([3])
        $ persistent.auto_open.append(([4],True)) # Instructs the loop to immediately load this label.
        jump MC_start
        call mem_dump() #Test dump.

label MC_start:
    "[persistent.epiphany_stage]"
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

label MC_hub_mainloop:
    $ mc_name=persistent.mcname
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
        call call_event(var_path,isFirstCall)
        jump MC_hub_mainloop
    play music m1
    scene code_void
    show mc turned worr at t33
    menu:
        "Access memory":
            python:
                var_X=persistent.memories['base']['main']
                var_Y=[]
                for var_k in var_X:
                    var_E=var_X[var_k]
                    var_Y.extend([(var_k,var_e) for var_e in var_E])
                var_n=len(var_Y)
                cho_menu_list=[]
                var_i=0
            while var_i!=var_n:
                $ var_E=var_Y[var_i]
                $ var_label='MISSING_LABEL_IN_MEMORY'
                $ temp = 'Chapter {}, part {}'.format(var_E[0],var_E[1])
                $ cho_menu_list.append((temp,list(var_E)))
                $ var_i+=1
            call cho_menu_call(cho_menu_list)
            $ var_path=cho_menu_list[cho_menu_result][1]
            scene black
            "Loading memory...{w=1}{nw}"
            call call_event(var_path,False)
            scene black
            "Leaving memory...{w=1}{nw}"
        "Ask question":
            pass
        "Dump memory":
            call mem_dump()
    jump MC_hub_mainloop

label MISSING_LABEL_IN_MEMORY:
    mc "Strange. I don't remember a label for this entry..."

label call_event(var_path=['base','main',0,0], isFirstCall=True):
    $ var_value=None # Set all the variables
    $ cho_menu_list=[]
    $ cho_menu_result=None
    $ var_label=None
    $ fit_size=6
    if isFirstCall:
        pass # This one does nothing for now, I forgor what's it for
    call mem_to_label(var_path) #Get callable label
    call expression var_label # Call label
    if isFirstCall:
        call adv_cho_menu_call(cho_menu_list,fit_size)
        call mem_save(var_path,{'final':cho_menu_result})
        if cho_menu_result is None:
            return
        $ var_call=cho_menu_list[cho_menu_result][1]
        $ isFirstCall=cho_menu_list[cho_menu_result][2]
        if isFirstCall:
            $ persistent.auto_open.append((var_call,True))
    else:
        call mem_load(var_path)
        if len(cho_menu_list)!=0:
            $ cho_menu_result=cho_menu_list[var_value[1]['final']][0] if (var_value[0] and 'final' in var_value[1]) else "ERROR: MEMORY NOT FOUND"
            menu:
                "[cho_menu_result]":
                    pass
    return

label cho_menu_call(cho_menu_list=[('Example':MC_hub_mainloop)]):
    $ cho_menu_size=len(cho_menu_list)
    if cho_menu_size==0:
        return
    python:
        temp=[(str(cho_menu_list[i][0]),i) for i in range(cho_menu_size)]
        cho_menu_result=renpy.display_menu(temp)
    return

label adv_cho_menu_call(cho_menu_list=[('Example':MC_hub_mainloop)],fit_size=5,mode=0,is_loopable=False):
    $ adv_cho_menu_size=len(cho_menu_list)
    if adv_cho_menu_size==0:
        return
    if adv_cho_menu_size<=fit_size:
        call cho_menu_call(cho_menu_list)
        return
    $ cho_index=0
    label adv_cho_menu_loop:
        python:
            adv_prefixes=[mode<1 and (is_loopable or cho_index>=fit_size),mode>-1 and (is_loopable or cho_index+fit_size<adv_cho_menu_size)]
            adv_cho_menu_list=[('Previous',None)][:adv_prefixes[0]]
            adv_cho_menu_list+=cho_menu_list[cho_index:cho_index+fit_size]
            adv_cho_menu_list+=[('Next',None)][:adv_prefixes[1]]
        call cho_menu_call(adv_cho_menu_list)
        if cho_menu_result==0:
            $ cho_index=cho_index-fit_size if cho_index>=fit_size else adv_cho_menu_size-(adv_cho_menu_size%fit_size)
        elif cho_menu_result==fit_size+adv_prefixes[0]:
            $ cho_index=cho_index+fit_size if cho_index+fit_size<adv_cho_menu_size else 0
        else:
            $ cho_menu_result+=cho_index-adv_prefixes[0]
            "Chosen option [cho_menu_result]"
            return
        jump adv_cho_menu_loop