from dataclasses import dataclass

@dataclass
class AudioConfig:
    sample_rate: int = 44100
    bpm: float = 104.0
    master_gain: float = 0.15
    peak_ceiling: float = 0.92

    @property
    def beat_duration(self) -> float:
        return 60.0 / self.bpm
