import random
from misc import velocity
from rhythm_guitar.intro import intro
from drums.common import choose_and_generate_fill
from rhythm_guitar.breakdown.default_melodic import RGuitarDefaultMelodicBreakdown


def choose_type():
    return random.choice(["none", "intro", "drum_fill", "ambience"])


def generate(gtr_file, drum_file, bass_file, amb_file, lead_file, start_pos, root_note, progression, scale):
    variation = choose_type()
    if variation == "none":
        return start_pos

    if variation == "intro":
        intro_obj = intro.RGuitarIntro(root_note, start_pos)
        pos = intro_obj.generate(gtr_file, drum_file, bass_file, random.randint(2, 4),
                                 random.choice([amb_file, lead_file]))
        return start_pos + pos

    if variation == "drum_fill":
        bars = random.randint(1, 2)
        drum_fill_variation(bars, drum_file, start_pos)
        return start_pos + bars * 4

    if variation == "ambience":
        reps = random.choice([2, 4])
        pos = RGuitarDefaultMelodicBreakdown(start_pos, root_note, progression, scale, None, amb_file). \
            generate(None, drum_file, bass_file, 4, reps, True)
        return pos


def drum_fill_variation(bars, drum_file, start_pos):
    choose_and_generate_fill(start_pos, bars - 0.5, drum_file, False)
    drum_file.addNote(0, 0, 36, start_pos + bars * 4 - 2, 0.25, velocity.main_velocity())
    drum_file.addNote(0, 0, 38, start_pos + bars * 4 - 2, 0.25, velocity.main_velocity())
    drum_file.addNote(0, 0, 41, start_pos + bars * 4 - 2, 0.25, velocity.main_velocity())
