# %% to create a pseudorandom list of trials in easy and hard demand
# coding=utf-8


### -------------- Pesudo-random ----------------- ###
import random
import csv


def generate_pseudorandom_sequence_learning(seed, num):
    # Set the seed for reproducibility
    random.seed(seed)

    # Create a list representing the trials
    trials = ["easy"] * int(num/2) + ["hard"] * int(num/2)

    # Shuffle the list to get an initial pseudorandom sequence
    random.shuffle(trials)

    # Check and reshuffle if there are more than 3 consecutive repetitions
    while any(trials[i] == trials[i+1] == trials[i+2] == trials[i+3] for i in range(len(trials)-3)):
        random.shuffle(trials)

    return trials



def generate_pseudorandom_sequence_choice(seed, num):
    # Set the seed for reproducibility
    random.seed(seed)

    # Create a list representing the trials
    demands_left = ["easy"] * int(num/2) + ["hard"] * int(num/2)

    # Shuffle the list to get an initial pseudorandom sequence
    random.shuffle(demands_left)

    # Check and reshuffle if there are more than 3 consecutive repetitions
    while any(demands_left[i] == demands_left[i+1] == demands_left[i+2] == demands_left[i+3]
              for i in range(len(demands_left)-3)):
        random.shuffle(demands_left)

    return demands_left


# mapping = "A"
mapping = "B"

# Get the pseudorandom sequence
pseudorandom_sequence_1 = generate_pseudorandom_sequence_learning(seed=23, num=50)  # A_block1; B_block2
pseudorandom_sequence_2 = generate_pseudorandom_sequence_learning(seed=73, num=50)  # A_block2; B_block1

if mapping == "A":
    pseudorandom_sequence = pseudorandom_sequence_1 + pseudorandom_sequence_2  # conditionsA
    cues = {"easy": "cue1.png", "hard": "cue2.png"}
else:
    pseudorandom_sequence = pseudorandom_sequence_2 + pseudorandom_sequence_1  # conditionsB
    cues = {"easy": "cue2.png", "hard": "cue1.png"}

# Add a column "nBackLevel" based on the "Trial Type" condition
n_back_levels = {"easy": 1, "hard": 3}
pseudorandom_sequence_learning_with_nBackLevel = []

for i, trial_demand in enumerate(pseudorandom_sequence, start=1):
    if i > 50:
        i_adjusted = i - 50
    else:
        i_adjusted = i
    trial_dict = {"trialID": i_adjusted,
                  "cue": cues[trial_demand],
                  "trialDemand_learning": trial_demand,
                  "nBackLevel_learning": n_back_levels[trial_demand]}

    pseudorandom_sequence_learning_with_nBackLevel.append(trial_dict)


pseudorandom_sequence_true_cues_left = generate_pseudorandom_sequence_choice(seed=53, num=10)  # true demand choice
pseudorandom_sequence_false_cues_left = generate_pseudorandom_sequence_choice(seed=73, num=50)  # false demand choice
# Add a column "nBackLevel" based on the "Trial Type" condition
n_back_levels = {"easy": 1, "hard": 3}
demands_right = {"easy": "hard", "hard": "easy"}
pseudorandom_sequence_true_choice_with_nBackLevel = []
pseudorandom_sequence_false_choice_with_nBackLevel = []

for i, trial_demand in enumerate(pseudorandom_sequence_true_cues_left, start=1):
    trial_dict = {"choiceID": i,
                  "cueLeft": cues[trial_demand],
                  "cueRight": cues[demands_right[trial_demand]],
                  "cueDemandLeft": trial_demand,
                  "cueDemandRight": demands_right[trial_demand],
                  "nBackLevelLeft": n_back_levels[trial_demand],
                  "nBackLevelRight": n_back_levels[demands_right[trial_demand]],
                  "cueDemandMid": "NA",
                  "nBackLevelMid": "NA"}

    pseudorandom_sequence_true_choice_with_nBackLevel.append(trial_dict)

for i, trial_demand in enumerate(pseudorandom_sequence_false_cues_left, start=1):
    trial_dict = {"choiceID": i,
                  "cueLeft": cues[trial_demand],
                  "cueRight": cues[demands_right[trial_demand]],
                  "cueDemandLeft": trial_demand,
                  "cueDemandRight": demands_right[trial_demand],
                  "nBackLevelLeft": n_back_levels[trial_demand],
                  "nBackLevelRight": n_back_levels[demands_right[trial_demand]],
                  "cueDemandMid": "mid",
                  "nBackLevelMid": 2}

    pseudorandom_sequence_false_choice_with_nBackLevel.append(trial_dict)

pseudorandom_sequence_with_nBackLevel = pseudorandom_sequence_learning_with_nBackLevel+\
                                        pseudorandom_sequence_true_choice_with_nBackLevel+\
                                        pseudorandom_sequence_false_choice_with_nBackLevel

# Save the pseudorandom sequence to a CSV file
csv_filename = f"pseudorandom_sequence_{mapping}.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file,
                            fieldnames=["trialID", "cue", "trialDemand_learning", "nBackLevel_learning",
                                        "choiceID",
                                        "cueLeft", "cueDemandLeft", "nBackLevelLeft",
                                        "cueRight", "cueDemandRight", "nBackLevelRight",
                                        "cueDemandMid", "nBackLevelMid"])
    writer.writeheader()
    writer.writerows(pseudorandom_sequence_with_nBackLevel)

print(f"Pseudorandom sequence saved to {csv_filename}")
