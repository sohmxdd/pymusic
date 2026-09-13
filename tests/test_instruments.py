import unittest
import numpy as np
from pymusic.instruments.registry import InstrumentRegistry
from pymusic.instruments.base import Instrument

class TestInstruments(unittest.TestCase):
    def setUp(self):
        self.registry = InstrumentRegistry()

    def test_default_instruments_registered(self):
        available = self.registry.available()
        for name in ["piano", "harpsichord", "synth", "guitar", "saw", "drums", "square"]:
            self.assertIn(name, available)

    def test_instrument_polymorphism_render(self):
        for name in self.registry.available():
            inst = self.registry.get(name)
            self.assertIsInstance(inst, Instrument)
            sound = inst.render_note(frequency=440.0, duration=0.1, velocity=100, sample_rate=44100)
            self.assertEqual(len(sound), int(0.1 * 44100))
            self.assertTrue(np.all(np.isfinite(sound)))
            self.assertLessEqual(np.max(np.abs(sound)), 2.0)

    def test_zero_duration_or_velocity(self):
        inst = self.registry.get("piano")
        zero_sound = inst.render_note(frequency=440.0, duration=0.0, velocity=100, sample_rate=44100)
        self.assertEqual(len(zero_sound), 0)
        silent_sound = inst.render_note(frequency=440.0, duration=0.1, velocity=0, sample_rate=44100)
        self.assertTrue(np.all(silent_sound == 0.0))

if __name__ == "__main__":
    unittest.main()
