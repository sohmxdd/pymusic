import numpy as np
from .base import Instrument
from ..envelopes import ExponentialDecayEnvelope

class SquareWave(Instrument):
    def __init__(self, decay: float = 3.5, duty: float = 0.5):
        super().__init__(name="square", envelope=ExponentialDecayEnvelope(decay=decay))
        self.duty = duty

    def synthesize_timbre(self, frequency: float, t: np.ndarray) -> np.ndarray:
        phase = (frequency * t) % 1.0
        return np.where(phase < self.duty, 1.0, -1.0)
