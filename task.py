#--- Day 2 ---#
from psychopy import visual, core, event, data, gui
import random
import pandas as pd

# Initialize window
win = visual.Window([800, 600],fullscr=True)
win.mouseVisible = False

# Initialize an empty list to store trial data
all_trials_data = []

#get participant number, session number with dlg
info = {'subject_num': '','session_number': ''}
dlg = gui.DlgFromDict(info, title='INFO')

# Stage 1 options - change to cards with letters
carpetA = visual.ImageStim(win, image="carpetA.png")
carpetB = visual.ImageStim(win, image="carpetB.png")

#Add transition picture
zzz="zzz.png"
# Stage 2 options - change to common/rare lamps with letters
option1_stage2_green = visual.ImageStim(win, image="lamp_green_1.png")
option2_stage2_green = visual.ImageStim(win, image="lamp_green_2.png")
option1_stage2_orange = visual.ImageStim(win, image="lamp_orange_1.png")
option2_stage2_orange = visual.ImageStim(win, image="lamp_orange_2.png")

# Feedback display - change to genie or zero
rewarded= visual.ImageStim(win, image="genie.png")
unrewarded=visual.ImageStim(win, image="zero.png")

# Timing
clock = core.Clock()

# Random walk function - with counterbalance
subject_number = int(dlg.subject_num)
if subject_number % 2 == 0:
    random_walk=pd.read.csv("random_walk1.csv")
else:
    random_walk=pd.read.csv("random_walk2.csv")

# Run task
n_trials = 200
block = 50
for trial in range(n_trials):
    #show fixation cross 
    fixation = visual.TextStim(win, text="+", pos=(0, 0), color="black")
    core.wait(1)
    # --- Stage 1 ---
    #randomize the location of the letters
    if random.random() < 0.5:
        locs1="1_2"
        carpetA.pos = (-0.5, 0)
        carpetB.pos = (0.5, 0)
    else:
        locs1="2_1"
        carpetA.pos = (0.5, 0)
        carpetB.pos = (-0.5, 0)
    #draw the carpets
    carpetA.draw()
    carpetB.draw()
    win.flip()
    
    #wait for response <8sec
    event.clearEvents()
    keys1 = event.waitKeys(keyList=["s", "k"],maxWait=8, timeStamped=core.Clock())
    
    # Reaction time
    if keys1:  # If a key was pressed
        rt1 = keys1[0][1]  # Reaction time is the second element of the tuple
    else:
        rt1 = None  # If no key was pressed within maxWait, set rt to None

    # Show choice for 1sec
    if keys1[0] == "s":
        ch_key="left"
        if(locs1=="1_2"):
            choice_stage1 = "A"
            carpetA.draw()
        else:
            choice_stage1 = "B"
            carpetB.draw()
    else:
        ch_key="right"
        if(locs1=="1_2"):
            choice_stage1 = "B"
            carpetB.draw()
        else:
            choice_stage1 = "A"
            carpetA.draw()
    win.flip()
    core.wait(1)

    #Show transition picture for 1sec
    zzz.draw() 
    win.flip()
    core.wait(1)

    #Determine transition to second state
    transition = "common" if random.random() < 0.7 else "rare"
    if (choice_stage1=="A" and transition=="common") or (choice_stage1=="B" and transition=="rare"):
        second_state="green"
    else:
        second_state="orange"


    # --- Stage 2 ---
    if second_state=="green":
        if random.random()<0.5:
            locs2="1_2"
            option1_stage2_green.pos=(-0.5,0)
            option2_stage2_green.pos=(0.5,0)
            option1_stage2_green.draw()
            option2_stage2_green.draw()
        else:
            locs2="2_1"
            option1_stage2_green.pos=(0.5,0)
            option2_stage2_green.pos=(-0.5,0)
            option1_stage2_green.draw()
            option2_stage2_green.draw()
    else: #second state is orange
        if random.random()<0.5:
            locs2="1_2"
            option1_stage2_orange.pos=(-0.5,0)
            option2_stage2_orange.pos=(0.5,0)
            option1_stage2_orange.draw()
            option2_stage2_orange.draw()
        else:
            locs2="2_1"
            option1_stage2_orange.pos=(0.5,0)
            option2_stage2_orange.pos=(-0.5,0)
            option1_stage2_orange.draw()
            option2_stage2_orange.draw()
    #show second stage options
    win.flip()

    #wait for second choice <8sec
    event.clearEvents()
    keys2 = event.waitKeys(keyList=["s", "k"],maxWait=8, timeStamped=core.Clock())
    
    # Reaction time
    if keys2:  # If a key was pressed
        rt2 = keys2[0][1]  # Reaction time is the second element of the tuple
    else:
        rt2 = None  # If no key was pressed within maxWait, set rt to None
        
    if (keys2[0] == "s" and locs2=="1_2") or (keys2[0] == "k" and locs2=="2_1") :
        choice_stage2 = 1
    else:
        choice_stage2 = 2
    if second_state=="orange":
        ch_card_2 =choice_stage2+2 #transforming 1-2 to 3-4 for state orange.

    # Determine reward
    current_probs=random_walk[trial]
    reward = random.random() < random_walk[trial,ch_card_2]
    if reward==True:
       outcome=rewarded
    else:
        outcome=unrewarded 
    # Feedback
    outcome.draw()
    win.flip()
    core.wait(2)

    #if block has ended, show break
    if (trial+1) % block == 0:
        break_text = visual.TextStim(win, text="Take a break! Press any key to continue.", pos=(0, 0), color="black")
        break_text.draw()
        win.flip()
        event.waitKeys()
    #save all data
    data_dict = {
        'subject_num': subject_number,
        'session_number': info['session_number'],
        'trial': trial + 1,
        'choice_stage1': choice_stage1,
        'reaction_time_stage1': rt1,
        'transition': transition,
        'second_state': second_state,
        'choice_stage2': choice_stage2,
        'reaction_time_stage2': rt2,
        'reward': reward,
        'prob1_1':current_probs[0],
        'prob1_2':current_probs[1],
        'prob2_1':current_probs[2],
        'prob2_2':current_probs[3],
    }
    # Append to the list
    all_trials_data.append(data_dict)
# Save data after the experiment
results_folder = "results"
os.makedirs(results_folder, exist_ok=True)  # Create results folder if it doesn't exist
file_name = f"{results_folder}/data_subject_{subject_number}_session_{info['session_number']
# Close window
win.close()
