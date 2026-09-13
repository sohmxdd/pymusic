from pymusic.config import AudioConfig
from pymusic.engine import SynthEngine

def main():
    config = AudioConfig(sample_rate=44100, bpm=104.0, master_gain=0.15, peak_ceiling=0.92)
    engine = SynthEngine(config=config)
    instrument_map = ["piano", "harpsichord", "piano", "synth", "drums", "guitar", "saw"]
    engine.render_to_file(
        midi_path="Kanye West - Stronger.mid",
        output_path="stronger_code.wav",
        instrument_map=instrument_map
    )

if __name__ == "__main__":
    main()
