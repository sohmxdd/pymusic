import numpy as np
from .config import AudioConfig

class MasterBus:
    def __init__(self, config: AudioConfig, duration_seconds: float):
        self.config = config
        total_samples = int(duration_seconds * config.sample_rate) + config.sample_rate
        self.buffer = np.zeros(max(config.sample_rate, total_samples), dtype=np.float64)

    def mix_sample(self, sound: np.ndarray, start_sample: int) -> None:
        if len(sound) == 0 or start_sample >= len(self.buffer):
            return
        end_sample = min(start_sample + len(sound), len(self.buffer))
        self.buffer[start_sample:end_sample] += sound[:end_sample - start_sample]

    def apply_saturation(self, gain: float | None = None) -> None:
        master_gain = gain if gain is not None else self.config.master_gain
        self.buffer *= master_gain
        self.buffer = np.tanh(self.buffer)

    def apply_peak_normalization(self, ceiling: float | None = None) -> None:
        peak_ceiling = ceiling if ceiling is not None else self.config.peak_ceiling
        peak = np.max(np.abs(self.buffer))
        if peak > 0.0:
            self.buffer = (self.buffer / peak) * peak_ceiling

    def finalize(self) -> np.ndarray:
        self.apply_saturation()
        self.apply_peak_normalization()
        return self.buffer

    def clear(self) -> None:
        self.buffer.fill(0.0)

    @property
    def raw_audio(self) -> np.ndarray:
        return self.buffer
