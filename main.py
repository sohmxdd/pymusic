import numpy as np 
import soundfile as sf 

sample_rate=44100

def note_frequency(note):
    notes={
        "C": 0,
        "C#": 1,
        "D": 2,
        "D#": 3,
        "E": 4,
        "F": 5,
        "F#": 6,
        "G": 7,
        "G#": 8,
        "A": 9,
        "A#": 10,
        "B": 11
    }
    name = note[:-1]
    octave = int(note[-1])
    midi_number=notes[name]+12*(octave+1)
    frequency= 440 * 2 ** ((midi_number - 69) / 12)
    return frequency
print(note_frequency("A4"))
print(note_frequency("C4"))
print(note_frequency("E4"))

def generate_note(note,duration):
    frequency= note_frequency(note)
    t = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        endpoint=False
    )
    wave=np.sin(2*np.pi*frequency*t)
    return wave 
melody=[
    ("C4", 0.5),
    ("E4", 0.5),
    ("G4", 0.5),
    ("E4", 0.5)
]
melody_wave=np.array([])
for note, duration in melody:
    wave= generate_note(note, duration)
    melody_wave=np.concatenate(
        (melody_wave,wave)
    )
sf.write(
    "melody.wav",
    melody_wave,
    sample_rate
)
print("A4 =", note_frequency("A4"))
print("C4 =", note_frequency("C4"))
print("A5 =", note_frequency("A5"))

print("Melody generated!")

