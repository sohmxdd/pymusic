import numpy as np
import pytest
from pymusic.tuning import FrequencyTuner
from pymusic.envelopes import ExponentialDecayEnvelope, ADSREnvelope

def test_frequency_tuner_standard():
    tuner = FrequencyTuner()
    assert abs(tuner.midi_to_frequency(69) - 440.0) < 1e-4
    assert abs(tuner.midi_to_frequency(57) - 220.0) < 1e-4
    assert abs(tuner.midi_to_frequency(81) - 880.0) < 1e-4

def test_frequency_to_midi_roundtrip():
    tuner = FrequencyTuner()
    freq = tuner.midi_to_frequency(60)
    midi_note = tuner.frequency_to_midi(freq)
    assert abs(midi_note - 60.0) < 1e-4

def test_exponential_decay_envelope():
    env_gen = ExponentialDecayEnvelope(decay=4.0)
    env = env_gen.generate(length=44100, sample_rate=44100)
    assert len(env) == 44100
    assert abs(env[0] - 1.0) < 1e-4
    assert env[-1] < env[0]
    assert np.all(env >= 0.0)

def test_adsr_envelope():
    adsr = ADSREnvelope(attack=0.01, decay=0.02, sustain=0.5, release=0.02)
    env = adsr.generate(length=4410, sample_rate=44100)
    assert len(env) == 4410
    assert np.all(env >= 0.0)
    assert np.all(env <= 1.0)
