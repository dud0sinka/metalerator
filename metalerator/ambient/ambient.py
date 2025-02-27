import random

from rhythm_guitar.verse.pedal_tone_riff import RGuitarPedalToneRiff as Guitar


def generate(amb_file, number_of_bars, repetitions, start_pos, root, scale, is_lead, amb_guarantee=False):
    """
    This function generates an optional ambient guitar section for a song using pedal_tone_riff.py module.
    """
    if is_lead:
        repetitions //= 2
    else:
        if random.random() > 0.69 and not amb_guarantee:
            start_pos += 32
            repetitions //= 2

    if random.random() > 0.45 or amb_guarantee:
        Guitar(start_pos, root, [0, 0, 0, 0], scale).generate(amb_file, None, None,
                                                              number_of_bars, repetitions,
                                                              False, False, True)
