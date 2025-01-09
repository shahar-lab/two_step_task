
from psychopy import visual, core, event

def check_for_esc(win):
    """Check if Esc key is pressed and quit if detected."""
    if "escape" in event.getKeys(keyList=["escape"]):
        win.close()  # Close the window
        core.quit()  # Exit the task immediately

def get_random_walk_path(subject_number, session_number):
    if subject_number % 2 == 0 and session_number == "1":
        return "random_walk/experiment/random_walk1.csv"
    elif subject_number % 2 == 0 and session_number == "2":
        return "random_walk/experiment/random_walk2.csv"
    elif subject_number % 2 != 0 and session_number == "1":
        return "random_walk/experiment/random_walk2.csv"
    elif subject_number % 2 != 0 and session_number == "2":
        return "random_walk/experiment/random_walk1.csv"
    else:
        raise ValueError("Invalid session_number or subject_number")