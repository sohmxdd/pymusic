import numpy as np
from .base import Instrument
from ..envelopes import ExponentialDecayEnvelope

class NoiseDrum(Instrument):
    def __init__(self, decay: float = 12.0):
        super().__init__(name="drums", envelope=ExponentialDecayEnvelope(decay=decay))

    def synthesize_timbre(self, frequency: float, t: np.ndarray) -> np.ndarray:
        noise = np.random.uniform(-1.0, 1.0, len(t))
        body = np.sin(2.0 * np.pi * max(40.0, frequency * 0.25) * t)
        return 0.7 * noise + 0.3 * body
