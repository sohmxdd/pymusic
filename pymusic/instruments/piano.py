import numpy as np
from .base import Instrument
from ..envelopes import ExponentialDecayEnvelope

class Piano(Instrument):
    def __init__(self, decay: float = 2.5):
        super().__init__(name="piano", envelope=ExponentialDecayEnvelope(decay=decay))

    def synthesize_timbre(self, frequency: float, t: np.ndarray) -> np.ndarray:
        return (
            np.sin(2.0 * np.pi * frequency * t)
            + 0.50 * np.sin(4.0 * np.pi * frequency * t)
            + 0.25 * np.sin(6.0 * np.pi * frequency * t)
        )
