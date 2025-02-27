import random


def default_kick(repetition, bars, kick_list, kicks_generated,
                 fill_flag=0):  # follows the pattern of the guitar
    for i in kick_list:
        j = kick_list[0]
        if (fill_flag == 1 and i >= bars * 4 - 4 + j) or (
                fill_flag == 2 and i >= bars * 4 - 6 + j and repetition in [3, 7]) or \
                (fill_flag == 3 and i == bars * 4 - 2 + j) or (fill_flag == 4 and i == bars * 4 - 4 + j):
            break
        kicks_generated.append(i + bars * 4 * repetition)
    return kicks_generated


def break_for_fill(i, fill_flag, bars, repetition):
    return (fill_flag == 1 and i == bars * 4 - 4) or (
            fill_flag == 2 and i >= bars * 4 - 6 and repetition in [3, 7]) or \
           (fill_flag == 3 and i == bars * 4 - 2) or (fill_flag == 4 and i == bars * 4 - 4)


class Kick:
    def __init__(self, start_pos):
        self.start_pos = start_pos

    def four_on_the_floor(self, repetition, bars, fill_flag=0, chorus=False):
        kicks = []
        for i in range(0, bars * 4):
            if break_for_fill(i, fill_flag, bars, repetition):
                break
            if i % 4 == 0:
                kicks.append(i + bars * 4 * repetition + self.start_pos)
            if i % 2 == 0 and i != 0:
                self.kick_bursts_before_snare(repetition, bars, i, kicks, 4, chorus)
        return kicks

    def kick_bursts_before_snare(self, repetition, bars, i, kicks, variation=4, chorus=False):
        burst_chance = random.random()
        if chorus:
            burst_chance -= 0.3

        if burst_chance < 0.4 / variation:
            if variation == 2:
                kicks.append(i + bars * 4 * repetition + self.start_pos)
            kicks.append(i + bars * 4 * repetition - 0.25 + self.start_pos)
            kicks.append(i + bars * 4 * repetition - 0.5 + self.start_pos)
            if variation == 4:
                self.kicks_after_snare(repetition, bars, kicks, i)

        if burst_chance < 0.2 / variation:
            kicks.append(i + bars * 4 * repetition - 0.75 + self.start_pos)
            kicks.append(i + bars * 4 * repetition - 1 + self.start_pos)
            if variation == 4:
                self.kicks_after_snare(repetition, bars, kicks, i)

    def kicks_after_snare(self, repetition, bars, kicks, i):
        kick_after_snare_chance = random.random()
        available_positions = [0.5, 0.75, 1, 1.5]

        if kick_after_snare_chance < 0.25:
            position = random.choice(available_positions)
            kicks.append(i + bars * 4 * repetition + position + self.start_pos)
            available_positions.remove(position)
            if position == 0.75:
                kicks.append(i + bars * 4 * repetition + 1.5 + self.start_pos)
                kick_after_snare_chance = 1

        if kick_after_snare_chance < 0.15:
            position = random.choice(available_positions)
            kicks.append(i + bars * 4 * repetition + position + self.start_pos)
            available_positions.remove(position)

        if kick_after_snare_chance < 0.1:
            position = random.choice(available_positions)
            kicks.append(i + bars * 4 * repetition + position + self.start_pos)
            available_positions.remove(position)

    def double_bass(self, repetition, bars, fill_flag=0):
        kicks = []
        for i in range(0, bars * 4):
            if break_for_fill(i, fill_flag, bars, repetition):
                break
            j = 0
            for _ in range(4):
                kicks.append(i + bars * 4 * repetition + j + self.start_pos)
                j += 0.25
        return kicks

    def eighth_kicks(self, repetition, bars, fill_flag=0, blast_flag=0, chorus=False):
        kicks = []
        for i in range(0, bars * 4):
            if break_for_fill(i, fill_flag, bars, repetition):
                break
            j = 0
            for _ in range(2):
                kicks.append(i + bars * 4 * repetition + j + self.start_pos)
                j += 0.5
                if i % 2 == 0 and i != 0 and blast_flag == 0:
                    self.kick_bursts_before_snare(repetition, bars, i, kicks, 8, chorus)
        return kicks

    def two_on_the_floor(self, repetition, bars, fill_flag=0):
        kicks = []
        for i in range(0, bars * 4):
            if break_for_fill(i, fill_flag, bars, repetition):
                break
            if i % 8 == 0:
                kicks.append(i + bars * 4 * repetition + self.start_pos)
            if i % 4 == 0 and i != 0:
                self.kick_bursts_before_snare(repetition, bars, i, kicks, 2)
        return kicks

    def trr_trr(self, repetition, bars, fill_flag=0):
        kicks = []
        for i in range(0, bars * 4):
            if break_for_fill(i, fill_flag, bars, repetition):
                break
            if i % 1 == 0:
                kicks.append(i + bars * 4 * repetition + self.start_pos + 0.5)
                kicks.append(i + bars * 4 * repetition + self.start_pos + 0.75)
            if i == 0:
                kicks.append(i + bars * 4 * repetition + self.start_pos)
        return kicks
