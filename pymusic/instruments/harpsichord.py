import numpy as np
from .base import Instrument
from ..envelopes import ExponentialDecayEnvelope

class Harpsichord(Instrument):
    def __init__(self, decay: float = 6.0):
        super().__init__(name="harpsichord", envelope=ExponentialDecayEnvelope(decay=decay))

    def synthesize_timbre(self, frequency: float, t: np.ndarray) -> np.ndarray:
        return (
            np.sin(2.0 * np.pi * frequency * t)
            + 0.35 * np.sin(4.0 * np.pi * frequency * t)
            + 0.15 * np.sin(8.0 * np.pi * frequency * t)
        )
