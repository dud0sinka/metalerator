import random

import drums.common
from misc import velocity
from drums.intro.open0_drum_fill import DrumsIntoOpen0DrumFill as Drums
from bass.intro.intro import BassIntoOpen0DrumFill as Bass
from rhythm_guitar.verse.pedal_tone_riff import RGuitarPedalToneRiff as Guitar
from rhythm_guitar import common as common
import rhythm_guitar.verse.pedal_tone_riff as guitar
from midiutil.MidiFile import MIDIFile


def slide_or_dead_notes(gtr_file: MIDIFile, bars: int, start_pos=0) -> bool:
    if random.random() > 0.5:
        gtr_file.addNote(0, 0, 102, start_pos + bars * 4 - 2, 1, velocity.main_velocity())  # slide
        gtr_file.addNote(0, 0, 101, start_pos + bars * 4 - 1, 1, velocity.main_velocity())
        return False
    else:
        gtr_file.addNote(0, 0, 94, start_pos + bars * 4 - 2, 0.5, velocity.main_velocity())  # dead notes
        gtr_file.addNote(0, 0, 94, start_pos + bars * 4 - 1.5, 0.5, velocity.main_velocity())
        gtr_file.addNote(0, 0, 94, start_pos + bars * 4 - 1, 0.5, velocity.main_velocity())
        gtr_file.addNote(0, 0, 94, start_pos + bars * 4 - 0.5, 0.5, velocity.main_velocity())
        return True


def choose_intro() -> str:
    intros = ["open0_drum_fill", "none", "drum_fill", "ambience"]
    return random.choice(intros)


class RGuitarIntro:

    def __init__(self, root=0, start_pos=0, intro=None):
        self.ROOT_NOTE = root
        self.intro = choose_intro() if intro is None else intro
        self.start_pos = 0 if start_pos == 0 else start_pos

    def get_root(self):
        return self.ROOT_NOTE

    def generate(self, gtr_file: MIDIFile, drum_file: MIDIFile, bass_file: MIDIFile, bars: int, amb_file: MIDIFile = None) -> int:
        if self.intro == "open0_drum_fill":
            root_copy = self.ROOT_NOTE if self.ROOT_NOTE > 34 else self.ROOT_NOTE + 12

            gtr_file.addNote(0, 0, root_copy, 0 + self.start_pos, bars * 4 - 2, velocity.main_velocity())
            gtr_file.addNote(0, 0, root_copy + 7, 0 + self.start_pos, bars * 4 - 2, velocity.main_velocity())
            gtr_file.addNote(0, 0, root_copy + 12, 0 + self.start_pos, bars * 4 - 2, velocity.main_velocity())

            dead_notes = slide_or_dead_notes(gtr_file, bars, self.start_pos)

            Drums(drum_file, self.start_pos).generate(bars, dead_notes)
            Bass(self.ROOT_NOTE, bass_file, 0 + self.start_pos).generate(bars)
        elif self.intro == "drum_fill":
            bars //= 2
            drums.common.choose_and_generate_fill(0 + self.start_pos, bars, drum_file, True)
        elif self.intro == "none":
            return 0
        elif self.intro == "ambience":
            lets_choose_a_scale = common.choose_scale(guitar.SCALES)
            scale = common.fill_scale(self.ROOT_NOTE, lets_choose_a_scale, [], self.ROOT_NOTE)
            progression = random.choice(list(guitar.CHORD_PROGRESSIONS.values()))
            Guitar(0 + self.start_pos, self.ROOT_NOTE, progression, scale).generate(amb_file, None, None, bars, 0, False, False, True)
            fill_size = random.choice([0, 0.5, 1])
            drums.common.choose_and_generate_fill(bars * 4 - fill_size * 4 + self.start_pos, fill_size, drum_file, True)
        return bars * 4  # starting position for the next section
