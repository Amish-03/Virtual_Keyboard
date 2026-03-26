import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QSlider, QSpinBox, QCheckBox, QComboBox
)
from PyQt5.QtCore import Qt
from audio_engine import AudioEngine
from piano_widget import PianoWidget
from config import (
    KEYBOARD_MAPPED_NOTES, START_NOTE, get_note_name, INSTRUMENTS,
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_TEXT, COLOR_PANEL
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio = AudioEngine()
        self.transpose_val = 0
        self.octave_shift = 0
        
        self.pressed_keys = set()
        self.playing_notes = set()

        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(f"background-color: {COLOR_BG}; color: {COLOR_TEXT}; font-size: 20px;")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        controls_layout = QHBoxLayout()
        
        # Transpose
        controls_layout.addWidget(QLabel("Transpose:"))
        self.transpose_spinbox = QSpinBox()
        self.transpose_spinbox.setRange(-12, 12)
        self.transpose_spinbox.setValue(0)
        self.transpose_spinbox.valueChanged.connect(self.on_transpose_changed)
        self.transpose_spinbox.setStyleSheet(f"background-color: {COLOR_PANEL}; color: {COLOR_TEXT};")
        controls_layout.addWidget(self.transpose_spinbox)
        
        # Octave Shift
        controls_layout.addWidget(QLabel("Octave:"))
        self.octave_spinbox = QSpinBox()
        self.octave_spinbox.setRange(-3, 3)
        self.octave_spinbox.setValue(0)
        self.octave_spinbox.valueChanged.connect(self.on_octave_changed)
        self.octave_spinbox.setStyleSheet(f"background-color: {COLOR_PANEL}; color: {COLOR_TEXT};")
        controls_layout.addWidget(self.octave_spinbox)
        
        # Volume
        controls_layout.addWidget(QLabel("Volume:"))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        controls_layout.addWidget(self.volume_slider)
        
        # Sustain
        self.sustain_checkbox = QCheckBox("Sustain")
        self.sustain_checkbox.stateChanged.connect(self.on_sustain_changed)
        controls_layout.addWidget(self.sustain_checkbox)
        
        # Instrument
        controls_layout.addWidget(QLabel("Instrument:"))
        self.instrument_combo = QComboBox()
        self.instrument_combo.addItems(list(INSTRUMENTS.keys()))
        self.instrument_combo.currentIndexChanged.connect(self.on_instrument_changed)
        self.instrument_combo.setStyleSheet(f"background-color: {COLOR_PANEL}; color: {COLOR_TEXT};")
        controls_layout.addWidget(self.instrument_combo)
        
        # Playing Label
        self.playing_label = QLabel("Playing: None")
        controls_layout.addWidget(self.playing_label)
        
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)
        
        # Piano Widget
        self.piano_widget = PianoWidget(start_note=START_NOTE, num_keys=36) # 3 octaves
        self.piano_widget.note_pressed.connect(self.on_ui_note_pressed)
        self.piano_widget.note_released.connect(self.on_ui_note_released)
        main_layout.addWidget(self.piano_widget)
        
    def on_transpose_changed(self, val):
        self.transpose_val = val
        self.release_all()
        self.update_playing_label()
        
    def on_octave_changed(self, val):
        self.octave_shift = val
        self.release_all()
        self.update_playing_label()
        
    def on_instrument_changed(self, index):
        name = self.instrument_combo.currentText()
        program = INSTRUMENTS.get(name, 0)
        self.audio.set_instrument(program)
        self.release_all()
        self.update_playing_label()

    def on_volume_changed(self, val):
        self.audio.set_volume(val / 100.0)

    def on_sustain_changed(self, state):
        self.audio.set_sustain(state == Qt.Checked)
        
    def get_actual_note(self, offset):
        return START_NOTE + offset + self.transpose_val + (self.octave_shift * 12)
        
    def on_ui_note_pressed(self, ui_note):
        offset = ui_note - START_NOTE
        actual_note = self.get_actual_note(offset)
        self.audio.note_on(actual_note)
        self.playing_notes.add(actual_note)
        self.update_playing_label()
        
    def on_ui_note_released(self, ui_note):
        offset = ui_note - START_NOTE
        actual_note = self.get_actual_note(offset)
        self.audio.note_off(actual_note)
        if actual_note in self.playing_notes:
            self.playing_notes.remove(actual_note)
        self.update_playing_label()

    def update_playing_label(self):
        if not self.playing_notes:
            self.playing_label.setText("Playing: None")
        else:
            names = [get_note_name(n) for n in sorted(self.playing_notes)]
            self.playing_label.setText("Playing: " + ", ".join(names))

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
            
        key_char = event.text().upper()
        if not key_char:
            key_char = chr(event.key()) if 32 <= event.key() <= 126 else ""
            
        if key_char in KEYBOARD_MAPPED_NOTES and key_char not in self.pressed_keys:
            offset = KEYBOARD_MAPPED_NOTES[key_char]
            actual_note = self.get_actual_note(offset)
            ui_note = START_NOTE + offset
            
            self.audio.note_on(actual_note)
            self.playing_notes.add(actual_note)
            self.piano_widget.set_key_pressed(ui_note, True)
            self.pressed_keys.add(key_char)
            self.update_playing_label()
            
    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
            
        key_char = event.text().upper()
        if not key_char:
            key_char = chr(event.key()) if 32 <= event.key() <= 126 else ""
            
        if key_char in KEYBOARD_MAPPED_NOTES and key_char in self.pressed_keys:
            offset = KEYBOARD_MAPPED_NOTES[key_char]
            actual_note = self.get_actual_note(offset)
            ui_note = START_NOTE + offset
            
            self.audio.note_off(actual_note)
            if actual_note in self.playing_notes:
                self.playing_notes.remove(actual_note)
                
            self.piano_widget.set_key_pressed(ui_note, False)
            self.pressed_keys.remove(key_char)
            self.update_playing_label()

    def release_all(self):
        for char in list(self.pressed_keys):
            offset = KEYBOARD_MAPPED_NOTES[char]
            ui_note = START_NOTE + offset
            self.piano_widget.set_key_pressed(ui_note, False)
            
        for note in list(self.playing_notes):
            self.audio.note_off(note)
            
        self.pressed_keys.clear()
        self.playing_notes.clear()

    def closeEvent(self, event):
        self.audio.close()
        event.accept()
