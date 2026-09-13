# pymusic

> converting midi into raw audio using pure math, numpy, and zero soundfonts.

<!-- banner / cover image placeholder -->
<!-- <p align="center"><img src="assets/banner.png" alt="pymusic banner" width="100%" /></p> -->

a minimal python sound synthesizer that renders multi-track midi sequences directly into `.wav` audio. no daws, no samples, no external soundfonts—just additive synthesis, harmonic overtone series, exponential decay envelopes, and soft analog-style saturation.

---

<!-- visualizer / waveform preview placeholder -->
<!-- <p align="center"><img src="assets/waveform.png" alt="waveform preview" width="100%" /></p> -->

## overview

pymusic treats audio synthesis as a pure numerical problem. given a standard midi file, it traverses every track, computes frequencies using the 12-tone equal temperament scale, generates timbre through harmonic summation, and mixes every voice into a unified master buffer.

### how it works

1. **midi event extraction**  
   parses ticks and delta times from track messages using `mido`, tracking active note durations and dynamic velocities.

2. **additive harmonic synthesis**  
   each instrument profile shapes timbre by stacking fundamental frequencies and harmonic overtones:
   - `piano`: fundamental + second harmonic (0.5) + third harmonic (0.25)
   - `harpsichord`: high-register presence with 4th and 8th harmonic emphasis
   - `synth`: dual-oscillator blend (65% sawtooth wave + 35% pure sine)
   - `guitar`: acoustic warmth via second harmonic coupling
   - `saw`: raw bipolar sawtooth oscillator

3. **envelope shaping**  
   notes decay exponentially over time via `np.exp(-decay * t)` to simulate physical acoustic dampening.

4. **analog warmth & master bus**  
   individual note buffers sum directly into an array sampled at 44.1 khz. the master bus runs through hyperbolic tangent (`np.tanh`) soft clipping for gentle compression, followed by peak normalization to -0.7 dB.

---

## architecture

```
MIDI Input (.mid)
       │
       ▼
Track Event Parser (mido)
       │
       ├── Piano Engine       (fundamental + 2nd/3rd harmonics)
       ├── Synth Engine       (sawtooth + sine oscillator blend)
       ├── Harpsichord Engine (fast transient + high harmonics)
       └── Guitar & Saw       (harmonic overtone shaping)
       │
       ▼
Exponential Decay Envelopes & Velocity Scaling
       │
       ▼
Global Master Buffer (44.1 kHz)
       │
       ▼
Hyperbolic Tangent (tanh) Soft Saturation & Peak Limiting
       │
       ▼
Master Output (.wav)
```

---

<!-- studio / workflow / demo image placeholder -->
<!-- <p align="center"><img src="assets/preview.png" alt="studio preview" width="100%" /></p> -->

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

place your target midi file in the root directory (currently set to `Kanye West - Stronger.mid`) and run:

```bash
python main.py
```

the rendered track will be exported as `stronger_code.wav` at 44.1 khz.

---

## configuration

all sound design parameters can be tuned directly in `main.py`:

- **sample rate & tempo**: adjust `SR` (default `44100`) and `BPM` (default `104`).
- **instrument routing**: map MIDI tracks to voice engines via the `instruments` array.
- **decay rates**: tweak the `envelope(length, decay)` factor to control sustain versus percussive pluck.
- **saturation drive**: adjust the pre-saturation gain multiplier before `np.tanh` to vary the warmth from clean to fuzzy overdrive.

---

## stack

- **numpy** - vector calculations, harmonic generation, signal arrays
- **soundfile** - high-fidelity wav encoding
- **mido** - midi event handling and delta-time parsing
