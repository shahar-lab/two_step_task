from psychopy import visual, event, core
import random

# Initialize window
win = visual.Window([800, 600], color="black")

# Stage 1 options
option1_stage1 = visual.TextStim(win, text="A", pos=(-0.5, 0), color="white")
option2_stage1 = visual.TextStim(win, text="B", pos=(0.5, 0), color="white")

# Stage 2 options
option1_stage2a = visual.TextStim(win, text="C", pos=(-0.5, 0), color="white")
option2_stage2a = visual.TextStim(win, text="D", pos=(0.5, 0), color="white")
option1_stage2b = visual.TextStim(win, text="E", pos=(-0.5, 0), color="white")
option2_stage2b = visual.TextStim(win, text="F", pos=(0.5, 0), color="white")

# Feedback display
feedback_text = visual.TextStim(win, text="", pos=(0, 0), color="green")

# Timing
clock = core.Clock()

# Reward probabilities (random walk mechanism)
reward_probs = {
    "C": 0.7,
    "D": 0.3,
    "E": 0.5,
    "F": 0.5
}

# Random walk update function
def update_rewards(reward_probs):
    for key in reward_probs:
        reward_probs[key] += random.choice([-0.05, 0.05])
        reward_probs[key] = max(0, min(1, reward_probs[key]))

# Run task
n_trials = 10
for trial in range(n_trials):
    # --- Stage 1 ---
    option1_stage1.draw()
    option2_stage1.draw()
    win.flip()

    keys = event.waitKeys(keyList=["left", "right"])
    if keys[0] == "left":
        choice_stage1 = "A"
        transition = "common" if random.random() < 0.7 else "rare"
    else:
        choice_stage1 = "B"
        transition = "common" if random.random() < 0.7 else "rare"

    # --- Stage 2 ---
    if transition == "common":
        stage2_options = [option1_stage2a, option2_stage2a]
    else:
        stage2_options = [option1_stage2b, option2_stage2b]

    for option in stage2_options:
        option.draw()
    win.flip()

    keys = event.waitKeys(keyList=["left", "right"])
    if keys[0] == "left":
        choice_stage2 = "C" if stage2_options == [option1_stage2a, option2_stage2a] else "E"
    else:
        choice_stage2 = "D" if stage2_options == [option1_stage2a, option2_stage2a] else "F"

    # Determine reward
    reward = random.random() < reward_probs[choice_stage2]

    # Feedback
    feedback_text.text = "Reward!" if reward else "No reward"
    feedback_text.draw()
    win.flip()
    core.wait(1)

    # Update reward probabilities
    update_rewards(reward_probs)

# Close window
win.close()
