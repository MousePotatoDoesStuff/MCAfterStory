init -10 python:
    class CharacterEntry:
        def __init__(self,name,char,global_namevar=None,global_charvar=None):
            self.name=name
            self.char=char
            self.global_namevar=global_namevar
            self.global_charvar=global_charvar
            return
        def change_name(self,new_name):
            self.name=new_name
            exec('global '+self.global_namevar)
            exec('{} = "{}"'.format(self.global_namevar,new_name))
            return
    class CharacterRegistry:
        def __init__(self,var_name):
            self.var_name=var_name
            self.char
            return
        def add_character_entry(self,id,chent):
            X=chent
            return
    t_name='Professor'
    t = DynamicCharacter('t_name', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")