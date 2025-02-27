from misc import velocity
from drums import common
import random


class DrumsIntoOpen0DrumFill:
    def __init__(self, file, start_pos=0):
        self.file = file
        self.start_pos = start_pos

    def generate(self, bars, snare_fill):
        self.kick_and_openers()

        snare_offset = 0
        if snare_fill:
            snare_offset = 0.5

        if bars == 2:
            if random.random() > 0.5:  # randomize where the fill begins
                common.choose_and_generate_fill(4 + self.start_pos, 1 - snare_offset, self.file)
                common.generate_snare_fill(bars * 4 - 2 + self.start_pos, snare_offset, self.file)
            else:
                common.choose_and_generate_fill(6 + self.start_pos, 0.5 - snare_offset, self.file)
                common.generate_snare_fill(bars * 4 - 2 + self.start_pos, snare_offset, self.file)
        elif bars == 4:
            if random.random() > 0.5:  # randomize where the fill begins
                common.choose_and_generate_fill(8 + self.start_pos, 2 - snare_offset, self.file)
                common.generate_snare_fill(bars * 4 - 2 + self.start_pos, snare_offset, self.file)
                self.insert_cymbals_on_upbeat(8 + self.start_pos)
            else:
                common.choose_and_generate_fill(12 + self.start_pos, 1 - snare_offset, self.file)
                common.generate_snare_fill(bars * 4 - 2 + self.start_pos, snare_offset, self.file)
                self.insert_cymbals_on_upbeat(12 + self.start_pos)

    def kick_and_openers(self):
        self.file.addNote(0, 0, 36, self.start_pos, 0.25, velocity.main_velocity())
        common.opening_cymbals(self.file, self.start_pos)

    def insert_cymbals_on_upbeat(self, fill_start_pos):
        if random.random() > 0.7:
            cymbal = random.choice(common.power_hand)
            half_time = random.random() > 0.5
            positions = [2, 6, 10] if half_time else [1, 3, 5, 7, 9, 11]

            for pos in positions:
                if pos >= fill_start_pos:
                    break
                self.file.addNote(0, 0, cymbal, pos, 0.25, velocity.main_velocity())
