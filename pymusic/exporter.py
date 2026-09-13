import soundfile as sf
import numpy as np

class AudioExporter:
    @staticmethod
    def export_wav(file_path: str, audio: np.ndarray, sample_rate: int, subtype: str = "FLOAT") -> None:
        sf.write(file_path, audio, sample_rate, subtype=subtype)

    @staticmethod
    def to_pcm16(audio: np.ndarray) -> np.ndarray:
        clipped = np.clip(audio, -1.0, 1.0)
        return (clipped * 32767.0).astype(np.int16)

    @staticmethod
    def get_duration_seconds(audio: np.ndarray, sample_rate: int) -> float:
        return len(audio) / float(sample_rate)
