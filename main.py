import mido
import numpy as np
import soundfile as sf

SR = 44100
BPM = 104
BEAT = 60 / BPM

mid = mido.MidiFile("Kanye West - Stronger.mid")


def midi_frequency(note):
    return 440 * 2 ** ((note - 69) / 12)


def envelope(length, decay=4):
    t = np.arange(length) / SR
    return np.exp(-decay * t)


def generate_note(midi_note, duration, velocity, instrument):
    frequency = midi_frequency(midi_note)
    length = int(duration * SR)
    t = np.arange(length) / SR

    if instrument == "piano":
        wave = (
            np.sin(2 * np.pi * frequency * t)
            + 0.5 * np.sin(4 * np.pi * frequency * t)
            + 0.25 * np.sin(6 * np.pi * frequency * t)
        )
        wave *= envelope(length, 2.5)

    elif instrument == "harpsichord":
        wave = (
            np.sin(2 * np.pi * frequency * t)
            + 0.35 * np.sin(4 * np.pi * frequency * t)
            + 0.15 * np.sin(8 * np.pi * frequency * t)
        )
        wave *= envelope(length, 6)

    elif instrument == "synth":
        saw = 2 * ((frequency * t) % 1) - 1
        sine = np.sin(2 * np.pi * frequency * t)
        wave = 0.65 * saw + 0.35 * sine
        wave *= envelope(length, 2)

    elif instrument == "guitar":
        wave = (
            np.sin(2 * np.pi * frequency * t)
            + 0.3 * np.sin(4 * np.pi * frequency * t)
        )
        wave *= envelope(length, 5)

    elif instrument == "saw":
        wave = 2 * ((frequency * t) % 1) - 1
        wave *= envelope(length, 3)

    else:
        wave = np.zeros(length)

    velocity_gain = velocity / 127
    return wave * velocity_gain


def extract_notes(track):
    absolute_tick = 0
    active = {}
    notes = []

    for message in track:
        absolute_tick += message.time

        if message.type == "note_on" and message.velocity > 0:
            active[message.note] = (absolute_tick, message.velocity)

        elif message.type == "note_off" or (
            message.type == "note_on" and message.velocity == 0
        ):
            if message.note in active:
                start_tick, velocity = active.pop(message.note)
                duration = absolute_tick - start_tick
                notes.append((start_tick, duration, message.note, velocity))

    return notes


instruments = [
    "piano",
    "harpsichord",
    "piano",
    "synth",
    "drums",
    "guitar",
    "saw",
]

total_ticks = 0
for track in mid.tracks:
    ticks = sum(message.time for message in track)
    total_ticks = max(total_ticks, ticks)

total_beats = total_ticks / mid.ticks_per_beat
total_seconds = total_beats * BEAT

master = np.zeros(int(total_seconds * SR) + SR)

for index, track in enumerate(mid.tracks):
    notes = extract_notes(track)
    instrument = instruments[min(index, len(instruments) - 1)]

    for start_tick, duration_tick, midi_note, velocity in notes:
        start_seconds = start_tick / mid.ticks_per_beat * BEAT
        duration_seconds = duration_tick / mid.ticks_per_beat * BEAT
        sound = generate_note(midi_note, duration_seconds, velocity, instrument)

        start_sample = int(start_seconds * SR)
        end_sample = min(start_sample + len(sound), len(master))

        master[start_sample:end_sample] += sound[:end_sample - start_sample]

master *= 0.15
master = np.tanh(master)

peak = np.max(np.abs(master))
if peak > 0:
    master /= peak
    master *= 0.92

sf.write("stronger_code.wav",master,SR)




