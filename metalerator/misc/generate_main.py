import random

from misc.generate_song import GenerateSong


def generate(r_gtr_MIDI, dr_MIDI, bass_MIDI, l_gtr_MIDI, amb_MIDI) -> None:
    """
    Generates a song structure by sequentially generating different sections of the song.

    Parameters:
    - r_gtr_MIDI: MIDI data for the rhythm guitar.
    - dr_MIDI: MIDI data for the drums.
    - bass_MIDI: MIDI data for the bass.
    - l_gtr_MIDI: MIDI data for the left guitar.
    - amb_MIDI: MIDI data for the ambient sounds.
    """
    song = GenerateSong(r_gtr_MIDI, dr_MIDI, bass_MIDI, l_gtr_MIDI, amb_MIDI)

    # Generate intro section
    position = song.generate_intro()
    song.start_pos = position

    # Generate first verse section
    position = song.generate_verse()
    song.start_pos = position

    # Generate first pre-chorus section
    position = song.generate_pre_chorus()
    song.start_pos = position

    # Generate first chorus section
    position = song.generate_chorus()
    song.start_pos = position

    # Generate first post-chorus section
    position = song.generate_post_chorus()
    song.start_pos = position

    # Generate second verse section
    position = song.generate_verse(random.choice([2, 4]))
    song.start_pos = position

    # Generate second pre-chorus section optionally
    if random.random() < 0.45:
        position = song.generate_pre_chorus()
    song.start_pos = position

    # Generate second chorus section optionally
    position = song.generate_chorus()
    song.start_pos = position

    # Generate pre-breakdown section
    position = song.generate_pre_breakdown()
    song.start_pos = position

    # Generate breakdown section
    position = song.generate_breakdown()
    song.start_pos = position

    # Generate third chorus section optionally
    position = song.generate_chorus()
    song.start_pos = position

    # Generate outro section
    song.generate_outro()
