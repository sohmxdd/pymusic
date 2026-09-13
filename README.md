# pymusic

> converting midi into raw audio using pure math, numpy, and zero soundfonts.

<p align="left">
  <img src="https://img.shields.io/badge/python-3.10+-000000?style=flat-square&logo=python&logoColor=white" alt="python" />
  <img src="https://img.shields.io/badge/dsp-additive%20synthesis-000000?style=flat-square" alt="dsp" />
  <img src="https://img.shields.io/badge/sample%20rate-44.1%20kHz-000000?style=flat-square" alt="sample rate" />
  <img src="https://img.shields.io/badge/precision-64--bit%20float-000000?style=flat-square" alt="precision" />
  <img src="https://img.shields.io/badge/soundfonts-0%25-000000?style=flat-square" alt="soundfonts" />
  <img src="https://img.shields.io/badge/license-MIT-000000?style=flat-square" alt="license" />
</p>

<p align="center">
  <img src="assets/banner.svg" alt="pymusic banner" width="100%" />
</p>

<!-- custom image / cover placeholder -->
<!-- <p align="center"><img src="assets/cover.png" alt="custom cover" width="100%" /></p> -->

a minimal python sound synthesizer that renders multi-track midi sequences directly into `.wav` audio. no daws, no samples, no external soundfonts—just additive synthesis, harmonic overtone series, exponential decay envelopes, and soft analog-style saturation.

---

<!-- visualizer / waveform preview placeholder -->
<!-- <p align="center"><img src="assets/waveform.png" alt="waveform preview" width="100%" /></p> -->

## overview

pymusic treats audio synthesis as a pure numerical problem. given a standard midi file, it traverses every track, computes frequencies using the 12-tone equal temperament scale, generates timbre through harmonic summation, and mixes every voice into a unified master buffer.

### how it works

1. **midi event extraction & frequency tuning**  
   parses delta ticks from track messages using `mido`, tracking active note durations and velocities. notes are mapped to continuous acoustic frequencies using standard 12-tone equal temperament ($A_4 = 440\text{ Hz}$):

   $$f(n) = 440 \cdot 2^{\frac{n - 69}{12}}$$

2. **additive harmonic synthesis**  
   each instrument profile shapes timbre by stacking fundamental frequencies and harmonic overtones:
   - `piano`: warm acoustic body driven by fundamental, 2nd, and 3rd harmonics:
     $$s_{\text{piano}}(t) = \sin(2\pi ft) + 0.5\sin(4\pi ft) + 0.25\sin(6\pi ft)$$
   - `harpsichord`: metallic plucked timbre rich in high-order octave harmonics:
     $$s_{\text{harpsichord}}(t) = \sin(2\pi ft) + 0.35\sin(4\pi ft) + 0.15\sin(8\pi ft)$$
   - `synth`: dual-oscillator hybrid blending sawtooth buzz and sine roundness:
     $$\text{saw}(t) = 2(ft \bmod 1) - 1, \quad s_{\text{synth}}(t) = 0.65 \cdot \text{saw}(t) + 0.35 \sin(2\pi ft)$$
   - `guitar`: string pluck resonance with second-harmonic coupling:
     $$s_{\text{guitar}}(t) = \sin(2\pi ft) + 0.3\sin(4\pi ft)$$
   - `saw`: raw bipolar linear sawtooth oscillator:
     $$s_{\text{saw}}(t) = 2(ft \bmod 1) - 1$$

3. **envelope shaping & energy dissipation**  
   notes decay exponentially over time to emulate acoustic string dampening and percussive amplitude decay:

   $$E(t) = e^{-\lambda t}$$

   where $\lambda$ specifies the decay coefficient ($\lambda = 2.5$ for piano sustain, $\lambda = 6.0$ for rapid harpsichord plucking). the finished note waveform scales with MIDI velocity:

   $$w_{\text{note}}(t) = s(t) \cdot E(t) \cdot \left(\frac{v}{127}\right)$$

4. **analog warmth & master bus**  
   all active note waveforms sum into a global 64-bit floating-point master buffer sampled at 44.1 kHz. to eliminate digital hard clipping and impart tape-like harmonic warmth, the master signal passes through a hyperbolic tangent waveshaper with gain scaling:

   $$y(t) = \tanh\left(0.15 \cdot x_{\text{sum}}(t)\right)$$

   the saturated audio is then peak-normalized to maintain a true-peak ceiling of -0.7 dBFS ($0.92$ amplitude):

   $$y_{\text{out}}(t) = 0.92 \cdot \frac{y(t)}{\max |y|}$$

---

## architecture

<p align="center">
  <img src="assets/signal-flow.svg" alt="signal flow architecture" width="100%" />
</p>

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

## voice matrix

| Voice | Oscillator Type | Harmonics & Weights | Decay ($\lambda$) | Character |
| :--- | :--- | :--- | :--- | :--- |
| `piano` | Additive Sinusoid | $f_0 (1.0) + 2f_0 (0.5) + 3f_0 (0.25)$ | $2.5$ | warm acoustic tone, rich body, gentle release |
| `harpsichord` | Additive Sinusoid | $f_0 (1.0) + 2f_0 (0.35) + 4f_0 (0.15)$ | $6.0$ | sharp transient attack, metallic register |
| `synth` | Hybrid Blend | $\text{saw}(t) \ (0.65) + \sin(2\pi ft) \ (0.35)$ | $2.0$ | cutting mid-range lead, modern electronic density |
| `guitar` | Additive Sinusoid | $f_0 (1.0) + 2f_0 (0.3)$ | $5.0$ | resonant string strike, hollow fundamental |
| `saw` | Linear Sawtooth | $2(ft \bmod 1) - 1$ | $3.0$ | bright, aggressive, high harmonic energy |

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

### track mapping

the demo project parses 7 polyphonic tracks from `Kanye West - Stronger.mid`:

| Track # | Assigned Voice | Role in Mix |
| :--- | :--- | :--- |
| `Track 0` | `piano` | primary harmonic progression & foundational chords |
| `Track 1` | `harpsichord` | rhythmic syncopated counterpoint & upper register sparkle |
| `Track 2` | `piano` | mid-register harmonic reinforcement |
| `Track 3` | `synth` | main aggressive electronic hook lead |
| `Track 4` | `drums` | percussive rhythm channel |
| `Track 5` | `guitar` | dynamic melodic fills and accents |
| `Track 6` | `saw` | raw sub-saw bassline and low-end drive |

### sound design cookbook

adding new instrument voices is straightforward. implement an oscillator formula and envelope decay in `generate_note`:

```python
# 808 sub-bass (fundamental dominance with subtle second harmonic)
elif instrument == "sub_808":
    wave = np.sin(2 * np.pi * frequency * t) + 0.12 * np.sin(4 * np.pi * frequency * t)
    wave *= envelope(length, decay=1.2)

# church organ (odd-harmonic additive stack with slow decay)
elif instrument == "organ":
    wave = (
        np.sin(2 * np.pi * frequency * t)
        + 0.60 * np.sin(6 * np.pi * frequency * t)
        + 0.35 * np.sin(10 * np.pi * frequency * t)
    )
    wave *= envelope(length, decay=0.8)
```

---

## technical specifications

| Parameter | Specification | Note |
| :--- | :--- | :--- |
| **Sample Rate** | `44,100 Hz` (CD standard) | Configurable via `SR` |
| **Internal Bit Depth** | `64-bit IEEE Floating Point` | High-precision NumPy array accumulation |
| **Export Format** | `16-bit PCM Linear WAV` | Encoded with `libsndfile` via `soundfile` |
| **Peak Ceiling** | `-0.7 dBFS` ($0.92$ normalized) | True-peak clipping safety margin |
| **Tuning Reference** | $A_4 = 440.0\text{ Hz}$ | Standard 12-TET tuning system |
| **Polyphony** | Unlimited | Vector superposition in memory |
| **Synthesis Type** | Additive Harmonic & Hybrid Waveshaping | Zero external sample libraries or soundfonts |

---

## performance & vectorization

pymusic avoids per-sample python loops by offloading all audio calculations to vectorized C-level SIMD operations in NumPy:

- **pre-allocated master buffer**: the master array `np.zeros(int(total_seconds * SR) + SR)` is allocated once upfront, maintaining contiguous cache locality throughout track summation.
- **vectorized time arrays**: time slices `t = np.arange(length) / SR` evaluate trigonometric harmonic series across whole buffers simultaneously.
- **sub-second render velocity**: renders a complete 40-second 7-track multi-instrument arrangement (~1.8 million audio samples) in under `0.35 seconds` on modern hardware.

---

## repository anatomy

```
pymusic/
├── assets/
│   ├── banner.svg             # vector header banner
│   └── signal-flow.svg        # dsp architecture diagram
├── Kanye West - Stronger.mid  # demo multi-track midi arrangement (7 tracks)
├── main.py                    # synthesis engine, harmonic stacker & master bus
├── stronger_code.wav          # rendered 44.1 khz 16-bit master export
├── .gitignore                 # python environment and cache filters
└── README.md                  # architectural documentation
```

---

## stack

- **numpy** - vector calculations, harmonic generation, signal arrays
- **soundfile** - high-fidelity wav encoding
- **mido** - midi event handling and delta-time parsing
