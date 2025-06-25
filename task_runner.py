# Import necessary modules
from psychopy import visual, core, event
import random
import pandas as pd

from utils import check_for_esc

def run_task(win, subject_number, type_s, session_number, num_trials, phase, random_walk_data, trial_data_list, block_size=50):
    for trial in range(num_trials):
        check_for_esc(win)

        # Show fixation cross
        fixation = visual.TextStim(win, text="+", pos=(0, 0), color="black")
        fixation.draw()
        win.flip()
        core.wait(1.5)
        check_for_esc(win)

        # Stage 1
        locs1 = "1_2" if random.random() < 0.5 else "2_1"
        carpetA_image = f"images/session_{session_number}/carpetA.png"
        carpetB_image = f"images/session_{session_number}/carpetB.png"
        carpetA = visual.ImageStim(win, image=carpetA_image, pos=(-0.5, 0) if locs1 == "1_2" else (0.5, 0))
        carpetB = visual.ImageStim(win, image=carpetB_image, pos=(0.5, 0) if locs1 == "1_2" else (-0.5, 0))
        carpetA.draw()
        carpetB.draw()
        fixation.draw()
        win.flip()
        check_for_esc(win)

        if locs1 == "1_2":
            left_option1 = 1
            right_option1 = 2
        else:
            left_option1 = 2
            right_option1 = 1

        # Wait for response
        event.clearEvents()
        keys1 = event.waitKeys(keyList=["s", "k"], maxWait=8, timeStamped=core.Clock())
        rt1 = keys1[0][1] if keys1 else None
        choice_stage1 = None
        if keys1:
            if (keys1[0][0] == "s" and locs1 == "1_2") or (keys1[0][0] == "k" and locs1 == "2_1"):
                choice_stage1 = 1
            else:
                choice_stage1 = 2
        else:
            too_slow_text = visual.TextStim(win, text="איטי מדי"[::-1], pos=(0, 0), color="red")
            too_slow_text.draw()
            win.flip()
            core.wait(8)
            check_for_esc(win)
            trial_data = {
                'subject': subject_number,
                'type_s': type_s,
                'session': session_number,
                'phase': phase,
                'trial': trial + 1,
                'block': (trial // block_size) + 1,
                'choice_stage1': None,
                'reaction_time_stage1': None,
                'transition': None,
                'second_state': None,
                'choice_stage2': None,
                'reaction_time_stage2': None,
                'reward': None,
                'prob1_1': random_walk_data.iloc[0, trial],
                'prob1_2': random_walk_data.iloc[1, trial],
                'prob2_1': random_walk_data.iloc[2, trial],
                'prob2_2': random_walk_data.iloc[3, trial],
                'left_option1': left_option1,
                'right_option1': right_option1,
                'left_option2': None,
                'right_option2': None
            }
            trial_data_list.append(trial_data)
            continue

        # Show chosen carpet
        chosen_carpet = carpetA if choice_stage1 == 1 else carpetB
        chosen_carpet.draw()
        fixation.draw()
        win.flip()
        core.wait(0.5)
        check_for_esc(win)

        # Transition picture
        zzz = visual.ImageStim(win, image="images/zzz.png")
        zzz.draw()
        win.flip()
        core.wait(1)
        check_for_esc(win)

        # Determine transition
        transition = "common" if random.random() < 0.7 else "rare"
        if session_number == 1:
            state_mapping = {"common_A": "blue", "rare_B": "blue", "common_B": "pink", "rare_A": "pink"}
        elif session_number == 2:
            state_mapping = {"common_A": "green", "rare_B": "green", "common_B": "orange", "rare_A": "orange"}
        else:
            raise ValueError("Unsupported session number")

        state_key = f"{transition}_{'A' if choice_stage1 == 1 else 'B'}"
        second_state = state_mapping[state_key]

        # Stage 2
        locs2 = "1_2" if random.random() < 0.5 else "2_1"
        option1_image = f"images/session_{session_number}/lamp_{second_state}_1.png"
        option2_image = f"images/session_{session_number}/lamp_{second_state}_2.png"
        option1 = visual.ImageStim(win, image=option1_image, pos=(-0.5, 0) if locs2 == "1_2" else (0.5, 0))
        option2 = visual.ImageStim(win, image=option2_image, pos=(0.5, 0) if locs2 == "1_2" else (-0.5, 0))
        option1.draw()
        option2.draw()
        fixation.draw()
        win.flip()
        check_for_esc(win)

        if locs2 == "1_2":
            left_option2 = 1
            right_option2 = 2
        else:
            left_option2 = 2
            right_option2 = 1

        # Wait for response
        event.clearEvents()
        keys2 = event.waitKeys(keyList=["s", "k"], maxWait=8, timeStamped=core.Clock())
        rt2 = keys2[0][1] if keys2 else None
        choice_stage2 = None
        if keys2:
            if (keys2[0][0] == "s" and locs2 == "1_2") or (keys2[0][0] == "k" and locs2 == "2_1"):
                choice_stage2 = 1
            else:
                choice_stage2 = 2
        else:
            too_slow_text = visual.TextStim(win, text="Too Slow", pos=(0, 0), color="red")
            too_slow_text.draw()
            win.flip()
            core.wait(8)
            check_for_esc(win)
            trial_data = {
                'subject': subject_number,
                'type_s': type_s,
                'session': session_number,
                'phase': phase,
                'trial': trial + 1,
                'block': (trial // block_size) + 1,
                'choice_stage1': choice_stage1,
                'reaction_time_stage1': rt1,
                'transition': transition,
                'second_state': second_state,
                'choice_stage2': None,
                'reaction_time_stage2': None,
                'reward': None,
                'prob1_1': random_walk_data.iloc[0, trial],
                'prob1_2': random_walk_data.iloc[1, trial],
                'prob2_1': random_walk_data.iloc[2, trial],
                'prob2_2': random_walk_data.iloc[3, trial],
                'left_option1': left_option1,
                'right_option1': right_option1,
                'left_option2': left_option2,
                'right_option2': right_option2
            }
            trial_data_list.append(trial_data)
            continue

        # Show chosen option
        chosen_option = option1 if choice_stage2 == 1 else option2
        chosen_option.draw()
        fixation.draw()
        win.flip()
        core.wait(0.5)
        check_for_esc(win)

        # Feedback
        ch_card_2 = choice_stage2 + 2 if second_state in ["pink", "orange"] else choice_stage2
        reward = random.random() < random_walk_data.iloc[ch_card_2 - 1, trial]
        feedback_image = visual.ImageStim(win, image="images/genie.png" if reward else "images/zero.png", pos=(0, 0.5))
        feedback_image.draw()
        fixation.draw()
        chosen_option.draw()
        win.flip()
        core.wait(1.5)
        check_for_esc(win)

        # Save trial data
        trial_data = {
            'subject': subject_number,
            'type_s': type_s,
            'session': session_number,
            'phase': phase,
            'trial': trial + 1,
            'block': (trial // block_size) + 1,
            'choice_stage1': choice_stage1,
            'reaction_time_stage1': rt1,
            'transition': transition,
            'second_state': second_state,
            'choice_stage2': choice_stage2,
            'reaction_time_stage2': rt2,
            'reward': reward,
            'prob1_1': random_walk_data.iloc[0, trial],
            'prob1_2': random_walk_data.iloc[1, trial],
            'prob2_1': random_walk_data.iloc[2, trial],
            'prob2_2': random_walk_data.iloc[3, trial],
            'left_option1': left_option1,
            'right_option1': right_option1,
            'left_option2': left_option2,
            'right_option2': right_option2
        }
        trial_data_list.append(trial_data)

        # Break after blocks
        if (trial + 1) % block_size == 0 and trial + 1 != num_trials and phase == "experiment":
            break_text = visual.TextStim(win, text="הפסקה - קרא לנסיין"[::-1], pos=(0, 0), color="black", height=0.05)
            break_text.draw()
            win.flip()
            event.waitKeys()
