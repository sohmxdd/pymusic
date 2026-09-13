from abc import ABC, abstractmethod
import numpy as np
from ..envelopes import Envelope, ExponentialDecayEnvelope

class Instrument(ABC):
    def __init__(self, name: str, envelope: Envelope | None = None):
        self.name = name
        self.envelope = envelope or ExponentialDecayEnvelope(decay=4.0)

    @abstractmethod
    def synthesize_timbre(self, frequency: float, t: np.ndarray) -> np.ndarray:
        pass

    def render_note(self, frequency: float, duration: float, velocity: int, sample_rate: int) -> np.ndarray:
        length = int(duration * sample_rate)
        if length <= 0:
            return np.zeros(0)
        t = np.arange(length) / sample_rate
        raw_wave = self.synthesize_timbre(frequency, t)
        env = self.envelope.generate(length, sample_rate)
        velocity_gain = max(0.0, min(1.0, velocity / 127.0))
        return raw_wave * env * velocity_gain
