import unittest
import os
import numpy as np
from pymusic.config import AudioConfig
from pymusic.engine import SynthEngine

class TestSynthEngineIntegration(unittest.TestCase):
    def setUp(self):
        self.midi_path = "Kanye West - Stronger.mid"
        self.output_wav = "test_output.wav"
        self.config = AudioConfig(sample_rate=22050, bpm=104.0, master_gain=0.15, peak_ceiling=0.92)
        self.engine = SynthEngine(config=self.config)

    def tearDown(self):
        if os.path.exists(self.output_wav):
            try:
                os.remove(self.output_wav)
            except OSError:
                pass

    def test_render_midi_array(self):
        if not os.path.exists(self.midi_path):
            self.skipTest("Midi file not found in current directory")
        audio = self.engine.render_midi(self.midi_path, ["piano", "synth", "guitar"])
        self.assertIsInstance(audio, np.ndarray)
        self.assertGreater(len(audio), 0)
        self.assertTrue(np.all(np.isfinite(audio)))
        self.assertLessEqual(np.max(np.abs(audio)), 1.0)

    def test_render_to_file(self):
        if not os.path.exists(self.midi_path):
            self.skipTest("Midi file not found in current directory")
        self.engine.render_to_file(self.midi_path, self.output_wav, ["piano", "synth"])
        self.assertTrue(os.path.exists(self.output_wav))
        self.assertGreater(os.path.getsize(self.output_wav), 1000)

if __name__ == "__main__":
    unittest.main()
