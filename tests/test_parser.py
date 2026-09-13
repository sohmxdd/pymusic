import unittest
import os
from pymusic.parser import MidiTrackParser
from pymusic.models import MidiNote, TrackEvents

class TestMidiTrackParser(unittest.TestCase):
    def setUp(self):
        self.midi_path = "Kanye West - Stronger.mid"

    def test_parser_loads_file_and_ticks(self):
        if not os.path.exists(self.midi_path):
            self.skipTest("Midi file not found in current directory")
        parser = MidiTrackParser(self.midi_path)
        self.assertGreater(parser.ticks_per_beat, 0)
        total_ticks = parser.get_total_ticks()
        self.assertGreater(total_ticks, 0)

    def test_parse_all_tracks_structure(self):
        if not os.path.exists(self.midi_path):
            self.skipTest("Midi file not found in current directory")
        parser = MidiTrackParser(self.midi_path)
        tracks = parser.parse_all_tracks(["piano", "synth"])
        self.assertIsInstance(tracks, list)
        self.assertGreater(len(tracks), 0)
        for t in tracks:
            self.assertIsInstance(t, TrackEvents)
            for n in t.notes:
                self.assertIsInstance(n, MidiNote)
                self.assertGreaterEqual(n.start_tick, 0)
                self.assertGreaterEqual(n.duration_tick, 0)
                self.assertTrue(0 <= n.midi_note <= 127)
                self.assertTrue(0 <= n.velocity <= 127)

if __name__ == "__main__":
    unittest.main()
