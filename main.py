import numpy as np 
import soundfile as sf 

sample_rate=44100
duration=2
t= np.linspace(
    0,
    duration,
    int(sample_rate*duration),
    endpoint=False
)
frequency = 440

wave = np.sin(2 * np.pi * frequency * t)

sf.write("note.wav", wave, sample_rate) 

def note_freq(note):
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