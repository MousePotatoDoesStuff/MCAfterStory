label versioncheck(versionstring):
    $ result='Success'
    if versionstring is None:
        return
    python:
        vls=versionstring.split('.')
        try:
            vlist=[int(e) for e in vls]
        except ValueError:
            result="InvalidVersionID"
    if result!="Success":
        return
    if vlist[0]<4:
        "You are attempting to reload a persistent savefile for an extremely early version of MCAS."
        "Versions 1.0 to 3.0 are not compatible due to their limited content and data structure differences."
        menu:
            "Would you like to delete your save data and start over?"
            "Yes, delete my existing data.":
                "Deleting save data...{nw}"
                python:
                    delete_all_saves()
                    renpy.loadsave.location.unlink_persistent()
                    renpy.persistent.should_save_persistent = False
                    renpy.utter_restart()
            "No, exit game.":
                $ renpy.quit()