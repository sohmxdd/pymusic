class FrequencyTuner:
    def __init__(self, reference_pitch: float = 440.0, reference_note: int = 69):
        self.reference_pitch = reference_pitch
        self.reference_note = reference_note
        self._cache: dict[int, float] = {}

    def midi_to_frequency(self, midi_note: int) -> float:
        if midi_note not in self._cache:
            self._cache[midi_note] = self.reference_pitch * (2.0 ** ((midi_note - self.reference_note) / 12.0))
        return self._cache[midi_note]

    def frequency_to_midi(self, frequency: float) -> float:
        import math
        return self.reference_note + 12.0 * math.log2(frequency / self.reference_pitch)
