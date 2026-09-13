import unittest
import numpy as np
from pymusic.tuning import FrequencyTuner
from pymusic.envelopes import ExponentialDecayEnvelope, ADSREnvelope

class TestTuningAndEnvelopes(unittest.TestCase):
    def test_frequency_tuner_standard(self):
        tuner = FrequencyTuner()
        self.assertAlmostEqual(tuner.midi_to_frequency(69), 440.0, places=3)
        self.assertAlmostEqual(tuner.midi_to_frequency(57), 220.0, places=3)
        self.assertAlmostEqual(tuner.midi_to_frequency(81), 880.0, places=3)

    def test_frequency_to_midi_roundtrip(self):
        tuner = FrequencyTuner()
        freq = tuner.midi_to_frequency(60)
        midi_note = tuner.frequency_to_midi(freq)
        self.assertAlmostEqual(midi_note, 60.0, places=3)

    def test_exponential_decay_envelope(self):
        env_gen = ExponentialDecayEnvelope(decay=4.0)
        env = env_gen.generate(length=44100, sample_rate=44100)
        self.assertEqual(len(env), 44100)
        self.assertAlmostEqual(env[0], 1.0, places=4)
        self.assertLess(env[-1], env[0])
        self.assertTrue(np.all(env >= 0.0))

    def test_adsr_envelope(self):
        adsr = ADSREnvelope(attack=0.01, decay=0.02, sustain=0.5, release=0.02)
        env = adsr.generate(length=4410, sample_rate=44100)
        self.assertEqual(len(env), 4410)
        self.assertTrue(np.all(env >= 0.0))
        self.assertTrue(np.all(env <= 1.0))

if __name__ == "__main__":
    unittest.main()
