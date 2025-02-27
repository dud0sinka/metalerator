import random

import rhythm_guitar.outro.outro
from misc import velocity
from rhythm_guitar.breakdown.default_melodic import RGuitarDefaultMelodicBreakdown
from rhythm_guitar.chorus.chorus import RGuitarChorus
from rhythm_guitar.intro.intro import RGuitarIntro
from rhythm_guitar.pre_breakdown import pre_breakdown
from rhythm_guitar.pre_chorus import chord_prog_breakdown
from rhythm_guitar.verse.pedal_tone_riff import RGuitarPedalToneRiff
from drums import common


class GenerateSong:
    def __init__(self, rhythm_midi, drums_midi, bass_midi, lead_midi, amb_midi):
        self.root_note = 0
        self.r_gtr_MIDI = rhythm_midi
        self.dr_MIDI = drums_midi
        self.bass_MIDI = bass_midi
        self.l_gtr_MIDI = lead_midi
        self.amb_MIDI = amb_midi
        self.start_pos = 0
        self.verse = None
        self.chorus = None
        self.pre_chorus_variation = ""
        self.pre_chorus_variations = ["normal", "rest", "none"]

    def generate_intro(self) -> float:
        intro = RGuitarIntro(random.randint(29, 38), self.start_pos)
        intro_bars = random.choice([2, 4])

        pos = intro.generate(self.r_gtr_MIDI, self.dr_MIDI, self.bass_MIDI, intro_bars, self.amb_MIDI)
        self.root_note = intro.get_root()

        return pos

    def generate_verse(self, repetitions=4) -> float:
        self.verse = RGuitarPedalToneRiff(self.start_pos, self.root_note)
        pos = self.verse.generate(self.r_gtr_MIDI, self.dr_MIDI, self.bass_MIDI, 4, repetitions)

        return pos

    def choose_pre_chorus(self) -> None:
        weight = 0.5 if self.pre_chorus_variation == "normal" else 4
        self.pre_chorus_variation = random.choices(self.pre_chorus_variations, weights=[weight, 2, 1], k=1)[0]

    def generate_pre_chorus(self) -> float:
        self.choose_pre_chorus()

        if self.pre_chorus_variation == "normal":
            pos = chord_prog_breakdown.generate(self.r_gtr_MIDI, self.dr_MIDI, self.bass_MIDI, self.start_pos,
                                                self.root_note, self.verse.progression,
                                                self.verse.current_scale)

            return pos
        elif self.pre_chorus_variation == "rest":
            self.pre_chorus_rest_variation()

            return self.start_pos + 4
        elif self.pre_chorus_variation == "none":
            return self.start_pos

    def pre_chorus_rest_variation(self):
        self.dr_MIDI.addNote(0, 0, 36, self.start_pos, 0.25, velocity.main_velocity())
        self.dr_MIDI.addNote(0, 0, 38, self.start_pos, 0.25, velocity.main_velocity())
        self.dr_MIDI.addNote(0, 0, 41, self.start_pos, 0.25, velocity.main_velocity())
        self.r_gtr_MIDI.addNote(0, 0, self.root_note, self.start_pos, 1.5, velocity.main_velocity())
        root = self.root_note
        if root <= 33:
            root += 12
        self.bass_MIDI.addNote(0, 0, root, self.start_pos, 1.5, velocity.main_velocity())

    def generate_chorus(self) -> float:
        fill_size = random.choices([0, 0.5, 1, 2], weights=[4, 1, 1, 1], k=1)
        self.start_pos = common.choose_and_generate_fill(self.start_pos, fill_size[0], self.dr_MIDI)
        # optional fill before chorus

        self.chorus = RGuitarChorus(self.start_pos, self.root_note)
        pos = self.chorus.generate(self.r_gtr_MIDI, self.dr_MIDI, self.bass_MIDI, 4, 4, self.l_gtr_MIDI)

        return pos

    def generate_post_chorus(self) -> float:
        pos = self.generate_pre_chorus()
        self.pre_chorus_variation = None

        return pos

    def generate_pre_breakdown(self) -> float:
        return pre_breakdown.generate(self.r_gtr_MIDI, self.dr_MIDI, self.bass_MIDI,
                                      self.amb_MIDI, self.l_gtr_MIDI, self.start_pos,
                                      self.root_note, self.chorus.progression, self.chorus.current_scale)

    def generate_breakdown(self) -> float:
        breakdown = RGuitarDefaultMelodicBreakdown(self.start_pos, self.root_note, None, None, self.l_gtr_MIDI,
                                                   self.amb_MIDI)
        pos = breakdown.generate(self.r_gtr_MIDI, self.dr_MIDI, self.bass_MIDI, 4, 4)

        return pos

    def generate_outro(self) -> None:
        rhythm_guitar.outro.outro.generate(self.r_gtr_MIDI, self.dr_MIDI, self.bass_MIDI, self.start_pos,
                                                   self.root_note)
