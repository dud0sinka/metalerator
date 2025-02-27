import random
from rhythm_guitar import common as common
from drums.verse.pedal_tone_riff import DrumsPedalToneRiffVerse as Drums
from bass.verse.bass_verse import *
from misc import velocity
from rhythm_guitar.common import handle_unchanged_parts_in_reps, handle_2nd_repetition

SCALES = {
    "MINOR_SCALE": [2, 1, 2, 2, 1, 2, 2],
    "PHRYGIAN_MODE": [1, 2, 2, 2, 1, 2, 2],
    "HARMONIC_MINOR_SCALE": [2, 1, 2, 2, 1, 3, 1],
    "DORIAN_MODE": [2, 1, 2, 2, 2, 1, 2],
}


CHORD_PROGRESSIONS = {  # the numbers are the intervals to add to the current root note
    "verse_0": [0, 0, 0, 0],  # 0 0 0 0
    "verse_1": [0, 0, 5, 4],  # 0 0 8 7
    "verse_2": [0, 0, 5, 3],  # 0 0 8 5
    "verse_3": [0, 0, 5, 6],  # 0 0 8 10
    "verse_4": [0, 0, 4, 2],  # 0 0 7 3
    "verse_5": [3, 3, 5, 4],  # 5 5 8 7
    "verse_6": [0, 0, 2, 3]  # 0 0 3 5
}


class RGuitarPedalToneRiff:
    def __init__(self, start_pos, root_note, progression=None, scale=None):
        self.start_pos = start_pos
        self.ROOT_NOTE = root_note
        self.current_scale = [] if scale is None else scale
        self.notes_generated = []
        self.progression = None if progression is None else progression
        self.palm_mutes_generated = 0
        self.bass_notes = []
        self.number_of_bars = 0  # used for creating leads
        self.repetitions = 0  # used for creating leads
        self.type2_riff = True if random.random() < 0.4 else False  # generate a bit different type of riff

    def set_number_of_bars(self, number_of_bars, repetitions):
        self.number_of_bars = number_of_bars
        self.repetitions = repetitions

    def generate(self, gtr_file, drum_file, bass_file, number_of_bars, repetitions, lead_flag=False, chorus_flag=False, amb_flag=False) -> None:
        if lead_flag and chorus_flag:
            self.type2_riff = False

        self.set_number_of_bars(number_of_bars, repetitions)
        ending_position = 0
        high_note_multiplier = 0 if lead_flag is False else 0.45

        if not self.current_scale:
            lets_choose_a_scale = common.choose_scale(SCALES)
            common.fill_scale(self.ROOT_NOTE, lets_choose_a_scale, self.current_scale, self.ROOT_NOTE)

        if self.progression is None:
            self.progression = random.choice(list(CHORD_PROGRESSIONS.values())) if not self.type2_riff else [0, 0, 0, 0]

        bar = 0
        for _ in range(number_of_bars):
            self.generate_bar(bar, number_of_bars, 0, high_note_multiplier)
            bar += 1
            ending_position = bar * 4

        ending_position = self.create_repetitions(ending_position, repetitions, number_of_bars)
        data = {"position": ending_position + self.start_pos,
                "bars": number_of_bars, "repetitions": repetitions}
        self.write_to_file(gtr_file, lead_flag, chorus_flag, amb_flag)

        if lead_flag is False and amb_flag is False:
            Drums(self.start_pos).generate(drum_file, data)  # generate drums
            write(bass_file, self.bass_notes)  # generate bass

        return ending_position + self.start_pos

    def create_repetitions(self, ending_position, repetitions, number_of_bars):
        end_pos_to_return = ending_position
        notes_to_repeat = self.notes_generated.copy()

        last_root_note_of_progression = self.progression[-1]
        # optional change of the last root note of the progression

        for current_repeat in range(1, repetitions):
            for note in notes_to_repeat:
                if current_repeat == 1:  # modify 1st repeat for 4 bars
                    if random.random() < 0.15:
                        # optional change of the last root note of the progression
                        self.progression[-1] = random.choice(
                            list(set(range(len(self.current_scale[:8]))) - set(self.progression)))
                    if note["position"] >= 12 + self.start_pos:
                        self.generate_bar(7, 4, 1, 0.6)
                        break
                    else:
                        handle_unchanged_parts_in_reps(self.notes_generated, self.bass_notes, current_repeat,
                                                       ending_position, note)

                elif current_repeat == 3:  # modify 3rd repeat for 4 bars
                    if random.random() < 0.25:
                        # optional change of the last root note of the progression
                        self.progression[-1] = random.choice(
                            list(set(range(len(self.current_scale[:8]))) - set(self.progression)))
                    if note["position"] >= 8 + self.start_pos:
                        self.generate_bar(14, 4, 3, 0)
                        self.generate_bar(15, 4, 3, 0.6)
                        break
                    else:
                        handle_unchanged_parts_in_reps(self.notes_generated, self.bass_notes, current_repeat,
                                                       ending_position, note)

                else:
                    handle_2nd_repetition(self.notes_generated, self.bass_notes, current_repeat, ending_position, note)

            self.progression[-1] = last_root_note_of_progression
            end_pos_to_return += number_of_bars * 4

        return end_pos_to_return

    def write_to_file(self, file, lead_flag=False, chorus_flag=False, amb_flag=False):
        if not any([lead_flag, amb_flag, chorus_flag]):  # normal verse riffs
            for note in self.notes_generated:
                file.addNote(0, 0, note["pitch"], note["position"], note["duration"], velocity.main_velocity())

        elif not amb_flag and lead_flag:  # lead licks
            lead_start_pos = self.start_pos + self.number_of_bars * 4 * self.repetitions / 2 if not chorus_flag else self.start_pos + self.number_of_bars * 4 * self.repetitions / random.choice([1, 2])

            for note in self.notes_generated:
                if note["position"] < lead_start_pos and not chorus_flag:
                    continue
                if note["pitch"] not in [12, 14]:
                    file.addNote(0, 0, note["pitch"] + 12, note["position"], note["duration"], velocity.main_velocity())
                else:
                    file.addNote(0, 0, note["pitch"], note["position"], note["duration"], velocity.main_velocity())
        else:
            for note in self.notes_generated:  # amb licks
                if note["pitch"] not in [12, 14]:
                    coef = 24 if self.ROOT_NOTE <= 33 else 12
                    file.addNote(0, 0, note["pitch"] + coef, note["position"], note["duration"], velocity.main_velocity())
                else:
                    file.addNote(0, 0, note["pitch"], note["position"], note["duration"], velocity.main_velocity())

    def generate_bar(self, bar, number_of_bars, repeat=0, high_note_multiplier=0.0):
        multiplier = 4
        if number_of_bars == 8:
            multiplier = 8
        current_root_note = self.set_root_note(bar) if repeat == 0 \
            else self.set_root_note(bar - multiplier * repeat)
        position = 0
        while position < 4:
            current_note = self.insert_notes(bar, position + self.start_pos, current_root_note, high_note_multiplier)
            self.save_gtr_and_bass_notes(bar, current_note, position)
            position += 0.5

    def save_gtr_and_bass_notes(self, bar, current_note, position):
        note = {  # save a note with the following parameters to the history of generated notes
            "pitch": current_note,
            "duration": 0.5,
            "position": bar * 4 + position + self.start_pos
        }
        bass_note = current_note if current_note > 32 else current_note + 12
        bass_note = {  # bass note
            "pitch": bass_note,
            "duration": 0.5,
            "position": bar * 4 + position + self.start_pos
        }
        self.notes_generated.append(note)
        self.bass_notes.append(bass_note)

    def insert_notes(self, bar, position, riff_root_note, high_note_multiplier=0.0):
        if len(self.notes_generated) >= 2 - self.palm_mutes_generated and self.notes_generated[-1]["pitch"] >= \
                self.current_scale[7] \
                and self.notes_generated[-2]["pitch"] >= self.current_scale[7]:
            # no more than two consecutive high notes
            current_note = riff_root_note
        else:
            chance = random.random()
            if chance < 0.65 - high_note_multiplier:
                current_note = riff_root_note
            else:
                current_note = random.choice(self.current_scale[7:]) if not self.type2_riff\
                    else random.choice(self.current_scale[3:10])

        if (current_note == riff_root_note and not self.type2_riff) or (self.type2_riff and random.random() > 0.6):
            self.palm_mute_root_notes(bar, position)

        return current_note

    def palm_mute_root_notes(self, bar, position):
        self.insert_palm_mute_note(bar, position, 14)
        self.insert_palm_mute_note(bar, position, 12, 0.25)

    def insert_palm_mute_note(self, bar, position, pitch, offset: float = 0.0):
        pm = {"pitch": pitch, "duration": 0.5 / 4, "position": bar * 4 + position - 0.125 + offset}
        self.notes_generated.append(pm)
        self.palm_mutes_generated += 1

    def set_root_note(self, bar):  # choose current root note for pedal tone riffs
        return self.current_scale[self.progression[bar]]
