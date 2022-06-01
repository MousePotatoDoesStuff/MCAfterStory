init -1 python:
    submod_name='TestSubmod'

    first_label=SubmodMemory(submod_name,'init')
    second_label=SubmodMemory(submod_name,'load')
    on_init=[(first_label,True)]
    on_load=[(second_label,True)]
    test_submod=SubmodData(submod_name,on_init,on_load)
    submods_available[submod_name]=test_submod

label submods_data_TestSubmod_init:
    $ persistent.auto_open.clear()
    "Hello, MCAS!"
    "This is a test submod!"
    return

label submods_data_TestSubmod_load:
    "Hello again, MCAS!"
    "This is still a test submod!"
    return