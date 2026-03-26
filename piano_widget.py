import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QRect

from config import (
    COLOR_WHITE_KEY, COLOR_BLACK_KEY, COLOR_WHITE_KEY_PRESSED,
    COLOR_BLACK_KEY_PRESSED, COLOR_OUTLINE, is_black_key, get_note_name,
    KEYBOARD_MAPPED_NOTES
)

class PianoWidget(QWidget):
    note_pressed = pyqtSignal(int)
    note_released = pyqtSignal(int)

    def __init__(self, start_note=48, num_keys=36, parent=None):
        super().__init__(parent)
        self.start_note = start_note
        self.num_keys = num_keys
        self.pressed_notes = set()
        
        self.num_white_keys = sum(not is_black_key(i) for i in range(self.num_keys))
        self.setMinimumHeight(200)
        self.mouse_pressed_note = None
        
        self.offset_to_char = {v: k for k, v in KEYBOARD_MAPPED_NOTES.items()}

    def set_key_pressed(self, note, pressed):
        if pressed:
            self.pressed_notes.add(note)
        else:
            if note in self.pressed_notes:
                self.pressed_notes.remove(note)
        self.update()

    def mousePressEvent(self, event):
        note = self.get_note_at_pos(event.pos())
        if note is not None:
            self.mouse_pressed_note = note
            self.note_pressed.emit(note)
            self.set_key_pressed(note, True)

    def mouseReleaseEvent(self, event):
        if self.mouse_pressed_note is not None:
            self.note_released.emit(self.mouse_pressed_note)
            self.set_key_pressed(self.mouse_pressed_note, False)
            self.mouse_pressed_note = None

    def get_note_at_pos(self, pos):
        rects = self.calculate_key_rects()
        
        for note, rect, is_black in rects:
            if is_black and rect.contains(pos):
                return note
                
        for note, rect, is_black in rects:
            if not is_black and rect.contains(pos):
                return note
                
        return None

    def calculate_key_rects(self):
        rects = []
        if self.num_white_keys == 0:
            return rects

        white_key_width = self.width() / self.num_white_keys
        white_key_height = self.height()
        black_key_width = white_key_width * 0.6
        black_key_height = white_key_height * 0.6

        white_idx = 0
        
        for i in range(self.num_keys):
            note = self.start_note + i
            if not is_black_key(i):
                x = white_idx * white_key_width
                rect = QRect(int(x), 0, int(white_key_width), int(white_key_height))
                rects.append((note, rect, False))
                white_idx += 1
                
        white_idx = 0
        for i in range(self.num_keys):
            note = self.start_note + i
            if is_black_key(i):
                x = white_idx * white_key_width - (black_key_width / 2)
                rect = QRect(int(x), 0, int(black_key_width), int(black_key_height))
                rects.append((note, rect, True))
            else:
                white_idx += 1
                
        return rects

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rects = self.calculate_key_rects()
        font = QFont("Arial", 8)
        painter.setFont(font)
        
        # White keys
        for note, rect, is_black in rects:
            if not is_black:
                color = QColor(COLOR_WHITE_KEY_PRESSED) if note in self.pressed_notes else QColor(COLOR_WHITE_KEY)
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(QColor(COLOR_OUTLINE), 1))
                painter.drawRect(rect)
                
                # Draw label
                offset = note - self.start_note
                char = self.offset_to_char.get(offset, "")
                note_name = get_note_name(note)
                label = f"{note_name}\n({char})" if char else note_name
                
                painter.setPen(QPen(Qt.black))
                text_rect = QRect(rect.x(), rect.bottom() - 40, rect.width(), 40)
                painter.drawText(text_rect, Qt.AlignCenter, label)
                
        # Black keys
        painter.setPen(QPen(Qt.white))
        for note, rect, is_black in rects:
            if is_black:
                color = QColor(COLOR_BLACK_KEY_PRESSED) if note in self.pressed_notes else QColor(COLOR_BLACK_KEY)
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(QColor(COLOR_OUTLINE), 1))
                painter.drawRect(rect)
                
                offset = note - self.start_note
                char = self.offset_to_char.get(offset, "")
                note_name = get_note_name(note)
                label = f"{note_name}\n({char})" if char else note_name
                
                painter.setPen(QPen(Qt.white))
                text_rect = QRect(rect.x(), rect.bottom() - 30, rect.width(), 30)
                painter.drawText(text_rect, Qt.AlignCenter, label)
                
        painter.end()
