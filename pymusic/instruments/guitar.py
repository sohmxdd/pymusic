import numpy as np
from .base import Instrument
from ..envelopes import ExponentialDecayEnvelope

class Guitar(Instrument):
    def __init__(self, decay: float = 5.0):
        super().__init__(name="guitar", envelope=ExponentialDecayEnvelope(decay=decay))

    def synthesize_timbre(self, frequency: float, t: np.ndarray) -> np.ndarray:
        return (
            np.sin(2.0 * np.pi * frequency * t)
            + 0.30 * np.sin(4.0 * np.pi * frequency * t)
        )
