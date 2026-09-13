from dataclasses import dataclass

@dataclass(frozen=True)
class MidiNote:
    start_tick: int
    duration_tick: int
    midi_note: int
    velocity: int

    @property
    def end_tick(self) -> int:
        return self.start_tick + self.duration_tick

@dataclass
class TrackEvents:
    track_index: int
    name: str
    instrument_name: str
    notes: list[MidiNote]
