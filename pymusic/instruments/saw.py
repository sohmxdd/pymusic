import numpy as np
from .base import Instrument
from ..envelopes import ExponentialDecayEnvelope

class Saw(Instrument):
    def __init__(self, decay: float = 3.0):
        super().__init__(name="saw", envelope=ExponentialDecayEnvelope(decay=decay))

    def synthesize_timbre(self, frequency: float, t: np.ndarray) -> np.ndarray:
        return 2.0 * ((frequency * t) % 1.0) - 1.0
