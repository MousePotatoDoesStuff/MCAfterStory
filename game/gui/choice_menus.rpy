init -10 python:
    class ExpandableChoiceList:
        def __init__(self,cho_list,output_size):
            self.cho_list=cho_list
            self.output_size=output_size
            self.current=0
            return
        def is_decrementable(self):
            return self.current!=0
        def is_incrementable(self):
            return self.current+self.output_size<=len(self.cho_list)
        def decrement(self):
            if self.is_decrementable():
                self.current-=self.output_size
            return
        def increment(self):
            if self.is_incrementable():
                self.current+=self.output_size
            return
        def get_current_slice(self):
            return self.cho_list[self.current:self.current+self.output_size]
    class ChoiceMenu:
        def __init__(self,cho_menu_list,disp_text=None,offer_return=False,fit_size=12):
            self.cho_menu_list=cho_menu_list
            self.size=len(cho_menu_list)
            self.disp_text=disp_text
            self.offer_return=offer_return
            self.fit_size=fit_size
            return
        def run(self, memchoice=-1):
            if memchoice!=-1:
                renpy.display_menu(self.cho_menu_list) # nowarn
            first=0
            after_last=min(first+self.fit_size,self.size)
            while True:
                temp=[(str(self.cho_menu_list[i][0]),i) for i in range(first,after_last)]
                if self.offer_return:
                    temp.append('Return',-1)
                if first>0:
                    temp.append('Previous',-2)
                if after_last<self.size:
                    temp.append('Next',-3)
                if self.disp_text is not None:
                    narrator(self.disp_text,interact=False)
                cho_menu_result=renpy.display_menu(temp)
                if cho_menu_result<0:
                    if cho_menu_result==-1:
                        return None
                    elif cho_menu_result==-2:
                        first-=self.fit_size
                        after_last-=self.fit_size
                    elif cho_menu_result==-3:
                        first+=self.fit_size
                        after_last=max(self.size,first+self.fit_size)
                else:
                    break
            return cho_menu_result
        def interpret(self,number):
            if number==-1:
                return None
            return self.cho_menu_list[number]
label choice_menu_getvar(k,options):
    if memory:
        $ result=mem_data[k]
        $ ChoiceMenu(options[result:][:1]).run()
        return mem_data[k]
    else:
        $ result=ChoiceMenu(options).run()
        $ mem_data[k]=result
        return
