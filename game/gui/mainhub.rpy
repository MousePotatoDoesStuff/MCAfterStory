default m_index=0
default dump=''
init -10 python:
    def MakeJumpTo(dest):
        def X():
            renpy.jump(dest)
            return
        return X
init -9 python:
    mc_str=DokiEntity()
    

image code_void:
    topleft
    "mod_assets/code_void.png"


label init_memories:
    python:
        test_ev_data={'label':'test_01'}
        EDR_MC.easy_set('test','test_01',[])

label init_main:

label init_mainloop:
    $ menu_navmanager.SetCurrent('hub')
    $ quickmenu_navmanager.SetCurrent('hub')
    call quick_menu_choice()
    $ mc_str.retrieve_memory('test')
    call quick_menu_choice
    python:
        current=LOCAL.get('technical',"current",None)
        if current is None:
            current=mc_str.get_from_queue()
    "[current]"
    if current is not None:
        call run_memlabel(current[0],current[1])
        python:
            current=None
            LOCAL.set('technical',"current",None)
    $ text_input=str(len(mc_str.persistent_queue))
    if submod_name is not None:
        call submod_mainhub
    else:
        scene bg black
        stop music
        show mc turned casual worr at t11
    $ quick_menu=True
    $ menu_navmanager.SetCurrent('hub')
    $ quickmenu_navmanager.SetCurrent('hub')
    menu:
        "[quickmenu_navmanager.current]"
        "Refresh":
            pass
        "Swap quick menus":
            $ m_index=1-m_index
            call quick_menu_choice
        "First":
            call run_memlabel('test_01',False)
        "Recall":
            call run_memlabel('test_01',True)
        "Wipe memory":
            $ mc_str.memories=MemoryManager()
            "Memory wiped."
    $ mcname="MC"
    jump init_mainloop

    "WARNING: CODE EXECUTION PASSED INTO FORBIDDEN AREA. SHUTDOWN INITIATED."
    $ renpy.quit()

label run_memlabel(lbl,memory=False):
    python:
        temp_data={'memory':memory}
        menu_navmanager.SetCurrent('memory' if memory else 'active')
        quickmenu_navmanager.SetCurrent('memory' if memory else 'active')
        # Get event data with label
        event_data=EDR_MC.get(lbl)
        # If label is not ephemeral, save it as persistent
        ephemeral=memory or event_data.get('ephemeral',False)
        if not ephemeral:
            LOCAL.set('technical',"current",(lbl,memory),autosave=True)
        # Error reporting
        error=None
        mem_data = None
        if memory: # Recalling a memory
            mem_main=mc_str.retrieve_memory(lbl)
            if mem_main is None:
                error="Memory not present."
            else:
                (mem_timestamp,mem_timedex,mem_data)=mem_main.retrieveLast()
                start_timestamp=mem_timestamp
                name_memory=mc_str.retrieve_memory('names')
        else: # Running a label
            start_timestamp=mc_str.clock.getTime()
            mem_data = dict()
            mem_data['label']=lbl
            if 'names' in event_data and False: # TODO
                chr_names=event_data['names']
                for (char,name) in chr_names.items(): # {"co":"Chosha Sonyu"}
                    name_memory=mc_str.retrieve_memory('names')
                    name_lastentry=mc_str.retrieveLast(start_timestamp).copy()
                    updated=False
                    if char not in name_memories:
                        name_lastentry[char]=name
                    exec('{}="{}"'.format(char,name))
    if error is not None: # Advanced Error Display System [LMAO]
        "[error]"
        return
    call expression lbl # LET'S FUCKING GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    $ end_timestamp=mc_str.clock.getTime() # It's time to stop
    python:
        if not ephemeral:
            LOCAL.set('technical',"current",None,autosave=True)
        if memory:
            pass
        else:
            # mem_data['t_start']=start_timestamp # Yeah...I'm pretty sure this is redundant.
            mem_data['t_end']=end_timestamp
            mc_str.create_memory(lbl,start_timestamp,mem_data,event_data.get('serial'))
        followup=event_data.get('followup',[])
        mc_str.apply_to_queue(followup,ephemeral)
    return

label test_01:
    $ temp = str(test_ev_data)
    mc "config.developer=[config.developer]"
    return

label universal_return:
    return