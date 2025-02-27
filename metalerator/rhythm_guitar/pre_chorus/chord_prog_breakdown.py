from rhythm_guitar.breakdown.default_melodic import *


def generate(gtr_file, drum_file, bass_file, start_pos, root_note, progression, scale):
    reps = random.choice([2, 4])
    guit = RGuitarDefaultMelodicBreakdown(start_pos, root_note, progression, scale)
    pos = guit.generate(gtr_file, drum_file, bass_file, 4, reps, True)

    return pos
