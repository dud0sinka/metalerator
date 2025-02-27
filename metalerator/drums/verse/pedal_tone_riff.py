from drums import common
from drums.kick.kick import *
from drums.snare.snare import *

snare_variations = ["double_time", "step", "half-step", "blast1", "blast2"]
snare_weights = [4, 4, 4, 2, 1]  # Weights for snare variations, blast beats have lower weight
kick_variations = ["double_bass", "8th_kicks", "trr_trr"]
kick_weights = [2, 4, 4]  # Weights for kick variations, double bass has lower weight
cymbal_variations = ["double_time", "step"]


class DrumsPedalToneRiffVerse:
    def __init__(self, start_pos, chorus=False):
        self.previous_kick = ""  # used for generating opening cymbals
        self.previous_snare = ""  # used for generating opening cymbals
        self.current_cymbal = ""  # used for generating opening cymbals
        self.start_pos = start_pos
        self.snare = Snare(start_pos)
        self.kicks_generated = []
        self.kick = Kick(start_pos)
        self.blast_count = 0
        self.chorus = chorus

    def generate(self, file, data):
        bars = data["bars"]
        repetitions = data["repetitions"]

        for repetition in range(repetitions):
            fill_flag = 0
            if bars == 4:
                if repetition in [1, 3]:
                    fill_flag = 1
            if bars == 8:
                if 0 <= repetition <= 2:
                    fill_flag = 3  # fills are common for different sections thus the usage of multiple flags
                if repetition == 3:
                    fill_flag = 4

            kick_snare = self.generate_kick_and_snare(repetition, bars, fill_flag)
            cymbal_var = kick_snare[2]
            self.insert_snare(repetition, bars, file, kick_snare[1], fill_flag)
            self.generate_cymbals(repetition, bars, file, kick_snare[0], kick_snare[1], cymbal_var, fill_flag)
            self.previous_kick = kick_snare[0]
            self.previous_snare = kick_snare[1]

            if bars == 4:
                if repetition in [1, 3]:
                    common.choose_and_generate_fill(self.start_pos + bars * 4 * repetition + bars * 3, 1, file)

            if bars == 8:
                if 0 <= repetition <= 2:
                    common.choose_and_generate_fill(self.start_pos + bars * 4 * repetition + bars * 4 - 2, 0.5, file)
                if repetition == 3:
                    common.choose_and_generate_fill(self.start_pos + bars * 4 * repetition + bars * 4 - 4, 1, file)
        self.write_kicks_to_file(file)

    def write_kicks_to_file(self, file):
        for kick in self.kicks_generated:
            file.addNote(0, 0, 36, kick, 0.25, velocity.main_velocity())

    def generate_kick_and_snare(self, repetition, bars, fill_flag=0):
        chorus_variations = ["double_bass", "8th_kicks", "4"]
        kick_variation = self.choose_kick_variation() if self.chorus is False else \
            random.choices(chorus_variations, weights=[1, 4, 2], k=1)[0]

        allowed_snares_for_eight_bars = snare_variations.copy()
        allowed_snare_weights = snare_weights.copy()
        allowed_snares_for_eight_bars.remove("blast2")
        allowed_snare_weights.pop(snare_variations.index("blast2"))

        if bars == 8 and self.blast_count >= 1:
            allowed_snares_for_eight_bars.remove("blast1")
            allowed_snare_weights.pop(snare_variations.index("blast1"))

        snare_variation = ""
        cymbal_variation = ""
        """double bass"""
        if kick_variation == "double_bass":
            self.kicks_generated.extend(self.kick.double_bass(repetition, bars, fill_flag))

            if self.chorus is False:
                snare_variation = random.choices(snare_variations, weights=snare_weights, k=1)[0] if bars == 4 else \
                    random.choices(allowed_snares_for_eight_bars, weights=allowed_snare_weights, k=1)[0]
            else:
                snare_variation = random.choices(["double_time", "step", "half-step"], weights=[1, 4, 4], k=1)[0]

            if "step" in snare_variation or snare_variation == "blast1":
                cymbal_variation = random.choice(cymbal_variations)
            elif snare_variation == "double_time" or snare_variation == "blast2":
                cymbal_variation = "double_time"

            if "blast" in snare_variation:
                self.blast_count += 1
        """8ths kicks"""
        if kick_variation == "8th_kicks":
            allowed_snare_variations = snare_variations.copy()
            allowed_snare_weights = snare_weights.copy()
            allowed_snare_variations.remove("double_time")
            allowed_snare_weights.pop(snare_variations.index("double_time"))

            snare_variation = random.choices(allowed_snare_variations, weights=allowed_snare_weights, k=1)[0] if \
                self.chorus is False else random.choice(["step", "half-step"])

            blast_flag = 0 if "blast" not in snare_variation else 1
            if blast_flag == 1:
                self.blast_count += 1

            self.kicks_generated.extend(self.kick.eighth_kicks(repetition, bars, fill_flag, blast_flag, self.chorus))

            if snare_variation == "step" or snare_variation == "blast1":
                cymbal_variation = random.choice(cymbal_variations)
            elif snare_variation == "half-step":
                cymbal_variation = "step"
            elif snare_variation == "blast2":
                cymbal_variation = "double_time"
        """trr_trr beat"""
        if kick_variation == "trr_trr":
            self.kicks_generated.extend(self.kick.trr_trr(repetition, bars, fill_flag))
            snare_variation = "double_time"
            cymbal_variation = "double_time"
        ###################################
        if kick_variation == "4":
            self.kicks_generated.extend(self.kick.four_on_the_floor(repetition, bars, fill_flag, self.chorus))
            snare_variation = "step"
            cymbal_variation = random.choice(cymbal_variations)
        return kick_variation, snare_variation, cymbal_variation

    def insert_snare(self, repetition, bars, file, snare_variation, fill_flag=0):
        if snare_variation == "step":
            self.snare.snare_step(repetition, bars, file, fill_flag)

        if snare_variation == "half-step":
            self.snare.snare_half_step(repetition, bars, file, fill_flag)

        if snare_variation == "double_time":
            self.snare.snare_double_time(repetition, bars, file, fill_flag)

        if snare_variation == "blast1":
            self.snare.snare_blast1(repetition, bars, file, fill_flag)

        if snare_variation == "blast2":
            self.snare.snare_blast2(repetition, bars, file, fill_flag)

    @staticmethod
    def choose_kick_variation():
        variation = random.choices(kick_variations, weights=kick_weights, k=1)[0]
        return variation

    def fill_break(self, fill_flag, position, pos_cmp_var, bars):
        return (fill_flag == 1 and position == pos_cmp_var + bars * 3) or (
                fill_flag == 3 and position == pos_cmp_var + bars * 4 - 2) or (
                       fill_flag == 4 and position == pos_cmp_var + bars * 4 - 4)

    def generate_cymbals(self, repetition, bars, file, current_kick, current_snare, cymbal_var, fill_flag=0):
        allowed_cymbals = common.power_hand.copy()

        # check if the current snare is a form of blastbeat
        blast_check = True if "blast" in current_snare else False
        if blast_check:
            allowed_cymbals.clear()
            allowed_cymbals.extend([51, 53, 52, 55, 60])

        if current_kick != self.previous_kick or current_snare != self.previous_snare:
            self.current_cymbal = random.choice(allowed_cymbals) if cymbal_var != "double_time" else random.choice(
                common.double_time_power_hand)  # conditions for current power hand change

        for i in range(bars * 4):
            position = i + bars * 4 * repetition + self.start_pos
            pos_cmp_var = self.start_pos + bars * 4 * repetition

            if self.fill_break(fill_flag, position, pos_cmp_var, bars):
                break

            if (position % 16 == 0) or (
                    position == bars * 4 * repetition + self.start_pos and current_snare != self.previous_snare):
                common.opening_cymbals(file, position, 1)  # opening cymbals

            if position % 16 != 0 and (
                    (i % 2 == 0 and cymbal_var == "step") or (i % 1 == 0 and cymbal_var == "double_time")):
                cymbal_velocity = velocity.main_velocity()
                if blast_check:
                    cymbal_velocity -= 15

                file.addNote(0, 0, self.current_cymbal, position, 0.25, cymbal_velocity)

            if i % 2 == 1:  # add a random splash on a downbeat
                splash_chance = random.random()
                splash_pos = position if cymbal_var != "double_time" else position - 0.5
                if splash_chance < 0.2:
                    file.addNote(0, 0, 55, splash_pos, 0.25, velocity.main_velocity())
