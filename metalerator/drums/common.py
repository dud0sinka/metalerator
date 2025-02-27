import random
from misc import velocity

allowed_drums_for_fills = [38, 41, 43, 45, 47, 48]
openers = [28, 31, 49, 57]
power_hand = [27, 29, 52, 57, 60]
double_time_power_hand = [27, 29, 52, 57, 60, 51, 53]


# cymbals: 27 - china, 28, 29 - china, 30, 31, 49, 51 - ride, 52 - china, 53 - ride top, 55 - splash, 57,
# 60 - open hat, 63 - closed hat
# MyMIDI.addNote(track,channel,pitch,position,duration,volume)

def choose_and_generate_fill(start_pos, bars, file, intro=False):
    fills = ["fast", "triplet", "snare", "tss"] if not intro else ["fast", "snare"]
    i = start_pos
    end_pos = start_pos + bars * 4
    while i < end_pos:
        choice = random.choice(fills)
        if choice == "fast":
            generate_fast_fill(i, 0.5, file)
        if choice == "triplet":
            generate_triplet_fill(i, 0.5, file)
        if choice == "snare":
            generate_snare_fill(i, 0.5, file)
        if choice == "tss":
            if i == end_pos - 2:
                file.addNote(0, 0, 36, i, 0.25, velocity.main_velocity())
                file.addNote(0, 0, random.choice(openers + power_hand), i, 0.25, velocity.main_velocity())
            else:
                generate_fast_fill(i, 0.5, file)
        i += 2
    return end_pos


def generate_fast_fill(start_pos, bars, file):
    position = start_pos
    previous_drum = None
    end_pos = start_pos + bars * 4

    while position < end_pos:
        if previous_drum is None:
            current_drum = random.choice(allowed_drums_for_fills + [36])
        elif previous_drum == 36:
            current_drum = random.choice(allowed_drums_for_fills)
        else:
            current_drum = 36

        reps = random.choice([2, 4]) if end_pos - position >= 1 else 2

        for _ in range(reps):
            vel = velocity.main_velocity() + 15 if position % 1 == 0 and current_drum != 36 \
                else velocity.main_velocity()  # accents

            file.addNote(0, 0, current_drum, position, 0.25, vel)
            position += 0.25
        previous_drum = current_drum


def generate_triplet_fill(start_pos, bars, file):
    position = start_pos
    end_pos = start_pos + bars * 4

    while abs(end_pos - position) > 0.001:
        current_drum = random.choice(allowed_drums_for_fills)

        for i in range(3):
            if i == 2:
                current_drum = 36
            file.addNote(0, 0, current_drum, position, 0.25, velocity.main_velocity())
            position += 1 / 3


def generate_snare_fill(start_pos, bars, file):
    position = start_pos
    end_pos = start_pos + bars * 4
    flag = False

    while position < end_pos:
        if (position + .25) % .5 != 0 and flag is True:
            flag = False

        velocity_subtraction = 0
        if position % 1 == 0:
            velocity_subtraction = 5

        if position + .5 % 1 == 0:
            velocity_subtraction = -10
        if position + .25 % .5 == 0:
            velocity_subtraction = -20

        file.addNote(0, 0, 38, position, .25, velocity.main_velocity() + velocity_subtraction)

        if (random.random() > .7 or flag is True) and position < end_pos - 1:  # add a chance of tu tu TRRRR tu
            position += .25
            flag = True
            continue
        else:
            position += .5


def opening_cymbals(file, position, cymbals=2):
    allowed_openers = openers.copy()
    opener1 = random.choice(allowed_openers)
    allowed_openers.remove(opener1)
    opener2 = random.choice(allowed_openers)

    file.addNote(0, 0, opener1, position, 0.25, velocity.main_velocity())
    if cymbals == 2:
        file.addNote(0, 0, opener2, position, 0.25, velocity.main_velocity())
