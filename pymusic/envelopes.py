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

class ADSREnvelope(Envelope):
    def __init__(self, attack: float = 0.01, decay: float = 0.1, sustain: float = 0.7, release: float = 0.2):
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release

    def generate(self, length: int, sample_rate: int) -> np.ndarray:
        attack_samples = int(self.attack * sample_rate)
        decay_samples = int(self.decay * sample_rate)
        release_samples = int(self.release * sample_rate)
        sustain_samples = max(0, length - attack_samples - decay_samples - release_samples)

        env_parts = []
        if attack_samples > 0:
            env_parts.append(np.linspace(0.0, 1.0, attack_samples, endpoint=False))
        if decay_samples > 0:
            env_parts.append(np.linspace(1.0, self.sustain, decay_samples, endpoint=False))
        if sustain_samples > 0:
            env_parts.append(np.full(sustain_samples, self.sustain))
        if release_samples > 0:
            env_parts.append(np.linspace(self.sustain, 0.0, release_samples, endpoint=True))

        if not env_parts:
            return np.ones(length)

        env = np.concatenate(env_parts)
        if len(env) < length:
            return np.pad(env, (0, length - len(env)), mode="constant", constant_values=0.0)
        return env[:length]
