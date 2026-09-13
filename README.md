# pymusic

> converting midi into raw audio using pure math, numpy, and zero soundfonts.

<p align="left">
  <img src="https://img.shields.io/badge/python-3.10+-000000?style=flat-square&logo=python&logoColor=white" alt="python" />
  <img src="https://img.shields.io/badge/dsp-additive%20synthesis-000000?style=flat-square" alt="dsp" />
  <img src="https://img.shields.io/badge/architecture-modular%20OOP-000000?style=flat-square" alt="oop" />
  <img src="https://img.shields.io/badge/sample%20rate-44.1%20kHz-000000?style=flat-square" alt="sample rate" />
  <img src="https://img.shields.io/badge/precision-64--bit%20float-000000?style=flat-square" alt="precision" />
  <img src="https://img.shields.io/badge/tests-14%20passed-000000?style=flat-square" alt="tests" />
  <img src="https://img.shields.io/badge/license-MIT-000000?style=flat-square" alt="license" />
</p>

<p align="center">
  <img src="assets/banner.svg" alt="pymusic banner" width="100%" />
</p>

a modular, high-performance object-oriented python synthesizer that renders multi-track midi sequences directly into `.wav` audio. no daws, no samples, no external soundfonts—pure additive synthesis, harmonic overtone stacking, polymorphic instrument classes, and analog-style soft saturation.

---

## architecture & oop class hierarchy

<p align="center">
  <img src="assets/signal-flow.svg" alt="signal flow architecture" width="100%" />
</p>

```
┌────────────────────────────────────────────────────────────────────────┐
│                              SynthEngine                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────────────┐ │
│  │   AudioConfig    │  │  FrequencyTuner  │  │  InstrumentRegistry   │ │
│  └────────┬─────────┘  └────────┬─────────┘  └───────────┬───────────┘ │
└───────────┼─────────────────────┼────────────────────────┼─────────────┘
            │                     │                        │
            ▼                     ▼                        ▼
┌───────────────────────┐ ┌────────────────┐ ┌───────────────────────────┐
│    MidiTrackParser    │ │   MidiNote     │ │     Instrument (ABC)      │
│  • track event stream │ │  • start_tick  │ │  ├── Piano                │
│  • delta tick to sec  │ │  • duration    │ │  ├── Harpsichord          │
│  • velocity scaling   │ │  • midi_note   │ │  ├── Synth (Saw + Sine)   │
└───────────┬───────────┘ └────────────────┘ │  ├── Guitar               │
            │                                │  ├── Saw (Bipolar)        │
            ▼                                │  ├── NoiseDrum (Noise+Sub)│
┌──────────────────────────────────────────┐ │  └── SquareWave (Chiptune)│
│                MasterBus                 │ └───────────────────────────┘
│  • vectorized sample accumulation buffer │
│  • tanh soft-saturation waveshaping      │
│  • peak normalization (-0.7 dBFS margin) │
└───────────────────┬──────────────────────┘
                    ▼
┌──────────────────────────────────────────┐
│              AudioExporter               │
│  • float64 / PCM16 / WAV export via sf   │
└──────────────────────────────────────────┘
```

---

## voice matrix

| Voice | Class | Oscillator Formula | Harmonics & Weights | Decay ($\lambda$) | Character |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `piano` | `Piano` | Additive Sinusoid | $f_0 (1.0) + 2f_0 (0.5) + 3f_0 (0.25)$ | $2.5$ | warm acoustic tone, rich body, gentle release |
| `harpsichord` | `Harpsichord` | Additive Sinusoid | $f_0 (1.0) + 2f_0 (0.35) + 4f_0 (0.15)$ | $6.0$ | sharp transient attack, metallic register |
| `synth` | `Synth` | Hybrid Blend | $\text{saw}(t) \ (0.65) + \sin(2\pi ft) \ (0.35)$ | $2.0$ | cutting mid-range lead, modern electronic density |
| `guitar` | `Guitar` | Additive Sinusoid | $f_0 (1.0) + 2f_0 (0.3)$ | $5.0$ | resonant string strike, hollow fundamental |
| `saw` | `Saw` | Linear Sawtooth | $2(ft \bmod 1) - 1$ | $3.0$ | bright, aggressive, high harmonic energy |
| `drums` | `NoiseDrum` | Noise + Sub Sine | $0.7 \cdot \text{noise} + 0.3 \sin(2\pi f_{\text{sub}} t)$ | $12.0$ | punchy percussive attack, fast exponential cutoff |
| `square` | `SquareWave` | Bipolar Pulse | $\text{sgn}(\sin(2\pi ft))$ | $3.5$ | nostalgic 8-bit chiptune character |

---

## quickstart

### prerequisites

ensure python 3.10+ is installed.

```bash
git clone https://github.com/sohmxdd/pymusic.git
cd pymusic
```

### environment setup

```bash
python -m venv .venv

# windows
.venv\Scripts\activate

# mac / linux
source .venv/bin/activate

pip install numpy soundfile mido
```

### render audio

```bash
python main.py
```

the rendered track will be exported as `stronger_code.wav` at 44.1 khz.

### running test suite

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## python api & custom instruments

you can embed `pymusic` directly into any python pipeline or register custom instruments dynamically:

```python
from pymusic.config import AudioConfig
from pymusic.engine import SynthEngine
from pymusic.instruments.base import Instrument
from pymusic.envelopes import ExponentialDecayEnvelope, ADSREnvelope
import numpy as np

class Sub808(Instrument):
    def __init__(self):
        super().__init__(name="sub_808", envelope=ExponentialDecayEnvelope(decay=1.2))

    def synthesize_timbre(self, frequency: float, t: np.ndarray) -> np.ndarray:
        return np.sin(2.0 * np.pi * frequency * t) + 0.12 * np.sin(4.0 * np.pi * frequency * t)

class AmbientPad(Instrument):
    def __init__(self):
        super().__init__(name="ambient_pad", envelope=ADSREnvelope(attack=0.4, decay=0.2, sustain=0.8, release=0.5))

    def synthesize_timbre(self, frequency: float, t: np.ndarray) -> np.ndarray:
        return (
            np.sin(2.0 * np.pi * frequency * t)
            + 0.4 * np.sin(2.0 * np.pi * (frequency * 1.005) * t)
            + 0.3 * np.sin(4.0 * np.pi * frequency * t)
        )

engine = SynthEngine(config=AudioConfig(sample_rate=44100, bpm=120.0))
engine.registry.register("sub_808", Sub808)
engine.registry.register("pad", AmbientPad)

engine.render_to_file(
    midi_path="song.mid",
    output_path="output.wav",
    instrument_map=["sub_808", "piano", "pad"]
)
```

---

## performance & vectorization

pymusic avoids per-sample python loops by offloading all audio calculations to vectorized C-level SIMD operations in NumPy:

- **pre-allocated master buffer**: the master array in `MasterBus` is allocated once upfront, maintaining contiguous cache locality throughout track summation.
- **vectorized time arrays**: time slices `t = np.arange(length) / sample_rate` evaluate trigonometric harmonic series across whole buffers simultaneously.
- **sub-second render velocity**: renders a complete 40-second 7-track multi-instrument arrangement (~1.8 million audio samples) in under `0.35 seconds` on modern hardware.

---

## repository anatomy

```
pymusic/
├── assets/
│   ├── banner.svg             # vector header banner
│   └── signal-flow.svg        # dsp architecture diagram
├── pymusic/                   # core object-oriented library
│   ├── __init__.py            # package exports
│   ├── config.py              # AudioConfig dataclass
│   ├── tuning.py              # FrequencyTuner (12-TET)
│   ├── envelopes.py           # ExponentialDecay & ADSR envelopes
│   ├── models.py              # MidiNote & TrackEvents models
│   ├── parser.py              # MidiTrackParser
│   ├── mixer.py               # MasterBus & SoftSaturation DSP
│   ├── engine.py              # SynthEngine orchestrator
│   ├── exporter.py            # AudioExporter
│   └── instruments/           # polymorphic instrument hierarchy
│       ├── __init__.py
│       ├── base.py            # Instrument abstract base
│       ├── piano.py
│       ├── harpsichord.py
│       ├── synth.py
│       ├── guitar.py
│       ├── saw.py
│       ├── drums.py
│       ├── square.py
│       └── registry.py        # InstrumentRegistry factory
├── tests/                     # comprehensive test suite (14 tests)
│   ├── test_tuning_envelopes.py
│   ├── test_instruments.py
│   ├── test_parser.py
│   ├── test_mixer.py
│   └── test_integration.py
├── Kanye West - Stronger.mid  # demo multi-track midi arrangement (7 tracks)
├── main.py                    # clean application entrypoint
├── stronger_code.wav          # rendered 44.1 khz 16-bit master export
├── .gitignore                 # python environment and cache filters
└── README.md                  # architectural documentation
```

---

## technical specifications

| Parameter | Specification | Note |
| :--- | :--- | :--- |
| **Sample Rate** | `44,100 Hz` (CD standard) | Configurable via `AudioConfig.sample_rate` |
| **Internal Bit Depth** | `64-bit IEEE Floating Point` | High-precision NumPy array accumulation |
| **Export Format** | `16-bit PCM Linear WAV` | Encoded with `libsndfile` via `soundfile` |
| **Peak Ceiling** | `-0.7 dBFS` ($0.92$ normalized) | True-peak clipping safety margin |
| **Tuning Reference** | $A_4 = 440.0\text{ Hz}$ | Configurable via `FrequencyTuner` |
| **Polyphony** | Unlimited | Vector superposition in memory |
| **Synthesis Type** | Polymorphic Additive Harmonic & DSP Saturation | Zero external sample libraries or soundfonts |

---

## license

mit license. crafted with pure math, numpy, and clean object-oriented architecture.
