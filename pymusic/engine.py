import soundfile as sf
import numpy as np
from .config import AudioConfig
from .tuning import FrequencyTuner
from .instruments.registry import InstrumentRegistry
from .parser import MidiTrackParser
from .mixer import MasterBus

class SynthEngine:
    def __init__(self, config: AudioConfig | None = None, registry: InstrumentRegistry | None = None, tuner: FrequencyTuner | None = None):
        self.config = config or AudioConfig()
        self.registry = registry or InstrumentRegistry()
        self.tuner = tuner or FrequencyTuner()

    def render_midi(self, midi_path: str, instrument_map: list[str] | None = None) -> np.ndarray:
        parser = MidiTrackParser(midi_path)
        total_ticks = parser.get_total_ticks()
        total_beats = total_ticks / parser.ticks_per_beat
        total_seconds = total_beats * self.config.beat_duration

        master_bus = MasterBus(self.config, total_seconds)
        tracks_data = parser.parse_all_tracks(instrument_map)

        for track_events in tracks_data:
            instrument = self.registry.get(track_events.instrument_name)
            for note in track_events.notes:
                start_seconds = (note.start_tick / parser.ticks_per_beat) * self.config.beat_duration
                duration_seconds = (note.duration_tick / parser.ticks_per_beat) * self.config.beat_duration
                freq = self.tuner.midi_to_frequency(note.midi_note)
                sound = instrument.render_note(freq, duration_seconds, note.velocity, self.config.sample_rate)
                start_sample = int(start_seconds * self.config.sample_rate)
                master_bus.mix_sample(sound, start_sample)

        return master_bus.finalize()

    def render_to_file(self, midi_path: str, output_path: str, instrument_map: list[str] | None = None) -> None:
        audio = self.render_midi(midi_path, instrument_map)
        sf.write(output_path, audio, self.config.sample_rate)
