label init_menu():
    stop music
    $ config.skipping = False
    $ config.allow_skipping = False
    $ allow_skipping = False #Not completely sure why skipping has to be explicitly disabled, but apparently it does..
    $ t=-1
    scene black
    python: #Variable initialization here. Important to note, these initialize at the start of the mini-game.
        init_menu_location=0
        # Main loop for drawing and selecting words
        while True:
            if init_menu_location==0:
                open_game="???" if persistent.epiphany_stage==1 else "Open game"
                cur_y=120
                ui.textbutton(open_game, clicked=ui.returns(0), text_style="mcas_init_text", xpos=160, ypos=cur_y)
                cur_y=cur_y+40
                ui.textbutton("Generate backup data", clicked=ui.returns(1), text_style="mcas_init_text", xpos=160, ypos=cur_y)
                cur_y=cur_y+40
                ui.textbutton("Restore persistent data from backup", clicked=ui.returns(2), text_style="mcas_init_text", xpos=160, ypos=cur_y)
                cur_y=cur_y+40
                ui.textbutton("Erase data and start over", clicked=ui.returns(3), text_style="mcas_init_text", xpos=160, ypos=cur_y)
                t = ui.interact()
                if t==0:
                    break
                elif t==3:
                    delete_all_saves()
                    renpy.loadsave.location.unlink_persistent()
                    renpy.persistent.should_save_persistent = False
                    renpy.utter_restart()
##################This block controls what happens when words are selected.############################
    "[t]"
##################End of main loop.##################################################################
    $ config.allow_skipping = True
    $ allow_skipping = True
    stop music fadeout 2.0
    show black as fadeout:
        alpha 0
        linear 1.0 alpha 1.0
    pause 1.0
    return