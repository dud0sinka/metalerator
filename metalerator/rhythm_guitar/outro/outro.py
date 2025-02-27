import random

import drums.common
import rhythm_guitar.intro.intro
from misc import velocity
from rhythm_guitar.verse.pedal_tone_riff import RGuitarPedalToneRiff


def choose_outro():
    return random.choice(["chug", "verse_bar_chug", "long0"])


def write_chug(gtr_file, drum_file, bass_file, start_pos, root_note):
    gtr_file.addNote(0, 0, root_note, start_pos, 1.5, velocity.main_velocity())
    if root_note <= 33:
        root_note += 12
    bass_file.addNote(0, 0, root_note, start_pos, 1.5, velocity.main_velocity())
    drum_file.addNote(0, 0, 36, start_pos, 0.25, velocity.main_velocity())
    if random.random() < 0.51:
        drum_file.addNote(0, 0, 38, start_pos, 0.25, velocity.main_velocity())
        drum_file.addNote(0, 0, 41, start_pos, 0.25, velocity.main_velocity())
    else:
        drums.common.opening_cymbals(drum_file, start_pos, 2)


def generate(gtr_file, drum_file, bass_file, start_pos, root_note):
    variation = choose_outro()

    if variation == "chug":
        write_chug(gtr_file, drum_file, bass_file, start_pos, root_note)
    if variation == "long0":
        bars = random.choice([2, 4])
        rhythm_guitar.intro.intro.RGuitarIntro(root_note, start_pos, "open0_drum_fill").generate(gtr_file, drum_file,
                                                                                                 bass_file, bars,
                                                                                                 None)
        write_chug(gtr_file, drum_file, bass_file, start_pos + bars * 4, root_note)
    if variation == "verse_bar_chug":
        verse_bar = RGuitarPedalToneRiff(start_pos, root_note)
        pos = verse_bar.generate(gtr_file, drum_file, bass_file, 4, 1)
        write_chug(gtr_file, drum_file, bass_file, pos, root_note)

