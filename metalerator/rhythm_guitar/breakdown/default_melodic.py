from misc import velocity
import random
from rhythm_guitar import common as common
from drums.breakdown.default_melodic import DrumsDefaultMelodicBreakdown as Drums
from bass.breakdown.bass_default_breakdown import BassDefaultMelodicBreakdown as Bass
from rhythm_guitar.verse.pedal_tone_riff import RGuitarPedalToneRiff as Guitar
from ambient import ambient
# position: 0.25 = 16th note, 0.5 = 8th note, 1 = 4th note. 1 bar has 16 positions
# duration: 0.25 = 16th, 0.5 = 8th, 1 = 4th
# we use bar * 4 because we count bars as 0, 1, 2..... but in terms of position 1 bar equals to 4
# MyMIDI.addNote(track,channel,pitch,position,duration,volume)

ROOT_NOTE_LOWEST = 29
ROOT_NOTE_HIGHEST = 38
SCALES = {
    "MINOR_SCALE": [2, 1, 2, 2, 1, 2, 2],
    "PHRYGIAN_MODE": [1, 2, 2, 2, 1, 2, 2],
    "HARMONIC_MINOR_SCALE": [2, 1, 2, 2, 1, 3, 1],
    "MELODIC_MINOR_SCALE_ASCENDING": [2, 1, 2, 2, 2, 2, 1],
}
INTERVALS = {
    "second": 1,
    "third": 2,
    "fourth": 3,
    "sixth": 5,
}

"""
 A class to generate melodic guitar breakdowns.

 Attributes:
 ----------
 start_pos : float
     The starting position where generation begins.
 root_note : int
     The root note used as a basis for generation.
 progression : list or None, optional
     A list representing a musical progression if applicable (default is None).
 scale : list or None, optional
     A list defining the musical scale used for generation (default is None).
 lead_file : str or None, optional
     File path for storing generated lead guitar parts (default is None).
 amb_file : str or None, optional
     File path for storing generated ambient sounds (default is None).

 Methods:
 -------
 generate(gtr_file, drum_file, bass_file, number_of_bars, repetitions, outside_flag=False):
     Generates melodic guitar breakdowns along with drums, bass, and optionally lead and ambient guitars.
 generate_bar(bar, root_note=None):
     Generates a single bar based on the specified parameters.
 write_to_file(file):
     Writes the generated notes to a specified file.
 generate_lead(lead_file, number_of_bars, repetitions):
     Generates lead guitar parts based on the specified parameters.
 create_repetitions(ending_position, repetitions, number_of_bars):
     Creates repetitions of the generated notes.
 create_kick_pattern():
     Generates a kick drum pattern based on the generated guitar parts.
 randomize_duration(position):
     Randomizes the duration of musical notes based on their position in the bar.
 insert_notes(bar, position, current_duration, root_note=None):
     Inserts musical notes into the generated sequence based on specified conditions.
 insert_rests(position):
     Inserts rests into the musical sequence based on specified conditions.
 diversify_notes(current_note, bar, position, current_duration):
     Diversifies the notes by adding intervals or variations.
 interval_randomizer(current_note):
     Randomly selects an interval for note variation.
 palm_mute(bar, position, duration):
     Inserts palm-muted notes into the sequence based on specified conditions.
 check_for_palm_mute(position, pitch, tolerance=0.075):
     Checks if a palm-muted note exists at a specific position and pitch.
 """


class RGuitarDefaultMelodicBreakdown:

    def __init__(self, start_pos, root_note, progression=None, scale=None, lead_file=None, amb_file=None):
        self.start_pos = start_pos
        self.current_scale = [] if scale is None else scale  # scale that was chosen
        self.root_notes_generated = []  # amount of generated 0's is affecting the amount of rests
        self.ROOT_NOTE = root_note
        self.recent_note = 0  # keep track of the last note played
        self.recent_duration = 0  # keep track of the duration of the lat note played
        self.notes_generated = []  # all notes generated
        self.consecutive_16ths = 0  # this variable is used to prevent the generation of singular 16th notes
        self.data = {}
        self.kick = []  # guitar 0's are being passed here to match the kick
        self.progression = None if progression is None else progression # for one of the pre-chorus variations
        self.lead_file = None if lead_file is None else lead_file
        self.amb_file = None if amb_file is None else amb_file
        self.is_lead = False
        self.type2 = True if random.random() < 0.3 and progression is None else False

    def generate(self, gtr_file, drum_file, bass_file, number_of_bars, repetitions, outside_flag=False):
        ending_position = 0

        if outside_flag is False:
            lets_choose_a_scale = common.choose_scale(SCALES)
            common.fill_scale(self.ROOT_NOTE, lets_choose_a_scale, self.current_scale, self.ROOT_NOTE)

        bar = 0
        for i in range(number_of_bars):
            if outside_flag is True:
                self.generate_bar(bar, self.progression[i])
            else:
                self.generate_bar(bar)
            bar += 1
            ending_position = bar * 4

        self.create_kick_pattern()
        ending_position = self.create_repetitions(ending_position, repetitions, number_of_bars)

        if gtr_file is not None:
            self.write_to_file(gtr_file)

        self.data = {"position": ending_position + self.start_pos,
                     "bars": number_of_bars, "repetitions": repetitions}
        Drums(self.start_pos, outside_flag).generate(drum_file, self.data, self.kick)  # generate drums
        Bass(self.notes_generated).copy_guitar(bass_file)  # generate bass

        if self.lead_file is not None:  # generate lead
            if random.random() < 0.55:
                self.is_lead = True
                self.generate_lead(self.lead_file, number_of_bars, repetitions)
        if self.amb_file is not None:  # generate ambience
            amb = False if gtr_file is not None else True
            ambient.generate(self.amb_file, number_of_bars, repetitions, self.start_pos, self.ROOT_NOTE, self.current_scale, self.is_lead, amb)
        return ending_position + self.start_pos

    def generate_bar(self, bar, root_note=None):
        position = 0

        if root_note is not None:
            root_note = self.current_scale[root_note]

        while position < 4:

            position_copy = position
            position = self.insert_rests(position)
            if position == -1:
                position = position_copy
            else:
                continue

            current_duration, current_note = self.choose_duration_pm_pitch(bar, position, root_note)
            self.root_notes_generated.append(current_note)
            note = {  # save a note with the following parameters to the history of generated notes
                "pitch": current_note,
                "duration": current_duration,
                "position": bar * 4 + position + self.start_pos
            }
            self.notes_generated.append(note)

            position += current_duration

            self.recent_note = current_note
            self.recent_duration = current_duration

    def choose_duration_pm_pitch(self, bar, position, root_note):
        current_duration = self.randomize_duration(position)  # generate duration
        if self.consecutive_16ths % 2 != 0 and current_duration != 0.25:  # prevent singular 16th notes
            current_duration = 0.25
        if current_duration == 0.25:
            self.consecutive_16ths += 1
        else:
            self.consecutive_16ths = 0
        self.palm_mute(bar, position + self.start_pos, current_duration)
        current_note = self.insert_notes(bar, position + self.start_pos, current_duration, root_note)
        return current_duration, current_note

    def write_to_file(self, file):
        for note in self.notes_generated:
            file.addNote(0, 0, note["pitch"], note["position"], note["duration"], velocity.main_velocity())

    def generate_lead(self, lead_file, number_of_bars, repetitions):
        progression = [0, 0, 0, 0] if self.progression is None else self.progression
        Guitar(self.start_pos, self.ROOT_NOTE, progression, self.current_scale).generate(lead_file, None, None, number_of_bars, repetitions, True)
        return

    def create_repetitions(self, ending_position, repetitions, number_of_bars):
        notes_to_repeat = self.notes_generated.copy()
        end_pos_to_return = ending_position
        for current_repeat in range(1, repetitions):
            for note in notes_to_repeat:
                if note["pitch"] not in [12, 14]:  # Check if the pitch is not 12 or 14
                    if current_repeat == 1:  # modify 1st and 3rd repeats
                        if note["position"] >= 12 + self.start_pos:
                            self.generate_bar(4 + current_repeat * 4 - 1)
                            break
                        else:
                            self.notes_generated.append({"pitch": note["pitch"], "duration": note["duration"],
                                                         "position": note[
                                                                         "position"] + ending_position * current_repeat})
                    elif current_repeat == 3:
                        if note["position"] >= 8 + self.start_pos:
                            self.generate_bar(4 + current_repeat * 4 - 2)
                            self.generate_bar(4 + current_repeat * 4 - 1)
                            break
                        else:
                            self.notes_generated.append({"pitch": note["pitch"], "duration": note["duration"],
                                                         "position": note[
                                                                         "position"] + ending_position * current_repeat})
                    else:
                        note["pitch"] = note["pitch"] - 12 if random.random() < 0.8 and note["pitch"] > 53 else note[
                            "pitch"]
                        self.notes_generated.append({"pitch": note["pitch"], "duration": note["duration"],
                                                     "position": note["position"] + ending_position * current_repeat})
            self.copy_palm_mutes_to_repetitions(current_repeat, notes_to_repeat, ending_position)
            end_pos_to_return += number_of_bars * 4
        return end_pos_to_return

    def copy_palm_mutes_to_repetitions(self, current_repeat, notes_to_repeat,
                                       ending_position):  # copying palm mutes sometimes
        # causes exceptions I cant find the reason for; hence a separate function
        if current_repeat == 1:
            self.handle_pms_in_different_reps(current_repeat, ending_position, notes_to_repeat, 11.925)
        elif current_repeat == 2:
            self.handle_pms_in_different_reps(current_repeat, ending_position, notes_to_repeat, 15.25)
        elif current_repeat == 3:
            self.handle_pms_in_different_reps(current_repeat, ending_position, notes_to_repeat, 7.925)

    def handle_pms_in_different_reps(self, current_repeat, ending_position, notes_to_repeat, pos):
        for pm in notes_to_repeat:  # copy to 1 repetition
            if pm["pitch"] in [12, 14]:
                if pm["position"] < pos + self.start_pos:
                    self.notes_generated.append({"pitch": pm["pitch"], "duration": pm["duration"],
                                                 "position": pm["position"] + ending_position * current_repeat})

    def create_kick_pattern(self):
        for note in self.notes_generated:  # default breakdown mode
            if 14 < note["pitch"] < 47 and note["position"] not in self.kick and self.progression is not None:  # progression breakdown mode
                self.kick.append(note["position"])

            if note["position"] == self.start_pos and note["position"] not in self.kick:  # default mode
                self.kick.append(self.start_pos)
                continue
            if note["pitch"] > ROOT_NOTE_HIGHEST and note["position"] not in self.kick:  # optional kick for high notes
                if random.random() < 0.4:
                    self.kick.append(note["position"])
                continue
            if ROOT_NOTE_LOWEST <= note["pitch"] <= ROOT_NOTE_HIGHEST and note["position"] not in self.kick:
                self.kick.append(
                    note["position"])  # remembering guitar accents to pass to the kick drum

    def randomize_duration(self, position):
        duration = [0.25, 0.5, 1, 2]
        weights = [1, 3, 3, 1]  if not self.type2 else [2, 4, 1.5, 0.5]
        allowed_duration = [dur for dur in duration if dur <= (4 - position)]

        allowed_weights = [weights[duration.index(dur)] for dur in allowed_duration]

        choice = random.choices(allowed_duration, weights=allowed_weights, k=1)[0] if self.progression is None else \
            random.choices([0.25, 0.5, 1], weights=[1, 3, 0.5], k=1)[0]
        return choice

    def insert_notes(self, bar, position, current_duration, root_note=None):
        high_notes = self.current_scale[7:] if not self.type2 else self.current_scale[:7]
        chance = random.random()
        condition = True if (self.check_for_palm_mute(position, 14) is True or
                             self.check_for_palm_mute(position, 12) is True) \
                            and current_duration >= 0.5 and self.ROOT_NOTE >= 35 else False

        if chance < 0.7 and current_duration > 0.25 and position % 1 == 0 and current_duration < 2:
            # add high notes from the scale
            current_note = random.choice(high_notes)
            self.diversify_notes(current_note, bar, position, current_duration)
            return current_note
        elif root_note is None:  # add 0's with (optional) 5ths
            if condition:
                fifth = {"pitch": self.ROOT_NOTE + 7, "duration": current_duration, "position": bar * 4 + position}
                self.notes_generated.append(fifth)
            return self.ROOT_NOTE
        else:  # for progression breakdown section
            if condition:
                fifth = {"pitch": root_note + 7, "duration": current_duration, "position": bar * 4 + position}
                self.notes_generated.append(fifth)
            return root_note

    def insert_rests(self, position):
        if self.type2:
            return -1
        rest_probability = random.random() if self.progression is None else 1  # no rests needed for a progression sect.
        if self.rest_condition(position, rest_probability, 0.02, 1):  # half note rest
            return self.rest_position_offset(position, 2)
        if self.rest_condition(position, rest_probability, 0.05, 0.5):  # quarter note rest
            return self.rest_position_offset(position, 1)
        if self.rest_condition(position, rest_probability, 0.05, 0.5):  # 8th note rest
            return self.rest_position_offset(position, 0.5)
        return -1

    def rest_position_offset(self, position, value):
        position += value
        self.root_notes_generated.clear()
        return position

    def rest_condition(self, position, rest_probability, value, pos):
        return rest_probability < value * len(self.root_notes_generated) and self.root_notes_generated[
            -1] == self.ROOT_NOTE and position % pos == 0 and \
               self.recent_note == self.ROOT_NOTE and self.recent_duration > 0.5

    def diversify_notes(self, current_note, bar, position, current_duration):
        chance = random.random()
        interval = self.interval_randomizer(current_note)

        if current_duration == 1:
            self.insert_diversified_note(bar, chance, current_duration, interval, position, 0.4)

        if current_duration == 2:
            self.insert_diversified_note(bar, chance, current_duration, interval, position, 0.66)

    def insert_diversified_note(self, bar, chance, current_duration, interval, position, chance_threshold):
        if chance < chance_threshold:
            note = {
                "pitch": interval,
                "duration": current_duration - 0.5,
                "position": bar * 4 + position + 0.5
            }
            self.notes_generated.append(note)

    def interval_randomizer(self, current_note):
        interval = INTERVALS[random.choice(list(INTERVALS.keys()))]

        if self.current_scale.index(current_note) + interval > len(self.current_scale) - 1:
            return self.current_scale[self.current_scale.index(current_note) - interval]
        else:
            return self.current_scale[self.current_scale.index(current_note) + interval]

    def palm_mute(self, bar, position, duration):
        if duration <= 0.5:
            self.palm_mute_12_14(bar, position)

        else:  # palm mute a long note with a certain chance
            palm_mute_chance = random.random()
            if palm_mute_chance < 0.4 and position != 0:
                self.palm_mute_12_14(bar, position)

    def palm_mute_12_14(self, bar, position):
        self.insert_palm_mute_note(bar, position, 14)
        self.insert_palm_mute_note(bar, position, 12, 0.25)

    def insert_palm_mute_note(self, bar, position, pitch, offset: float = 0.0):
        pm = {"pitch": pitch, "duration": 0.5 / 4, "position": bar * 4 + position - 0.125 + offset}
        self.notes_generated.append(pm)

    def check_for_palm_mute(self, position, pitch, tolerance=0.075):
        for note in self.notes_generated:
            if abs(note["position"] - position) <= tolerance and note["pitch"] == pitch:
                return True
        return False
