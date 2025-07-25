from psychopy import visual, core, event
import pandas as pd

def check_for_esc(win, trial_data_list=None, output_filename=None):
    keys = event.getKeys()
    if "escape" in keys:
        if trial_data_list is not None and output_filename is not None:
            df = pd.DataFrame(trial_data_list)
            df.to_csv(output_filename, index=False)
            print(f"Data saved to {output_filename} before exit.")
        win.close()
        core.quit()


def get_random_walk_path(subject_number, session_number):
    if subject_number % 2 == 0 and session_number == 1:
        return pd.read_csv("random_walk/experiment/random_walk1.csv",header=None)
    elif subject_number % 2 == 0 and session_number == 2:
        return pd.read_csv("random_walk/experiment/random_walk2.csv",header=None)
    elif subject_number % 2 != 0 and session_number == 1:
        return pd.read_csv("random_walk/experiment/random_walk2.csv",header=None)
    elif subject_number % 2 != 0 and session_number == 2:
        return pd.read_csv("random_walk/experiment/random_walk1.csv",header=None)
    else:
        raise ValueError("Invalid session_number or subject_number")