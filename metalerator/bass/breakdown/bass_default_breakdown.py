def create_bass_note(note):
    pitch = note["pitch"]
    if pitch > 48:
        pitch -= 12
    elif 29 <= pitch < 33:
        pitch += 12
    return {
        "pitch": pitch,
        "duration": note["duration"],
        "position": note["position"]
    }


class BassDefaultMelodicBreakdown:
    def __init__(self, guitar_notes):
        self.bass_notes = []
        self.current_low_note_position = -1
        self.last_16th_note = -1
        self.guitar_notes = guitar_notes

    def copy_guitar(self, file):
        for note in self.guitar_notes:
            if self.should_skip(note):
                continue

            if note["duration"] == 0.25:
                self.last_16th_note = note["position"]

            if note["pitch"] > 38 and note["position"] == self.current_low_note_position:
                continue

            if 29 <= note["pitch"] <= 38:
                self.current_low_note_position = note["position"]

            bass_note = create_bass_note(note)
            self.bass_notes.append(bass_note)

        self.bass_notes = self.check_for_the_same_positions()
        self.write(file)

    def should_skip(self, note):
        if 92 <= note["pitch"] <= 95:
            return True
        if note["pitch"] in (14, 12):
            return True
        if note["pitch"] > 48 and note["duration"] <= 0.5 and note["position"] != self.last_16th_note + 0.25:
            return True
        return False

    def check_for_the_same_positions(self):
        filtered_notes = [self.bass_notes[0]]

        for i in range(1, len(self.bass_notes)):
            current_note = self.bass_notes[i]
            if current_note["position"] != filtered_notes[-1]["position"]:
                filtered_notes.append(current_note)

        return filtered_notes

    def write(self, file):
        for note in self.bass_notes:
            file.addNote(0, 0, note["pitch"], note["position"], note["duration"], 120)
