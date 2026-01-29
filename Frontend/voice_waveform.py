import numpy as np
import threading
import time
from collections import deque
import customtkinter as ctk

# Try to import pyaudio, provide fallback
pyaudio = None
PYAUDIO_AVAILABLE = False
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("⚠️ PyAudio not available. Voice waveform will be disabled.")
except Exception as e:
    PYAUDIO_AVAILABLE = False
    print(f"⚠️ PyAudio error: {e}. Voice waveform will be disabled.")

class VoiceWaveform:
    def __init__(self, parent, width=400, height=100):
        self.parent = parent
        self.width = width
        self.height = height
        self.is_recording = False
        self.stop_event = threading.Event()
        
        # Audio parameters
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16 if PYAUDIO_AVAILABLE and pyaudio else None
        self.CHANNELS = 1
        self.RATE = 16000
        
        # Waveform data
        self.waveform_data = deque(maxlen=100)
        
        # Create canvas for waveform
        self.canvas = ctk.CTkCanvas(
            parent,
            width=width,
            height=height,
            bg="#1a1a1a",
            highlightthickness=0
        )
        
        # Initialize pyaudio if available
        self.pa = None
        self.stream = None
        if PYAUDIO_AVAILABLE:
            try:
                self.pa = pyaudio.PyAudio()
            except Exception as e:
                print(f"⚠️ Could not initialize PyAudio: {e}")
                PYAUDIO_AVAILABLE = False
        
    def start_recording(self):
        """Start recording and visualizing audio"""
        if not PYAUDIO_AVAILABLE:
            # Show disabled state
            self._show_disabled_message()
            return
            
        if self.is_recording:
            return
            
        self.is_recording = True
        self.stop_event.clear()
        self.waveform_data.clear()
        
        try:
            # Start audio stream
            self.stream = self.pa.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
        except Exception as e:
            print(f"⚠️ Could not start audio stream: {e}")
            self.is_recording = False
            self._show_error_message()
            return
        
        # Start visualization thread
        self.visualization_thread = threading.Thread(target=self._visualize_loop, daemon=True)
        self.visualization_thread.start()
        
    def stop_recording(self):
        """Stop recording"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        self.stop_event.set()
        
        # Stop audio stream
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
            self.stream = None
            
        # Clear the canvas
        self.canvas.delete("all")
        
    def _show_disabled_message(self):
        """Show message when PyAudio is not available"""
        self.canvas.delete("all")
        self.canvas.create_text(
            self.width//2, self.height//2,
            text="🎤 Audio Not Available\nInstall PyAudio: pip install pyaudio",
            fill="#888888",
            font=("Arial", 10),
            justify="center"
        )
        
    def _show_error_message(self):
        """Show error message"""
        self.canvas.delete("all")
        self.canvas.create_text(
            self.width//2, self.height//2,
            text="❌ Audio Error\nCheck microphone permissions",
            fill="#dc3545",
            font=("Arial", 10),
            justify="center"
        )
        
    def _visualize_loop(self):
        """Main visualization loop with simulated data if needed"""
        while not self.stop_event.is_set() and self.is_recording:
            try:
                if self.stream:
                    # Read actual audio data
                    data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                    
                    # Convert to numpy array
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    
                    # Calculate RMS (volume)
                    if len(audio_data) > 0:
                        rms = np.sqrt(np.mean(np.square(audio_data, dtype=np.float64)))
                        self.waveform_data.append(rms)
                else:
                    # Simulate waveform data for demo
                    import random
                    simulated_value = random.uniform(0, 1000)
                    self.waveform_data.append(simulated_value)
                
                # Update visualization
                self._update_waveform()
                
                time.sleep(0.05)  # 20 FPS
                
            except Exception as e:
                print(f"Waveform error: {e}")
                break
                
    def _update_waveform(self):
        """Update the waveform visualization"""
        self.canvas.delete("all")
        
        if len(self.waveform_data) < 2:
            return
            
        # Draw background grid
        self._draw_grid()
        
        # Calculate points for waveform
        points = []
        for i, value in enumerate(self.waveform_data):
            x = (i / len(self.waveform_data)) * self.width
            
            # Normalize value to canvas height
            max_value = max(self.waveform_data) if self.waveform_data else 1
            normalized_value = (value / max_value) if max_value > 0 else 0
            y = self.height - (normalized_value * self.height * 0.8) - 10
            
            points.extend([x, y])
            
        # Draw waveform line
        if len(points) >= 4:
            # Create gradient effect
            for i in range(0, len(points) - 2, 2):
                intensity = int(255 * (i / len(points)))
                color = f"#{intensity:02x}{100:02x}{255-intensity:02x}"
                
                if i + 3 < len(points):
                    self.canvas.create_line(
                        points[i], points[i+1], points[i+2], points[i+3],
                        fill=color, width=2, smooth=True
                    )
                    
    def _draw_grid(self):
        """Draw background grid"""
        # Horizontal lines
        for i in range(0, self.height, 20):
            self.canvas.create_line(
                0, i, self.width, i,
                fill="#2a2a2a", width=1
            )
            
        # Vertical lines
        for i in range(0, self.width, 40):
            self.canvas.create_line(
                i, 0, i, self.height,
                fill="#2a2a2a", width=1
            )
            
    def destroy(self):
        """Clean up resources"""
        self.stop_recording()
        if self.pa:
            try:
                self.pa.terminate()
            except:
                pass

class VoiceLevelIndicator:
    def __init__(self, parent, width=20, height=100):
        self.parent = parent
        self.width = width
        self.height = height
        
        # Create frame for level indicator
        self.frame = ctk.CTkFrame(parent, width=width, height=height, corner_radius=5)
        
        # Create canvas for level bars
        self.canvas = ctk.CTkCanvas(
            self.frame,
            width=width-4,
            height=height-4,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.canvas.pack(padx=2, pady=2)
        
        self.current_level = 0
        
    def update_level(self, level):
        """Update the volume level (0.0 to 1.0)"""
        self.current_level = max(0, min(1, level))
        self._draw_level()
        
    def _draw_level(self):
        """Draw the level bars"""
        self.canvas.delete("all")
        
        # Calculate number of bars
        num_bars = 10
        bar_height = (self.height - 8) / num_bars
        
        # Draw bars
        for i in range(num_bars):
            y_start = self.height - 4 - (i * bar_height)
            y_end = y_start - bar_height + 2
            
            # Determine color based on level
            if i < self.current_level * num_bars:
                if i < 3:
                    color = "#28a745"  # Green
                elif i < 7:
                    color = "#ffc107"  # Yellow
                else:
                    color = "#dc3545"  # Red
            else:
                color = "#2a2a2a"  # Dark gray
                
            self.canvas.create_rectangle(
                4, y_start, self.width - 4, y_end,
                fill=color, outline=""
            )
