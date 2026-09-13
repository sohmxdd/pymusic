import unittest
import numpy as np
from pymusic.config import AudioConfig
from pymusic.mixer import MasterBus

class TestMasterBus(unittest.TestCase):
    def setUp(self):
        self.config = AudioConfig(sample_rate=44100, master_gain=0.15, peak_ceiling=0.92)
        self.mixer = MasterBus(self.config, duration_seconds=1.0)

    def test_mix_sample_accumulation(self):
        sample = np.ones(100, dtype=np.float64) * 0.5
        self.mixer.mix_sample(sample, start_sample=10)
        self.mixer.mix_sample(sample, start_sample=10)
        self.assertAlmostEqual(self.mixer.raw_audio[10], 1.0, places=4)
        self.assertAlmostEqual(self.mixer.raw_audio[109], 1.0, places=4)
        self.assertAlmostEqual(self.mixer.raw_audio[0], 0.0, places=4)

    def test_saturation_and_normalization(self):
        hot_signal = np.ones(1000, dtype=np.float64) * 10.0
        self.mixer.mix_sample(hot_signal, start_sample=0)
        final = self.mixer.finalize()
        self.assertLessEqual(np.max(np.abs(final)), self.config.peak_ceiling + 1e-4)
        self.assertTrue(np.all(np.isfinite(final)))

    def test_clear_buffer(self):
        sample = np.ones(50, dtype=np.float64)
        self.mixer.mix_sample(sample, start_sample=0)
        self.mixer.clear()
        self.assertTrue(np.all(self.mixer.raw_audio == 0.0))

if __name__ == "__main__":
    unittest.main()
