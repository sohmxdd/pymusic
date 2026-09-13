import mido
from .models import MidiNote, TrackEvents

class MidiTrackParser:
    def __init__(self, midi_path: str):
        self.midi_path = midi_path
        self.midi_file = mido.MidiFile(midi_path)
        self.ticks_per_beat = self.midi_file.ticks_per_beat

    def extract_notes_from_track(self, track: mido.MidiTrack) -> list[MidiNote]:
        absolute_tick = 0
        active: dict[int, tuple[int, int]] = {}
        notes: list[MidiNote] = []

        for message in track:
            absolute_tick += message.time
            if message.type == "note_on" and message.velocity > 0:
                active[message.note] = (absolute_tick, message.velocity)
            elif message.type == "note_off" or (message.type == "note_on" and message.velocity == 0):
                if message.note in active:
                    start_tick, velocity = active.pop(message.note)
                    duration_tick = absolute_tick - start_tick
                    notes.append(MidiNote(start_tick, duration_tick, message.note, velocity))

        return notes

    def parse_all_tracks(self, default_instrument_map: list[str] | None = None) -> list[TrackEvents]:
        tracks_data: list[TrackEvents] = []
        instruments = default_instrument_map or ["piano"]

        for index, track in enumerate(self.midi_file.tracks):
            track_name = getattr(track, "name", f"track_{index}")
            inst = instruments[min(index, len(instruments) - 1)]
            notes = self.extract_notes_from_track(track)
            tracks_data.append(TrackEvents(track_index=index, name=track_name, instrument_name=inst, notes=notes))

        return tracks_data

    def get_total_ticks(self) -> int:
        total = 0
        for track in self.midi_file.tracks:
            ticks = sum(message.time for message in track)
            total = max(total, ticks)
        return total
