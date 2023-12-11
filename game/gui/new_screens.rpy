screen text_input_scr(message, ok_action, scmaxlen=12, scletters='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'):

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

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            input default "" value VariableInputValue("text_input") length scmaxlen allow scletters

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action

screen selection_scr(message, options=['Alpha','Aleph','Alert','Derp']+['A'*(i%4+1)+'B'*(i//4+1) for i in range(16)], scmaxlen=20, scletters='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_'):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message+text_input):
                style "confirm_prompt"
                xalign 0.5

            input default "" value VariableInputValue("text_input") length scmaxlen allow scletters
            for el in filter_buttons(options, text_input):
                hbox:
                    xalign 0.5
                    spacing 100

                    textbutton _(el) action [Play("sound", gui.activate_sound), MakeScreenHideFunction('selection_scr')]

screen menu_option_selector(entries):
    vbox:
        hbox:
            textbutton _("<Prev") action NullAction()
            textbutton _("Next>") action NullAction()
        for el in [None]+list(EDR_MC.categories.keys()):
            textbutton _(str(el)) action NullAction()

screen memory:
    tag menu
    
    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("Run memory"), scroll=("vpgrid" if gui.history_height else "viewport")):
        
        style_prefix "history"
        hbox:
            vbox:
                hbox:
                    textbutton _("<Prev") action NullAction()
                    textbutton _("Next>") action NullAction()
                for el in [None]+list(EDR_MC.categories.keys()):
                    textbutton _(str(el)) action NullAction()
            vbox:
                for el in EDR_MC.list_events():
                    textbutton _(el) action MakeCallMemoryFunction(el,True,'memory')

screen run_label:
    tag menu
    
    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("Run label"), scroll=("vpgrid" if gui.history_height else "viewport")):
        
        style_prefix "history"
        hbox:
            vbox:
                hbox:
                    textbutton _("<Prev") action NullAction()
                    textbutton _("Next>") action NullAction()
                for el in [None]+list(EDR_MC.categories.keys()):
                    textbutton _(str(el)) action NullAction()
            vbox:
                for el in mc_str.available_labels:
                    textbutton _(el) action MakeCallMemoryFunction(el,False,'run_label')
