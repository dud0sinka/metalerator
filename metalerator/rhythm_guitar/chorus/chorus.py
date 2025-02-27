import random
from rhythm_guitar import common as common
from drums.verse.pedal_tone_riff import DrumsPedalToneRiffVerse as Drums
from rhythm_guitar.verse.pedal_tone_riff import RGuitarPedalToneRiff as Guitar
from bass.verse.bass_verse import *
from misc import velocity
from rhythm_guitar.common import handle_2nd_repetition, handle_unchanged_parts_in_reps

SCALES = {
    "MINOR_SCALE": [2, 1, 2, 2, 1, 2, 2],
    "PHRYGIAN_MODE": [1, 2, 2, 2, 1, 2, 2]
}


CHORD_PROGRESSIONS = {  # the numbers are the intervals to add to the current root note
    "chorus0": [0, 0, 5, 4],  # 0 0 8 7
    "chorus1": [0, 0, 5, 3],  # 0 0 8 5
    "chorus2": [0, 0, 5, 6],  # 0 0 8 10
    "chorus3": [0, 0, 4, 2],  # 0 0 7 3
    "chorus4": [3, 3, 5, 4],  # 5 5 8 7
}


# data = {"position": ending_position, "scale": current_scale, "bars": number_of_bars, "repetitions": repetitions}


class RGuitarChorus:
    def __init__(self, start_pos, root_note):
        self.start_pos = start_pos
        self.ROOT_NOTE = root_note
        self.current_scale = []
        self.notes_generated = []
        self.progression = None
        self.palm_mutes_generated = 0
        self.bass_notes = []

    def generate(self, gtr_file, drum_file, bass_file, number_of_bars, repetitions, lead_file):
        ending_position = 0

        lets_choose_a_scale = common.choose_scale(SCALES)
        common.fill_scale(self.ROOT_NOTE, lets_choose_a_scale, self.current_scale, self.ROOT_NOTE)
        self.progression = random.choice(list(CHORD_PROGRESSIONS.values()))

        bar = 0
        for _ in range(number_of_bars):
            self.generate_bar(bar, number_of_bars)
            bar += 1
            ending_position = bar * 4

        ending_position = self.create_repetitions(ending_position, repetitions, number_of_bars)
        data = {"position": ending_position + self.start_pos,
                "bars": number_of_bars, "repetitions": repetitions}
        self.write_to_file(gtr_file)

        Drums(self.start_pos, True).generate(drum_file, data)  # generate drums
        write(bass_file, self.bass_notes)  # generate bass

        self.generate_lead(lead_file, number_of_bars, repetitions)

        return ending_position + self.start_pos

    def generate_lead(self, lead_file, number_of_bars, repetitions):
        Guitar(self.start_pos, self.ROOT_NOTE, self.progression, self.current_scale).generate(lead_file, None, None, number_of_bars, repetitions, True, True)

    def create_repetitions(self, ending_position, repetitions, number_of_bars):
        end_pos_to_return = ending_position
        notes_to_repeat = self.notes_generated.copy()

        last_root_note_of_progression = self.progression[-1]
        # optional change of the last root note of the progression

        for current_repeat in range(1, repetitions):
            for note in notes_to_repeat:
                if current_repeat == 1:  # modify 1st repeat
                    if random.random() < 0.4:
                        # optional change of the last root note of the progression
                        self.progression[-1] = random.choice(
                            list(set(range(len(self.current_scale[:8]))) - set(self.progression)))
                    if note["position"] >= 12 + self.start_pos:
                        self.generate_bar(7, 4, 1)
                        break
                    else:
                        note_to_repeat = {"pitch": note["pitch"], "duration": note["duration"],
                                          "position": note["position"] + ending_position * current_repeat}
                        self.notes_generated.append(note_to_repeat)

                        if note_to_repeat["pitch"] > 14 and not any(
                                bass_note["position"] == note_to_repeat["position"] for bass_note in self.bass_notes):
                            self.bass_notes.append(note_to_repeat)

                elif current_repeat == 3:  # modify 3rd repeat for 4 bars
                    if random.random() < 1:
                        # optional change of the last root note of the progression
                        self.progression[-1] = random.choice(
                            list(set(range(len(self.current_scale[:8]))) - set(self.progression)))
                    if note["position"] >= 8 + self.start_pos:
                        self.generate_bar(14, 4, 3)
                        self.generate_bar(15, 4, 3)
                        break
                    else:
                        handle_unchanged_parts_in_reps(self.notes_generated, self.bass_notes, current_repeat,
                                                       ending_position, note)
                else:
                    handle_2nd_repetition(self.notes_generated, self.bass_notes, current_repeat, ending_position, note)

            self.progression[-1] = last_root_note_of_progression
            end_pos_to_return += number_of_bars * 4

        return end_pos_to_return

    def write_to_file(self, file):
        for note in self.notes_generated:
            file.addNote(0, 0, note["pitch"], note["position"], note["duration"], velocity.main_velocity())

    def generate_bar(self, bar, number_of_bars, repeat=0):
        multiplier = 4
        if number_of_bars == 8:
            multiplier = 8
        current_root_note = self.set_root_note(bar) if repeat == 0 \
            else self.set_root_note(bar - multiplier * repeat)
        position = 0
        while position < 4:
            current_note = current_root_note
            if current_note < 35:
                current_note += 12
            self.power_chord_and_bass(bar, current_note, position)

            position += 1

    def power_chord_and_bass(self, bar, current_note, position):
        note = {  # save a note with the following parameters to the history of generated notes
            "pitch": current_note,
            "duration": 1,
            "position": bar * 4 + position + self.start_pos
        }
        note_fifth = {
            "pitch": current_note + 7,
            "duration": 1,
            "position": bar * 4 + position + self.start_pos
        }
        note_octave = {
            "pitch": current_note + 12,
            "duration": 1,
            "position": bar * 4 + position + self.start_pos
        }
        bass_note = current_note if current_note > 32 else current_note + 12
        bass_note = {  # bass note
            "pitch": bass_note,
            "duration": 1,
            "position": bar * 4 + position + self.start_pos
        }
        self.notes_generated.append(note)
        self.notes_generated.append(note_fifth)
        self.notes_generated.append(note_octave)
        self.bass_notes.append(bass_note)

    def set_root_note(self, bar):  # choose current root note for pedal tone riffs
        return self.current_scale[self.progression[bar]]
