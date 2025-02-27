import random


def choose_scale(SCALES):
    scale = random.choice(list(SCALES.keys()))
    return SCALES[scale]


def fill_scale(current_note, scale, current_scale, ROOT_NOTE):  # fill the scale with notes
    if ROOT_NOTE not in scale:
        current_scale.append(ROOT_NOTE)
    for _ in range(2):
        for i in scale:
            current_note += i
            current_scale.append(current_note)
            if current_note >= ROOT_NOTE + 31:  # restrict the scale to 2.5 octaves
                break
        ROOT_NOTE += 12
    return current_scale


def handle_unchanged_parts_in_reps(notes_generated, bass_notes, current_repeat, ending_position, note):
    note_to_repeat = {"pitch": note["pitch"], "duration": note["duration"],
                      "position": note["position"] + ending_position * current_repeat}
    notes_generated.append(note_to_repeat)
    if note_to_repeat["pitch"] > 14:
        bass_notes.append(note_to_repeat)


def handle_2nd_repetition(notes_generated, bass_notes, current_repeat, ending_position, note):
    note_to_repeat = {"pitch": note["pitch"], "duration": note["duration"],
                      "position": note["position"] + ending_position * current_repeat}
    note_to_repeat["pitch"] = note_to_repeat["pitch"] - 12 if random.random() < 0.8 and note_to_repeat[
        "pitch"] > 48 else note_to_repeat[
        "pitch"]
    notes_generated.append(note_to_repeat)
    if note_to_repeat["pitch"] > 14:
        bass_notes.append(note_to_repeat)