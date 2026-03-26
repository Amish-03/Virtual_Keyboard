# Modern Desktop Piano

A beautifully designed virtual piano application written in Python using PyQt5 and pygame.midi. Allows you to play the piano using your computer keyboard or mouse with low-latency MIDI synthesis.

## Features
- **Visual Piano Keyboard**: 3 octaves displaying both white and black keys.
- **Polyphony**: Play multiple notes at once.
- **MIDI Synthesis**: High quality output using your system's default MIDI synth (e.g., Windows GS Wavetable).
- **Control Panel**:
  - **Transpose**: Shift the pitch up or down by up to 12 semitones.
  - **Octave Switch**: Shift the base octave up or down.
  - **Volume**: Adjust the playback velocity.
  - **Sustain**: Hold notes after keys are released.
- **Visual Feedback**: Keys highlight when pressed, and currently playing notes are displayed.

## Requirements
- Python 3
- PyQt5
- pygame

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## Controls
Use the lower two rows for the first octave (`Z` to `M` for white keys, `S`, `D`, `G`, `H`, `J` for black keys).
Use the upper two rows for the second octave (`Q` to `I` for white keys, `2`, `3`, `5`, `6`, `7` for black keys).
