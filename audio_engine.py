import pygame
import pygame.midi
from config import MIDI_PROGRAM_PIANO, DEFAULT_VELOCITY

class AudioEngine:
    def __init__(self):
        pygame.init()
        pygame.midi.init()
        self.midi_out = None
        self.sustain_active = False
        
        # Track currently sounding notes so we don't hold them forever if released
        self.active_notes = set()

        try:
            port = pygame.midi.get_default_output_id()
            if port != -1:
                self.midi_out = pygame.midi.Output(port, 0)
                self.midi_out.set_instrument(MIDI_PROGRAM_PIANO)
                print(f"Initialized MIDI on port {port}")
            else:
                print("No default MIDI output found!")
        except Exception as e:
            print(f"Failed to initialize MIDI: {e}")

    def note_on(self, note, velocity=None):
        if self.midi_out is None:
            return
            
        if velocity is None:
            velocity = DEFAULT_VELOCITY
            
        # Optional: Send note_off if the note is already playing to retrigger cleanly
        if note in self.active_notes:
            self.midi_out.note_off(note, 0)
            
        self.midi_out.note_on(note, velocity)
        self.active_notes.add(note)

    def note_off(self, note):
        if self.midi_out is None:
            return
        
        # Send actual note_off to MIDI synth.
        # If sustain is active, we've increased the Release Time (CC 72)
        # so it naturally fades out instead of abruptly stopping!
        self.midi_out.note_off(note, 0)
        
        if note in self.active_notes:
            self.active_notes.remove(note)

    def set_sustain(self, active):
        if self.midi_out is None:
            return
            
        self.sustain_active = active
        
        # Instead of using the traditional Sustain Pedal (CC 64) which holds continuous 
        # instruments like pads and strings infinitely at maximum volume,
        # we configure the envelope Release Time (CC 72).
        # This forces the synthesizer to emulate natural decay fade-out for all patches!
        
        release_val = 115 if active else 64  # Default is 64. 115 is a long realistic decay.
        self.midi_out.write_short(0xB0, 72, release_val)
        
        # Ensure traditional sustain is off so it doesn't blockade the release envelope
        self.midi_out.write_short(0xB0, 64, 0)

    def set_instrument(self, program):
        if self.midi_out:
            # Stop all notes before switching
            for note in list(self.active_notes):
                self.midi_out.note_off(note, 0)
            self.active_notes.clear()
            
            # CC 123 is "All Notes Off"
            self.midi_out.write_short(0xB0, 123, 0)
            # Temporarily reset Release Time to silence anything decaying quickly
            self.midi_out.write_short(0xB0, 72, 64)
            
            self.midi_out.set_instrument(program)
            
            # Restore Release Time state if sustain was checked
            if self.sustain_active:
                self.midi_out.write_short(0xB0, 72, 115)

    def set_volume(self, volume):
        if self.midi_out:
            # volume should be between 0.0 and 1.0
            val = int(volume * 127)
            # CC 7 is Channel Volume
            self.midi_out.write_short(0xB0, 7, val)

    def close(self):
        if self.midi_out:
            # Turn off all notes just in case
            for note in range(128):
                self.midi_out.note_off(note, 0)
            self.midi_out.close()
            pygame.midi.quit()
