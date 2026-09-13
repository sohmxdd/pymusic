from .base import Instrument
from .piano import Piano
from .harpsichord import Harpsichord
from .synth import Synth
from .guitar import Guitar
from .saw import Saw
from .drums import NoiseDrum
from .square import SquareWave
from .registry import InstrumentRegistry

__all__ = [
    "Instrument",
    "Piano",
    "Harpsichord",
    "Synth",
    "Guitar",
    "Saw",
    "NoiseDrum",
    "SquareWave",
    "InstrumentRegistry",
]
