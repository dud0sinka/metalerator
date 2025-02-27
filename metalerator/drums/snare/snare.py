import random

from misc import velocity


def should_break(i, bars, repetition, fill_flag):
    return (fill_flag == 1 and i >= bars * 3) or \
           (fill_flag == 2 and i >= bars * 2.5 and repetition == 3) or \
           (fill_flag == 3 and i >= bars * 4 - 2) or \
           (fill_flag == 4 and i >= bars * 4 - 4)


def calculate_position(i, bars, repetition, start_pos):
    return i + bars * 4 * repetition + start_pos


def insert_ghost_notes(position, file):
    vel_before = velocity.main_velocity()  # ghost notes before the main hit
    pos_before = 0.5

    vel_after = int(velocity.main_velocity() // 1.5)  # after
    pos_after = 0.5

    for _ in range(generate_ghost_notes_before_snare()):
        vel_before = int(vel_before // 1.5)
        file.addNote(0, 0, 38, position - pos_before, 0.25, vel_before)
        pos_before -= 0.5

    for _ in range(generate_ghost_notes_after_snare()):
        file.addNote(0, 0, 38, position + pos_after, 0.25, vel_after)
        pos_after += 0.5


def generate_ghost_notes_before_snare():
    chance = random.random()
    ghost_note_count = 0

    if chance < 0.35:
        ghost_note_count += 1
    if chance < 0.2:
        ghost_note_count += 1
    if chance < 0.1:
        ghost_note_count += 1

    return ghost_note_count


def generate_ghost_notes_after_snare():
    chance = random.random()
    ghost_note_count = 0

    if chance < 0.3:
        ghost_note_count += 1
    if chance < 0.2:
        ghost_note_count += 1

    return ghost_note_count


class Snare:
    def __init__(self, start_pos):
        self.start_pos = start_pos

    def snare_double_time(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if should_break(i, bars, repetition, fill_flag):
                break
            position = calculate_position(i, bars, repetition, self.start_pos)
            if i % 1 == 0 and i != 0:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity())

    def snare_step(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if should_break(i, bars, repetition, fill_flag):
                break
            position = calculate_position(i, bars, repetition, self.start_pos)
            if i % 4 == 2:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity())
                insert_ghost_notes(position, file)

    def snare_half_step(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if should_break(i, bars, repetition, fill_flag):
                break
            position = calculate_position(i, bars, repetition, self.start_pos)
            if i % 8 == 4:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity())
                insert_ghost_notes(position, file)

    def snare_blast1(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if should_break(i, bars, repetition, fill_flag):
                break
            position = calculate_position(i, bars, repetition, self.start_pos)

            if i == 0:
                file.addNote(0, 0, 38, position + 0.5, 0.25, velocity.main_velocity() - 25)

            if i % 1 == 0 and i != 0:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity() - 10)
                file.addNote(0, 0, 38, position + 0.5, 0.25, velocity.main_velocity() - 25)

    def snare_blast2(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if should_break(i, bars, repetition, fill_flag):
                break
            position = calculate_position(i, bars, repetition, self.start_pos)

            if i % 1 == 0 and i != 0:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity() - 10)
                file.addNote(0, 0, 38, position + 0.33, 0.25, velocity.main_velocity() - 35)
                file.addNote(0, 0, 38, position + 0.66, 0.25, velocity.main_velocity() - 30)
