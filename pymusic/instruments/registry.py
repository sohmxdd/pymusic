from .base import Instrument
from .piano import Piano
from .harpsichord import Harpsichord
from .synth import Synth
from .guitar import Guitar
from .saw import Saw
from .drums import NoiseDrum
from .square import SquareWave

class InstrumentRegistry:
    def __init__(self):
        self._registry: dict[str, type[Instrument]] = {}
        self.register_defaults()

    def register_defaults(self) -> None:
        self._registry["piano"] = Piano
        self._registry["harpsichord"] = Harpsichord
        self._registry["synth"] = Synth
        self._registry["guitar"] = Guitar
        self._registry["saw"] = Saw
        self._registry["drums"] = NoiseDrum
        self._registry["square"] = SquareWave

    def register(self, name: str, instrument_cls: type[Instrument]) -> None:
        self._registry[name.lower()] = instrument_cls

    def get(self, name: str, **kwargs) -> Instrument:
        cls = self._registry.get(name.lower(), Piano)
        return cls(**kwargs)

    def available(self) -> list[str]:
        return list(self._registry.keys())
