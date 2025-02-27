import os
import sys
from midiutil import MIDIFile
from misc import generate_main

executable_path = os.path.dirname(sys.argv[0])
midis_dir = os.path.normpath(os.path.join(executable_path, "midis"))
os.makedirs(midis_dir, exist_ok=True)

r_gtr_MIDI = MIDIFile(1)
dr_MIDI = MIDIFile(1)
bass_MIDI = MIDIFile(1)
l_gtr_MIDI = MIDIFile(1)
amb_MIDI = MIDIFile(1)

generate_main.generate(r_gtr_MIDI, dr_MIDI, bass_MIDI, l_gtr_MIDI, amb_MIDI)

with open(os.path.join(midis_dir, "rhythm_guitar.mid"), "wb") as output_file:
    r_gtr_MIDI.writeFile(output_file)
with open(os.path.join(midis_dir, "drums.mid"), "wb") as output_file:
    dr_MIDI.writeFile(output_file)
with open(os.path.join(midis_dir, "bass.mid"), "wb") as output_file:
    bass_MIDI.writeFile(output_file)
with open(os.path.join(midis_dir, "lead.mid"), "wb") as output_file:
    l_gtr_MIDI.writeFile(output_file)
with open(os.path.join(midis_dir, "amb.mid"), "wb") as output_file:
    amb_MIDI.writeFile(output_file)

print("Generated succesfully!")
print("MIDIs saved to ", midis_dir, ".")
