import numpy as np
from .base import Instrument
from ..envelopes import ExponentialDecayEnvelope

class Synth(Instrument):
    def __init__(self, decay: float = 2.0, saw_mix: float = 0.65):
        super().__init__(name="synth", envelope=ExponentialDecayEnvelope(decay=decay))
        self.saw_mix = saw_mix

    def synthesize_timbre(self, frequency: float, t: np.ndarray) -> np.ndarray:
        saw = 2.0 * ((frequency * t) % 1.0) - 1.0
        sine = np.sin(2.0 * np.pi * frequency * t)
        return self.saw_mix * saw + (1.0 - self.saw_mix) * sine
