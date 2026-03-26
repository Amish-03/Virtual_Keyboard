# config.py - Constants and Keyboard Mappings

WINDOW_TITLE = "Modern Desktop Piano"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400

MIDI_PROGRAM_PIANO = 0
DEFAULT_VELOCITY = 127

INSTRUMENTS = {
    "Piano": 0,
    "Synth": 81,      # Sawtooth lead
    "Strings": 48,    # String Ensemble 1
    "Accordion": 21,
    "Guitar": 27,     # Electric Guitar (clean)
    "Pads": 89        # Pad 2 (warm)
}

# Base note for the piano start (48 = C3)
START_NOTE = 48

COLOR_BG = "#1e1e2e"
COLOR_PANEL = "#313244"
COLOR_TEXT = "#cdd6f4"
COLOR_WHITE_KEY = "#f5e0dc"
COLOR_BLACK_KEY = "#11111b"
COLOR_WHITE_KEY_PRESSED = "#89b4fa"
COLOR_BLACK_KEY_PRESSED = "#cba6f7"
COLOR_OUTLINE = "#45475a"

# Note mapping: offsets from the base C note
# Lower octave maps to keys Z, X, C...
LOWER_OCTAVE = {
    'Z': 0, 'S': 1, 'X': 2, 'D': 3, 'C': 4, 'V': 5, 'G': 6, 'B': 7,
    'H': 8, 'N': 9, 'J': 10, 'M': 11, ',': 12, 'L': 13, '.': 14, ';': 15, '/': 16
}

# Upper octave maps to Q, W, E...
UPPER_OCTAVE = {
    'Q': 12, '2': 13, 'W': 14, '3': 15, 'E': 16, 'R': 17, '5': 18, 'T': 19,
    '6': 20, 'Y': 21, '7': 22, 'U': 23, 'I': 24, '9': 25, 'O': 26, '0': 27,
    'P': 28, '[': 29, '=': 30, ']': 31, '\\': 32
}

KEYBOARD_MAPPED_NOTES = {**LOWER_OCTAVE, **UPPER_OCTAVE}

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def is_black_key(offset):
    # Determine if a note offset corresponds to a black key
    return (offset % 12) in {1, 3, 6, 8, 10}

def get_note_name(midi_note):
    name = NOTE_NAMES[midi_note % 12]
    octave = (midi_note // 12) - 1
    return f"{name}{octave}"
