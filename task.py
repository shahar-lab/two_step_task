#--- Day 2 ---#
# Import necessary libraries
from psychopy import visual, core,gui,event
import pandas as pd
import os
import datetime

# Import run_task function
from task_runner import run_task
from utils import get_random_walk_path
# Get participant number and session number using the dialog
info = {'subject_number': '', 'session_number': '', 'type_s': ''}  # Define the dialog box dictionary
order = ['subject_number', 'session_number','type_s']  # Define the desired order

dlg = gui.DlgFromDict(info, title='INFO', order=order)

if not dlg.OK:  # If the user cancels the dialog
    core.quit()

# Access the values from the 'info' dictionary
subject_number = int(info['subject_number'])  # Get and convert the subject number
session_number = int(info['session_number'])  # Get the session number as a string
type_s         = info['type_s']
# Initialize Window
win = visual.Window([800, 600], fullscr=True, color="white", colorSpace="rgb")
win.mouseVisible = False

# Setup Data
random_walk_practice = pd.read_csv("random_walk/practice/random_walk_practice.csv", header=None) #transpose rows and columns
random_walk_exp=get_random_walk_path(subject_number, session_number)

#Start practice
start_practice_text = "כעת נתחיל באימון. לחץ על כל מקש כדי להתחיל."[::-1]

# Display the message
start_practice = visual.TextStim(win, text=start_practice_text, pos=(0, 0), color="black",height=0.05)
start_practice.draw()
win.flip()
# Wait for any key to proceed
event.waitKeys()
# Practice Task
practice_trials_data = []
run_task(win,type_s,session_number, num_trials=4, phase="practice", random_walk_data=random_walk_practice, trial_data_list=practice_trials_data)

# Save Practice Data
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
practice_file = os.path.join("results", f"practice_data_{timestamp}.csv")
pd.DataFrame(practice_trials_data).to_csv(practice_file, index=False)

#End practice
end_practice_text = "האימון הסתיים. לחץ על כל מקש כדי להתחיל בניסוי."[::-1]

# Display the message
end_practice = visual.TextStim(win, text=end_practice_text, pos=(0, 0), color="black",height=0.05)
end_practice.draw()
win.flip()

# Wait for any key to proceed
event.waitKeys()
# Main Experiment Task
experiment_trials_data = []
run_task(win,type_s,session_number ,num_trials=4, phase="experiment", random_walk_data=random_walk_exp, trial_data_list=experiment_trials_data)

# Save Experiment Data
experiment_file = os.path.join("results", f"experiment_data_{timestamp}.csv")
pd.DataFrame(experiment_trials_data).to_csv(experiment_file, index=False)
