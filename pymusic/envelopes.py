from abc import ABC, abstractmethod
import numpy as np

class Envelope(ABC):
    @abstractmethod
    def generate(self, length: int, sample_rate: int) -> np.ndarray:
        pass

class ExponentialDecayEnvelope(Envelope):
    def __init__(self, decay: float = 4.0):
        self.decay = decay

    def generate(self, length: int, sample_rate: int) -> np.ndarray:
        t = np.arange(length) / sample_rate
        return np.exp(-self.decay * t)
