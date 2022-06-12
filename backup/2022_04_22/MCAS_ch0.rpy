label intro_main:
    call ch0_0
    call ch0_1
    call ch0_2
    call ch0_3
    scene bg club_day
    $ persistent.epiphany_stage=1
    $ renpy.utter_restart()
    return

label ch0_0:
    stop music fadeout 2.0
    scene bg residential_day
    with dissolve_scene_full
    play music t2
    "...I hate Mondays."
    "Mornings are usually the worst, being surrounded by couples and friend groups walking to school together."
    "Meanwhile, I've always walked to school alone."
    "I always tell myself it's about time I meet some girls or something like that..."
    "But I have no motivation to join any clubs."
    "In fact, I have no motivation to do anything with my life."
    "I'm perfectly content just getting by on the average while spending my free time on games and anime."
    "Let's just get this over with..."
    return
    

label ch0_1:
    stop music fadeout 2.0
    scene bg class_day
    with wipeleft_scene

    "This class is taking FOREVER."
    "I can roughly understand what is going on, but I really don't care."
    "I look around the classroom, seeking something interesting to occupy my thoughts."
    "Most of the class seems to be as bored as I am."
    "..."
    "I secretly open a copy of {i}Half Piece Redux{/i} under the desk."
    "{i}You thought this part would be a JoJo reference, but it was me, {/i}{nw}"
    t "[mc_name]?"
    mc "Uh, yes?"
    t "What role does mitochondria have in a cell?"
    mc "It's the powerhouse of the cell."
    t "What nitrogenous base in RNA pairs with adenine in DNA?"
    mc "Uracil."
    t "What are you holding under your desk?"
    mc "{i}Half Piece Redux{/i} part 723-   {nw}"
    "Whoops."
    t "This is the fifth time this month, [mc_name]."
    "The professor takes out his phone and starts typing something."
    "Am I in trouble?"
    t "Go to the councilor's office, third floor, room 307."
    "Yeah, it definitely seems like I'm in trouble."
    return

label ch0_2:
    play music t5
    scene bg corridor
    with wipeleft_scene

    "At least this isn't as boring as sitting in class."
    "I go across the school and upstairs - a section of the school I rarely visit, being generally used for third-year classes and activities."
    "I see a list of clubs on one of the bulletin boards."
    mc "Drama club, debate club, anime club, Fight Club..."
    "They all have club presidents and contact information listed, except for one..."
    mc "Literature club?"
    "I guess whoever started the club couldn't find any members and eventually gave up."
    "Or teachers started it in hope someone would get interested."
    "Either way, I am not surprised at all no one wants to join it. Studying literature is boring."
    mc "Oh yeah, I should hurry to the councilor's office..."
    return

label ch0_3:
    $ renpy.music.play(audio.t5,relative_volume=0.2)
    scene bg club_day
    with wipeleft_scene
    "I look inside the classroom, wondering if I'm at the right place."
    mc "Hello?"
    co "Ah yes, [mc_name]. Come in."
    "I enter the classroom."
    co "My office is currently being renovated, so I borrowed this unused classroom."
    mc "Oh."
    "That makes sense."
    co "So, the biology teacher told me you're not paying attention in class."
    mc "Am I in trouble?"
    co "If it was up to him, you would be."
    co "But luckily for you, I have a more constructive approach to your laziness."
    co "I think you just need an activity that feels, for a lack of better words, more real."
    co "Have you considered joining a club?"
    mc "I can't say I have?"
    "He gives me a list of clubs identical to the one I saw in the hallway just now."
    "And once again, the literature club entry is mysteriously blank."
    mc "Why is there no name or contact for the literature club?"
    co "There is a literature club?"
    mc "Yes, it's right here."
    "I return the list, and the councilor double-checks it."
    co "One moment."
    "He starts typing something into his computer."
    $ pause(2)
    co "There doesn't seem to be a literature club registered."
    co "It's probably a clerical error. You should look for another club to join."
    "Then, I come up with an idea."
    mc "If the literature club doesn't exist now, does that mean I can start it?"
    co "You want to start a literature club?"
    co "I didn't know you had an interest in {i}{b}actual literature{/b}{/i}, [mc_name]."
    "I let that slide."
    "I don't, in fact, have an interest in \"actual\" literature."
    "And I definitely don't have any interest in running a club."
    mc "Oh well..."
    "But from what I can tell, no other student here really has an interest in literature either."
    "So if I start this club, I won't actually have to do much about it."
    mc "...I guess this is a chance to broaden my horizons."
    "Maybe I can somehow use it as an excuse to read {i}Half Piece Redux{/i} in class, too..."
    co "Sounds like all you needed was a little push."
    co "Just fill in your name and phone or email here."
    "Okay, let's see how this goes."
    menu:
        "Fill the document.":
            "Done."
    stop music
    call glitch(0.25) from _call_glitch
    scene bg club_day3
    mc "AAAAAAAAAAAAAAAA"
    call glitch(0.25) from _call_glitch_1
    scene bg kitchen
    mc "MY HEAD"
    call glitch(0.5) from _call_glitch_2
    scene bg bedroom
    mc "WHAT IS HAPPENING?!?"
    call glitch(0.5) from _call_glitch_3
    show s_kill_bg2
    mc "COUNCILOR WHAT IS HAPPENING TO ME"
    call glitch(0.5) from _call_glitch_4
    return

label glitch(time=1):
    window hide(None)
    show screen tear(20, 0.1, 0.1, 0, 40)
    play sound "sfx/glitch1.ogg"
    $ pause(time)
    stop sound
    hide screen tear
    window show(None)
    return

label ch0_4:
    scene code_void
    show mc turned worr at t11
    mc "What is this place?"
    mc "I can't see anything but weird words all over the place."
    mc "Am I asleep? Is this some weird dream?"
    mc "Wait, no, I was in the councilor office just now. I didn't fall asleep..."
    mc "{i}Am I in a coma?{i}"
    mc "{b}{i}AM I DEAD?!?{/i}{/b}"
    mc "... Okay, calm down, [mc_name]. Let's see what we have here."
    mc "I seem to be standing in a strange void."
    mc "The air seems fine - or at least I can't sense anything wrong with it."
    mc "I can't see the ground I'm standing on, but it seems solid..."
    "[mc_name] proceeds to stomp the ground."
    mc "Nothing interesting happened."
    mc "These words all have different colors, and there seems to be a pattern in them."
    mc "And if I look hard in this one particular direction, I can see what looks like a..."
    mc "......."
    mc "Who the hell are YOU?!?"
    python:
        cho_menu_list = [("Don't you remember me?",['4a'],True),
        ('The councilor.',['4b'],True),
        ('God.',['4c'],True),
        ('Monika.',['4d'],True),
        ('Sayori.',['4e'],True),
        ('The player.',['4f'],True)]*2
    return

label ch0_4a:
    if not isFirstCall:
        scene code_void
        show mc turned worr at t11
    mc "No, I most definitely do not."
    jump ch0_4end

label ch0_4b:
    if not isFirstCall:
        scene code_void
        show mc turned worr at t11
    mc "You don't really look like him..."
    jump ch0_4end

label ch0_4c:
    if not isFirstCall:
        scene code_void
        show mc turned worr at t11
    mc "So...does that mean I am dead?"
    mc "What did I even die of?"
    jump ch0_4end

label ch0_4d:
    pass
label ch0_4e:
    if not isFirstCall:
        scene code_void
        show mc turned worr at t11
    mc "For some reason, I remember this person...and I remember they look nothing like you."
    jump ch0_4end

label ch0_4f:
    if not isFirstCall:
        scene code_void
        show mc turned worr at t11
    mc "The what?"
    jump ch0_4end

label ch0_4end:
    $ persistent.auto_open.append(([5],isFirstCall))
    return

label ch0_5:
    "TODO"
    return