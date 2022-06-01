init -1 python:
    import pickle
    class errorLogClass:
        def __init__(self,filename='LOGDUMP'):
            self.filename=filename
            F=open(basedir+'/'+filename+'.txt','w') # Semi temporary - will replace with proper file making
            F.write("Log dump:\n")
            F.close()
        def add(self,text):
            F=open(basedir+'/'+self.filename+'.txt','a') # Semi temporary - will replace with proper file making
            F.write(text+'\n')
            F.close()
    
    # Hardcoded character pose data - TODO replace with semi-hardcoded MPT script reader

    SCC_chr_list = ['Sayori', 'Yuri', 'Natsuki', 'Monika', 'MC']  # Character list
    SCC_chr = {e: e.lower() for e in SCC_chr_list}
    SCC_raw_moods = {
        'Angry': 'angr',
        'Annoyed': 'anno',
        'Crying': 'cry',
        'Curious': 'curi',
        'Distant': 'dist',
        'Doubtful': 'doub',
        'Flustered': 'flus',
        'Happy': 'happ',
        'Laughing': 'laug',
        'Lightly surprised': 'lsur',
        'Nervous': 'nerv',
        'Neutral': 'neut',
        'Panicked': 'pani',
        'Pouting': 'pout',
        'Sad': 'sad',
        'Seductive': 'sedu',
        'Shocked': 'shoc',
        'Very angry': 'vang',
        'Very surprised': 'vsur',
        'Worried': 'worr',
        'Yandere': 'yand'
    }
    SCC_raw_moods_s2 = {
        'Angry': 'angr',
        'Distant': 'dist',
        'Nervous': 'nerv',
        'Neutral': 'neut',
        'Pouting': 'pout'
    }
    SCC_raw_moods_y2 = {
        'Distant': 'dist',
        'Happy': 'happ',
        'Neutral': 'neut',
        'Sad': 'sad'
    }
    SCC_raw_moods_m2 = {
        'Happy': 'happ',
        'Angry': 'angr',
        'Annoyed': 'anno',
        'Neutral': 'neut',
    }

    SCC_raw_effects = {
        'Default': 't',
        'Slide in from left': 'l',
        'Sink': 's',
        'Hop': 'h',
        'Focus': 'f',
        'Instant': 'i',
        'Dip': 'd',
        'Hop and focus': 'hf'
    }

    SCC_raw_positions = {
        'Center': '11',
        'Left of 2': '21',
        'Right of 2': '22',
        'Left of 3': '31',
        'Center of 3': '32',
        'Right of 3': '33',
        'Leftmost of 4': '41',
        'Left of 4': '42',
        'Right of 4': '43',
        'Rightmost of 4': '44'
    }
    
    # Hardcoded character pose merger (for special pose combinations)

    SCC_poses = {None: {'ERROR: No pose found': 'NULL'}, # Default set of choices (in this case, there is no "default character" so it returns a error when attempted - this is intentional)
                (('character', 'Sayori'),): {'Default': 'turned', 'Special': 'tap'}, # Special sets of choices (in this case, Sayori tapping her fingers)
                (('character', 'Yuri'),): {'Default': 'turned', 'Special': 'shy'},
                (('character', 'Natsuki'),): {'Default': 'turned', 'Special': 'cross'},
                (('character', 'Monika'),): {'Default': 'forward', 'Special': 'lean'},
                (('character', 'MC'),): {'Default': 'turned'}} # y no MC special pose lol

    SCC_eyecolor = {
        None: {'Default': ''}, (('character', 'MC'),): {'Yellow': 'yelo', 'Red': 'red'}
    }

    SCC_outfits = {None: {'School uniform': 'uniform', 'Casual outfit': 'casual'}}

    SCC_moods = {
        None: SCC_raw_moods,
        (('character', 'Sayori'), ('pose', 'Special')): SCC_raw_moods_s2,
        (('character', 'Yuri'), ('pose', 'Special')): SCC_raw_moods_y2,
        (('character', 'Monika'), ('pose', 'Special')): SCC_raw_moods_m2,
    }

    SCC_mouth={None:{'Open mouth':'om','Closed mouth':'cm','default':''}}
    SCC_eyes={None:{'Open eyes':'oe','Closed eyes':'ce','default':''}}

    # Input group class

    class SC_Input_Group:
        def __init__(self, name, dependencies, defaultOnly=False):
            self.name = name
            if defaultOnly:
                dependencies = {None: dependencies}
            if None not in dependencies:
                raise Exception(name + " does not have default (None) setting!") # ALWAYS include a default setting in dependencies!
            self.dependencies = dependencies
            self.current = None
            self.container = self.dependencies[self.current]
            (self.chosen, self.value) = max(self.container.items())
            return

        def __repr__(self):
            return '{}:{}'.format(self.chosen, self.value)

        def copy(self): # Copies data into a new input group, making sure the two don't share mutable containers.
            X=SC_Input_Group(self.name, self.dependencies)
            X.current=self.current #These two are not treated as mutable.
            X.container=self.container
            (X.chosen, X.value) = (self.chosen, self.value)
            return X

        def get_options(self):
            return [e for e in self.dependencies]

        def choose(self, choice):
            self.chosen = choice
            self.value = self.container[choice]
            return

        def adjust_for(self, dep_v): # Chooses the set of options available for character/pose/etc. For example, special poses have a limited number of moods.
            if dep_v == self.current:
                return
            self.current = dep_v
            maxsize = 0
            container = self.dependencies[None]
            for E in self.dependencies: # Option goes through all the dependencies to check if any is satisfied. Conflicts are resolved by choosing the longer dependency.
                confirmed = True        # It doesn't scale well, but with a maximum of 5 different dependencies so far, it doesn't have to.
                if E is None or len(E) <= maxsize: # Dependency is default or too short.
                    continue
                for f in E:
                    if f[0] in dep_v and dep_v[f[0]] != f[1]:
                        confirmed = False
                        break
                if not confirmed:
                    continue
                container = self.dependencies[E]
                maxsize = len(E)
            self.container = container
            # errorLog.add('Checking if {} can be {}'.format(self.name,self.chosen))
            if self.chosen not in self.container:
                (self.chosen, self.value) = max(self.container.items()) # If current option is not available given new set of dependencies, chooses that with maximum value of item pair. (arbitrary decision)
                # errorLog.add('{} set to {}'.format(self.name,self.chosen))
            else:
                self.value = self.container[self.chosen]
            return

    # Build list of input groups. Again, all hardcoded for now.

    sc_all_inputs = [
        SC_Input_Group('character', SCC_chr, True),
        SC_Input_Group('pose', SCC_poses),
        SC_Input_Group('outfit', SCC_outfits),
        SC_Input_Group('eye color', SCC_eyecolor),
        SC_Input_Group('mood', SCC_moods),
        SC_Input_Group('mouth', SCC_mouth),
        SC_Input_Group('eyes', SCC_eyes),
        SC_Input_Group('effect', SCC_raw_effects, True),
        SC_Input_Group('position', SCC_raw_positions, True)
    ]
    SCC_map = {sc_all_inputs[i].name:i for i in range(len(sc_all_inputs))}


    class SC_Input_Manager: # (SCIM) Manages inputs. Also holds information about 1 character in 1 frame.
        def __init__(self,source=None):
            if source is None: # Generates new SCIM.
                self.inputs = [e.copy() for e in sc_all_inputs]
                self.save = None
                self.isApplicable = False
                self.current = 0
                self.cur_scroll = 0
                self.cur_size = None
                self.apply_dependencies() # Needed to initialise a default setting.
            else: # Generates copy of existing SCIM.
                self.inputs = [e.copy() for e in source.inputs]
                self.save = source.save
                self.isApplicable = source.isApplicable
                self.current = source.current
                self.cur_scroll = source.cur_scroll
                self.cur_size = source.cur_size
            return
        
        def get_name(self): # Returns the character's name.
            return self.inputs[0].chosen
        
        def copy(self): # Creates a copy of the structure.
            return SC_Input_Manager(self)
        
        def get_categories(self):
            return [(i,self.inputs[i].name) for i in range(len(self.inputs))]
        
        def set_scroll_position(self,size=10): # ...I'll get back to this one.
            svar=self.cur_scroll
            if svar is None:
                X=self.inputs[self.current]
                Y=list(X.container.keys())
                Y.sort()
                cho=X.chosen 
                if cho in Y:
                    svar=Y.index(cho)
                else:
                    svar=0
                svar-=svar%size
                self.cur_scroll=svar
            return

        
        def get_category_options(self,size=10): # Retrieves options for the currently selected category (or their subset)
            self.set_scroll_position()
            svar=self.cur_scroll
            startpoint=svar-svar%size
            X=self.inputs[self.current]
            Y=list(X.container.keys())
            Y.sort()
            return Y[startpoint:startpoint+size]
        
        def make_scroll(self,nx=False,size=10): # Allows switching through pages of options for the character. Who needs a scrollbar?
            def scroll():
                X=self.inputs[self.current]
                Y=list(X.container.keys())
                svar=self.cur_scroll
                if svar is None:
                    return
                if nx:
                    svar+=size
                    if svar>len(Y):
                        return
                    self.cur_scroll=svar
                else:
                    svar-=size
                    if svar<0:
                        return
                    self.cur_scroll=svar
                self.make_open_submenu(self.current)()
            return scroll

        
        def is_current_setting(self, value): # Checks if this is the currently chosen setting for the current category (used for graying out)
            X=self.inputs[self.current]
            return X.chosen==value
        
        def get_names(self): # Get category names.
            return [e.name() for e in self.inputs]

        def apply_dependencies(self): # Applies dependencies to generate a new valid combination
            values = dict()
            # errorLog.add('Adjusting...')
            for E in self.inputs:
                E.adjust_for(values)
                values[E.name] = E.chosen
            return

        def __repr__(self):
            return str([e.chosen for e in self.inputs])
        
        def display(self):
            return self.turn_into_command()
        
        def turn_into_command(self,side_mode=False): # Generates a Renpy-runnable command for either the character editor mode or the scene editor mode.
            if side_mode:
                IN=sc_all_inputs[:-2]
                OUT=[self.inputs[i].value for i in range(len(IN))]
                command=" ".join([e for e in OUT if e not in ('',None)])
                location='t33'
            else:
                location=self.inputs[-2].value+self.inputs[-1].value
                IN=sc_all_inputs[:-2]
                OUT=[self.inputs[i].value for i in range(len(IN))]
                command=" ".join([e for e in OUT if e not in ('',None)])
            return command,location

        def make_open_submenu(self, k): # CONNECTION This part manages swapping between submenus...or at least it's supposed to.
            def sc_open_submenu():
                renpy.hide_screen("sc_edit_menu")
                if k == -1:
                    self.__init__()
                    return
                if k!=self.current:
                    self.cur_scroll = None
                    self.current = k
                    self.set_scroll_position()
                renpy.show_screen("sc_edit_menu")
                return

            return sc_open_submenu

        def make_close_submenu(self, choice): # CONNECTION This part manages applying changes to the model...or at least it's supposed to.
            def sc_close_submenu():
                renpy.hide_screen("sc_edit_menu")
                renpy.show_screen("sc_edit_menu")
                if choice is None:
                    return
                self.inputs[self.current].choose(choice)
                self.apply_dependencies()
                return

            return sc_close_submenu


    class SC_Frame: # Data class that manages one frame
        def __init__(self, chr_data, tx='', bg=None, sound_var=None):
            self.tx = tx
            self.bg = bg
            self.sound = sound_var
            self.characters = dict()
            k = 0
            for e in chr_data:
                name = e.inputs[0].chosen
                self.characters[name] = e
                k += 1
            return

        def copy(self): # Create copy of frame.
            fr2 = SC_Frame([], self.tx, self.bg, self.sound)
            fr2.characters = {e[0]:e[1].copy() for e in self.characters.items()}
            return fr2
        
        def makeCopyTo(self,charKey):
            def copyTo():
                sc_mgr.__init__(self.characters[charKey])
                renpy.hide_screen("sc_get_character")
                sc_mgr.make_close_submenu(None)()
                return
            return copyTo
        
        def makeImport(self,mgr,charKey):
            def Import():
                self.characters[charKey]=SC_Input_Manager(mgr)
                renpy.hide_screen("sc_get_character")
                sc_mgr.make_open_submenu(sc_mgr.current)
                return
            return Import
        
        def makeDelete(self,mgr,charKey):
            def Delete():
                if charKey not in sc_ene.curframe.characters:
                    return
                self.characters.pop(charKey)
                errorLog.add('Deleting {}...'.format(charKey))
                renpy.hide(charKey.lower())
                renpy.hide_screen("sc_get_character")
                sc_mgr.make_open_submenu(sc_mgr.current)
                return
            return Delete

        def display(self):
            # TODO store prev state
            # errorLog.add('Displaying...')
            for el in self.characters.values():
                disp=el.display()
                errorLog.add(str(el)+str(disp))
                loc=globals()[disp[1]]
                renpy.show(disp[0],[loc], zorder=3)
            try:
                speaker=globals()[self.tx[0]]
            except:
                speaker=self.tx[0]
            try:
                renpy.say(speaker,self.tx[1])
            except:
                renpy.say('System','An exception has occured. Please change sayer name and/or message.')
            return

        def apply_command(self, raw_command): # Apply a command to the frame (e.g. show character, change background) - currently unused
            L = [e for e in raw_command.split(' ') if e != '']
            if L[0] not in self.characters:
                k = len(self.chr_data)
            return
        
        def apply_text(self):
            renpy.hide_screen("sc_text_input")
            if not text_input:
                return
            self.tx=(self.tx[0],text_input)
            renpy.jump_out_of_context("scriptcreator_scene")
        
        def apply_text_name(self):
            renpy.hide_screen("sc_name_input")
            if not text_input:
                return
            self.tx=(text_input,self.tx[1])
            renpy.jump_out_of_context("scriptcreator_scene")


    class SC_Scene:
        def __init__(self, frames, cur_index=0):
            self.frames = frames
            self.cur_index = cur_index
            self.curframe = None
            self.prev_frame = None
            return
        
        def isNotMinimal(self):
            return len(self.frames)>1

        def get_frame(self, ind=0):
            return self.frames[ind]

        def get_curframe(self):
            if self.cur_index not in range(0,len(self.frames)):
                return None
            return self.frames[self.cur_index]
        
        def display_curframe(self,check_characters=True):
            self.curframe=self.frames[self.cur_index]
            if self.prev_frame is not None:
                for e in self.prev_frame.characters:
                    if e not in self.curframe.characters:
                        errorLog.add('Hiding {}...'.format(e))
                        renpy.hide(e.lower())
            self.curframe.display()
            self.frames[self.cur_index]=self.curframe
            sc_ene.cur_index+=1
            self.prev_frame=self.curframe
            return

        def set_curframe(self,fr):
            self.frames[self.cur_index]=fr
            self.curframe=fr
            return
        
        def duplicate_curframe(self):
            self.frames.insert(self.cur_index,self.frames[self.cur_index].copy())
            self.cur_index+=1
            self.curframe=self.frames[self.cur_index]
            return
        
        def delete_curframe(self):
            if self.isNotMinimal():
                self.frames.pop(self.cur_index)
                if self.cur_index==len(self.frames):
                    self.cur_index-=1
                self.curframe=self.frames[self.cur_index]
            else:
                Show(screen="name_input", message="Cannot delete only frame in scene.", ok_action=Return())
            return


# Menus that allow editing:
default sc_quick_menu=False
default command=''
default sc_mgr=None
default sc_ene=None
default text_input=''

screen sc_quick_menu():

    # Ensure this appears on top of other screens.
    zorder 100

    if sc_quick_menu:
        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 0.995

            textbutton _("Characters") action ShowMenu(screen="sc_edit_menu")
            textbutton _("Duplicate") action sc_ene.duplicate_curframe
            textbutton _("Delete") action [ShowMenu(screen="confirm",message="Delete current frame?",yes_action=[Hide("confirm"), sc_ene.delete_curframe, ReturnToScene],
            no_action=Hide("confirm")),SensitiveIf(sc_ene.isNotMinimal())]
            textbutton _("EditSpeaker") action ShowMenu(screen="sc_name_input",
            ok_action=sc_ene.curframe.apply_text_name)
            textbutton _("EditText") action ShowMenu(screen="sc_text_input",
            ok_action=sc_ene.curframe.apply_text)
            textbutton _("Settings") action ShowMenu('preferences')

screen sc_name_input(ok_action):

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

            input default sc_ene.curframe.tx[0]+'?' value VariableInputValue("text_input") length 20 # allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _"
            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action

screen sc_text_input(ok_action):

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

            label _('Edit text'):
                style "confirm_prompt" # MCAS
                xalign 0.5

            input default 'pizza' value VariableInputValue("text_input") length 1000 # allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _"
            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action


screen sc_navigation():
    vbox:
        style_prefix "navigation"

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.8

        spacing gui.navigation_spacing

        textbutton _('Load from scene') action ShowMenu(screen='sc_get_character',make_ok_action=sc_ene.curframe.makeCopyTo)
        for e in sc_mgr.get_categories():
            textbutton _(e[1].capitalize()) action [sc_mgr.make_open_submenu(e[0]),ShowMenu('sc_edit_menu'),SensitiveIf(sc_mgr.current!=e[0])]
        textbutton _('Apply {}'.format(sc_mgr.get_name())) action sc_ene.curframe.makeImport(sc_mgr,sc_mgr.get_name())
        textbutton _('Remove {}'.format(sc_mgr.get_name())) action [sc_ene.curframe.makeDelete(sc_mgr,sc_mgr.get_name()),SensitiveIf(sc_mgr.get_name() in sc_ene.curframe.characters)]

screen sc_get_character(make_ok_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            if sc_ene.curframe is None:
                label _('Cannot import character.'):
                    style "confirm_prompt"
                    xalign 0.5
                textbutton _("OK") action Return()
            else:
                label _('Import character\n({}found):'.format(len(sc_ene.curframe.characters.keys()))):
                    style "confirm_prompt"
                    xalign 0.5
                for e in sc_ene.curframe.characters.keys():
                    textbutton _(e) action [sc_ene.curframe.makeCopyTo(e),Hide('sc_get_character')]
                xalign .5
                yalign .5
                spacing 30
                textbutton _("Don't import") action Hide('sc_get_character')
                
                    


screen sc_options_menu():
    frame:
        vbox:
            style "game_menu_content_frame"

            xpos gui.navigation_xpos
            yalign 0.8

            spacing gui.navigation_spacing
            # textbutton _(str(sc_mgr.cur_scroll))
            for e in sc_mgr.get_category_options():
                textbutton _(e.capitalize()) action [sc_mgr.make_close_submenu(e),ShowMenu('sc_edit_menu'),SensitiveIf(not sc_mgr.is_current_setting(e))]
            hbox:
                textbutton _('<<') action [sc_mgr.make_scroll(0),ShowMenu('sc_edit_menu')]
                textbutton _('>>') action [sc_mgr.make_scroll(1),ShowMenu('sc_edit_menu')]

init python:
    def ReturnToScene():
        renpy.jump_out_of_context("scriptcreator_scene")
        return
    def MakeReturnWithLambda():
        renpy.jump_out_of_context("scriptcreator_scene")
        return



screen sc_edit_menu(scroll=None):

    # Add the backgrounds.

    key "mouseup_3" action sc_mgr.make_open_submenu(-1)
    add gui.game_menu_background

    style_prefix "game_menu"

    frame:
        style "game_menu_outer_frame"

        hbox:

            # Reserve space for the navigation section.
            vbox:
                style "game_menu_navigation_frame"
            vbox:
                use sc_options_menu
            vbox:
                add sc_mgr.turn_into_command(True)[0]


    label _(sc_mgr.turn_into_command())
    label _(sc_mgr.turn_into_command(True))
    use sc_navigation

    textbutton _("Exit without inserting"):
        style "return_button"

        action [Return(),ReturnToScene]
# This is where the runtime begins.

label scriptcreator:
    stop music
    scene black
    python:
        dialog_content='''The Dialog Editor is an experimental scene editor.
Currently there are no options to save or export generated content,
and there are yet-to-be-solved issues requiring extensive changes.

However, you can use it as a partial cheat sheet for MPT.'''
    call screen dialog(dialog_content, [Hide("dialog"), Return()])
    python:
        errorLog=errorLogClass()
        SCC_cfs={'Sayori':s,'Yuri':y,'Natsuki':n,'Monika':m,'MC':mc}
        try:
            F=open(basedir+'/game/default.scrpt','r') # Semi temporary - will replace with proper file making
            sc_ene=pickle.load(F)
        except:
            X=[]
            chr_data_1=[
                    ]
            scene_text_1=('','TEST')
            X.append(SC_Frame(chr_data_1,scene_text_1))
            sc_ene=SC_Scene(X)
label scriptcreator_mainmenu:
    menu:
        "Play scene":
            call scriptcreator_play from _call_scriptcreator_play
        "Return to [persistent.mcname]":
            stop music
            python:
                with open(basedir+'/game/default.scrpt','w') as F:
                    pickle.dump(sc_ene,F)
            return
    jump scriptcreator_mainmenu
label scriptcreator_play:
    python:
        errorLog.add(str(sc_mgr))
        sc_mgr=SC_Input_Manager()
        sc_ene.cur_index=0
    call quick_menu_choice(2) from _call_quick_menu_choice
    scene black
    label scriptcreator_scene:
        python:
            sc_ene.display_curframe()
        if sc_ene.cur_index==len(sc_ene.frames):
            scene black
            $ sc_ene.prev_frame=None
            menu:
                "Rewind scene":
                    jump scriptcreator_play
                "Exit scene":
                    call quick_menu_choice(0) from _call_quick_menu_choice_1
                    return
        jump scriptcreator_scene

