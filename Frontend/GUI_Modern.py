import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import threading
import asyncio
import sys
import os
from dotenv import dotenv_values
from Frontend.voice_waveform import VoiceWaveform, VoiceLevelIndicator
from Frontend.streaming_text import StreamingTextWidget, TypingIndicator

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Add the parent directory to sys.path for backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
env_vars = dotenv_values("E:\\COde\\py\\jarvisAI\\.env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Jarvis")

class JarvisAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{Assistantname} AI Assistant")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        
        # Initialize variables
        self.is_mic_on = False
        self.speech_thread = None
        self.stop_speech_event = threading.Event()
        
        # Voice visualization components
        self.voice_waveform = None
        self.voice_level_indicator = None
        
        # Streaming text components
        self.streaming_widget = None
        self.typing_indicator = None
        
        # Create the UI
        self.create_widgets()
        
        # Lazy import backend modules
        self.backend_loaded = False
        
    def lazy_import_backend(self):
        """Import backend modules only when needed"""
        if not self.backend_loaded:
            try:
                global ChatBot, RealtimeSearchEngine, FirstLayerDMM, Automation
                global GenerateImages, text_to_speech, SpeechRecognition, QueryModifier, UniversalTranslator
                
                from Backend.Chatbot import ChatBot
                from Backend.RealtimeSearchEngine import RealtimeSearchEngine
                from Backend.Model import FirstLayerDMM
                from Backend.Automation import Automation
                from Backend.ImageGeneration import GenerateImages
                from Backend.TextToSpeech import text_to_speech
                from Backend.SpeechToText import SpeechRecognition, QueryModifier, UniversalTranslator
                
                self.backend_loaded = True
                self.update_status("✅ Backend modules loaded successfully")
            except Exception as e:
                self.update_status(f"❌ Error loading backend: {str(e)}")
                messagebox.showerror("Backend Error", f"Failed to load backend modules: {str(e)}")
    
    def create_widgets(self):
        """Create and arrange all UI widgets"""
        # Configure grid weights for responsive design
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        
        # Title section
        self.create_title_section(main_frame)
        
        # Chat display area
        self.create_chat_area(main_frame)
        
        # Input area
        self.create_input_area(main_frame)
        
        # Control buttons
        self.create_control_buttons(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_title_section(self, parent):
        """Create modern title section"""
        title_frame = ctk.CTkFrame(parent, height=80, corner_radius=10)
        title_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        title_frame.grid_columnconfigure(1, weight=1)
        
        # Avatar/icon
        avatar_label = ctk.CTkLabel(
            title_frame, 
            text="🤖", 
            font=("Arial", 32),
            width=50,
            height=50
        )
        avatar_label.grid(row=0, column=0, padx=15, pady=15)
        
        # Title text
        title_label = ctk.CTkLabel(
            title_frame,
            text=f"{Assistantname} AI Assistant",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        title_label.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        
        # Settings button
        settings_btn = ctk.CTkButton(
            title_frame,
            text="⚙️",
            width=40,
            height=40,
            font=("Arial", 16),
            command=self.open_settings
        )
        settings_btn.grid(row=0, column=2, padx=15, pady=15)
    
    def create_chat_area(self, parent):
        """Create modern chat display area with streaming support"""
        chat_frame = ctk.CTkFrame(parent, corner_radius=10)
        chat_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        chat_frame.grid_columnconfigure(0, weight=1)
        chat_frame.grid_rowconfigure(0, weight=1)
        
        # Create streaming text widget
        self.streaming_widget = StreamingTextWidget(chat_frame, width=800, height=400)
        self.streaming_widget.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Create typing indicator
        self.typing_indicator = TypingIndicator(self.streaming_widget.frame)
        
        # Welcome message
        self.streaming_widget.add_complete_message("system", f"👋 Welcome to {Assistantname}! I'm ready to help you.")
    
    def create_input_area(self, parent):
        """Create modern input area"""
        input_frame = ctk.CTkFrame(parent, corner_radius=10)
        input_frame.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Input field with modern styling
        self.input_field = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your message here...",
            font=ctk.CTkFont(size=14),
            height=45,
            corner_radius=8,
            border_width=2
        )
        self.input_field.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.input_field.bind("<Return>", self.process_input)
        
        # Send button with icon
        self.send_button = ctk.CTkButton(
            input_frame,
            text="📤",
            width=60,
            height=45,
            font=("Arial", 16),
            command=self.process_input,
            corner_radius=8
        )
        self.send_button.grid(row=0, column=1, padx=(5, 10), pady=10)
    
    def create_control_buttons(self, parent):
        """Create modern control buttons with voice visualization"""
        control_frame = ctk.CTkFrame(parent, height=120, corner_radius=10)
        control_frame.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="ew")
        control_frame.grid_columnconfigure(1, weight=1)
        
        # Left side - Voice controls
        voice_frame = ctk.CTkFrame(control_frame, width=500, corner_radius=8)
        voice_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
        
        # Voice waveform visualization
        self.voice_waveform = VoiceWaveform(voice_frame, width=400, height=60)
        self.voice_waveform.canvas.grid(row=0, column=0, padx=10, pady=5)
        
        # Voice level indicator
        self.voice_level_indicator = VoiceLevelIndicator(voice_frame, width=20, height=60)
        self.voice_level_indicator.frame.grid(row=0, column=1, padx=(0, 10), pady=5)
        
        # Microphone button
        self.mic_button = ctk.CTkButton(
            voice_frame,
            text="🎤 Start Listening",
            command=self.toggle_microphone,
            width=180,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.mic_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        # Center - Action buttons
        action_frame = ctk.CTkFrame(control_frame, corner_radius=8)
        action_frame.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)
        
        # Voice settings button
        voice_btn = ctk.CTkButton(
            action_frame,
            text="🔊 Voice",
            command=self.open_voice_settings,
            width=100,
            height=35,
            font=ctk.CTkFont(size=12),
            corner_radius=8
        )
        voice_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Clear chat button
        clear_button = ctk.CTkButton(
            action_frame,
            text="🗑️ Clear",
            command=self.clear_chat,
            width=100,
            height=35,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        clear_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Theme toggle button
        theme_btn = ctk.CTkButton(
            action_frame,
            text="🌙 Theme",
            command=self.toggle_theme,
            width=100,
            height=35,
            font=ctk.CTkFont(size=12),
            corner_radius=8
        )
        theme_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Right side - Exit button
        exit_button = ctk.CTkButton(
            control_frame,
            text="❌ Exit",
            command=self.on_closing,
            width=100,
            height=35,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        exit_button.grid(row=0, column=2, padx=(5, 10), pady=10, sticky="e")
    
    def create_status_bar(self, parent):
        """Create modern status bar"""
        status_frame = ctk.CTkFrame(parent, height=40, corner_radius=10)
        status_frame.grid(row=4, column=0, padx=10, pady=(5, 10), sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)
        
        # Status indicator
        self.status_indicator = ctk.CTkLabel(
            status_frame,
            text="🟢",
            font=("Arial", 12),
            width=20
        )
        self.status_indicator.grid(row=0, column=0, padx=(10, 5), pady=10)
        
        # Status text
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.status_label.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        
        # Connection status
        self.connection_label = ctk.CTkLabel(
            status_frame,
            text="🌐 Connected",
            font=ctk.CTkFont(size=12),
            text_color="#28a745"
        )
        self.connection_label.grid(row=0, column=2, padx=(5, 10), pady=10)
    
    def add_message(self, msg_type, content):
        """Add a message to the chat display"""
        self.streaming_widget.add_complete_message(msg_type, content)
    
    def start_streaming_message(self, msg_type, prefix=""):
        """Start streaming a message"""
        if msg_type == "assistant":
            full_prefix = f"🤖 {Assistantname}: {prefix}"
        elif msg_type == "user":
            full_prefix = f"👤 {Username}: {prefix}"
        elif msg_type == "system":
            full_prefix = f"ℹ️ System: {prefix}"
        else:  # error
            full_prefix = f"❌ Error: {prefix}"
            
        self.streaming_widget.start_streaming(msg_type, full_prefix)
    
    def stream_text(self, text_chunk, delay=0.03):
        """Stream a chunk of text"""
        self.streaming_widget.add_text(text_chunk, delay)
    
    def finish_streaming_message(self):
        """Finish the current streaming message"""
        self.streaming_widget.finish_streaming()
    
    def update_status(self, status):
        """Update the status bar"""
        self.status_label.configure(text=status)
        self.root.update_idletasks()
    
    def process_input(self, event=None):
        """Process text input from the entry field"""
        query = self.input_field.get().strip()
        if not query:
            return
        
        # Clear input field
        self.input_field.delete(0, "end")
        
        # Add user message
        self.add_message("user", query)
        
        # Process query in background thread
        threading.Thread(target=self.process_query_background, args=(query,), daemon=True).start()
    
    def process_query_background(self, query):
        """Process query in background thread with streaming responses"""
        try:
            # Load backend if not already loaded
            self.lazy_import_backend()
            
            if not self.backend_loaded:
                self.root.after(0, lambda: self.add_message("error", "Backend modules not available"))
                return
            
            self.root.after(0, lambda: self.update_status("🤔 Processing query..."))
            
            # Show typing indicator
            self.root.after(0, lambda: self.typing_indicator.show())
            
            # Get commands from FirstLayerDMM
            commands = FirstLayerDMM(query)
            
            responses = []
            
            for command in commands:
                try:
                    if command.startswith("exit"):
                        self.root.after(0, self.on_closing)
                        return
                    
                    elif command.startswith("general "):
                        # Hide typing indicator and start streaming
                        self.root.after(0, lambda: self.typing_indicator.hide())
                        self.root.after(0, lambda: self.start_streaming_message("assistant"))
                        
                        # Stream the response
                        response = ChatBot(command.removeprefix("general "))
                        self._stream_response_text(response)
                        responses.append(response)
                    
                    elif command.startswith("realtime "):
                        # Hide typing indicator and start streaming
                        self.root.after(0, lambda: self.typing_indicator.hide())
                        self.root.after(0, lambda: self.start_streaming_message("assistant"))
                        
                        # Stream the response
                        response = RealtimeSearchEngine(command.removeprefix("realtime "))
                        self._stream_response_text(response)
                        responses.append(response)
                    
                    elif command.startswith("generate image "):
                        self.root.after(0, lambda: self.typing_indicator.hide())
                        GenerateImages(command.removeprefix("generate image "))
                        self.root.after(0, lambda: self.add_message("assistant", "✅ Images generated and displayed."))
                        responses.append("✅ Images generated and displayed.")
                    
                    elif command.startswith(("open ", "close ", "play ", "content ", 
                                           "google search ", "youtube search ", "system ")):
                        self.root.after(0, lambda: self.typing_indicator.hide())
                        asyncio.run(Automation([command]))
                        self.root.after(0, lambda: self.add_message("assistant", "✅ Task executed successfully."))
                        responses.append("✅ Task executed successfully.")
                    
                    else:
                        self.root.after(0, lambda: self.typing_indicator.hide())
                        responses.append(f"❓ Unrecognized command: {command}")
                
                except Exception as e:
                    error_msg = f"❌ Error executing '{command}': {str(e)}"
                    responses.append(error_msg)
                    print(f"Command execution error: {e}")
            
            # Hide typing indicator if still visible
            self.root.after(0, lambda: self.typing_indicator.hide())
            
            # Convert response to speech in background
            if responses:
                try:
                    threading.Thread(target=text_to_speech, args=("\n".join(responses),), daemon=True).start()
                except Exception as e:
                    print(f"TTS error: {e}")
            
            self.root.after(0, lambda: self.update_status("✅ Ready"))
            
        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)}"
            self.root.after(0, lambda: self.typing_indicator.hide())
            self.root.after(0, lambda: self.add_message("error", error_msg))
            self.root.after(0, lambda: self.update_status("❌ Error occurred"))
            print(f"Process query error: {e}")
    
    def _stream_response_text(self, response):
        """Stream response text character by character"""
        if not response:
            return
            
        # Stream the response word by word for better readability
        words = response.split()
        current_sentence = ""
        
        for i, word in enumerate(words):
            current_sentence += word + " "
            
            # Add punctuation and stream at sentence boundaries
            if word.endswith(('.', '!', '?', ':', ';')) or i == len(words) - 1:
                self.root.after(0, lambda text=current_sentence: self.stream_text(text + " ", 0.05))
                current_sentence = ""
                time.sleep(0.1)  # Pause between sentences
            else:
                # Stream word by word for longer responses
                if len(response) > 100:
                    self.root.after(0, lambda text=word + " ": self.stream_text(text, 0.02))
        
        # Finish streaming
        self.root.after(0, self.finish_streaming_message)
    
    def toggle_microphone(self):
        """Toggle microphone on/off"""
        if not self.is_mic_on:
            self.start_speech_recognition()
        else:
            self.stop_speech_recognition()
    
    def start_speech_recognition(self):
        """Start speech recognition with waveform visualization"""
        try:
            self.lazy_import_backend()
            
            if not self.backend_loaded:
                messagebox.showerror("Error", "Backend modules not loaded")
                return
            
            self.is_mic_on = True
            self.mic_button.configure(text="🛑 Stop Listening", fg_color="#dc3545", hover_color="#c82333")
            self.stop_speech_event.clear()
            self.update_status("🎤 Listening...")
            
            # Start voice waveform visualization
            if self.voice_waveform:
                self.voice_waveform.start_recording()
            
            # Start speech recognition in background thread
            self.speech_thread = threading.Thread(target=self.speech_recognition_loop, daemon=True)
            self.speech_thread.start()
            
        except Exception as e:
            messagebox.showerror("Speech Recognition Error", f"Failed to start speech recognition: {str(e)}")
            self.is_mic_on = False
            self.mic_button.configure(text="🎤 Start Listening", fg_color="#28a745", hover_color="#218838")
            if self.voice_waveform:
                self.voice_waveform.stop_recording()
    
    def stop_speech_recognition(self):
        """Stop speech recognition"""
        self.is_mic_on = False
        self.mic_button.configure(text="🎤 Start Listening", fg_color="#28a745", hover_color="#218838")
        self.stop_speech_event.set()
        
        # Stop voice waveform visualization
        if self.voice_waveform:
            self.voice_waveform.stop_recording()
        
        # Reset voice level indicator
        if self.voice_level_indicator:
            self.voice_level_indicator.update_level(0)
        
        self.update_status("✅ Ready")
    
    def speech_recognition_loop(self):
        """Speech recognition loop running in background thread"""
        while not self.stop_speech_event.is_set() and self.is_mic_on:
            try:
                text = SpeechRecognition()
                
                if text and not text.startswith("[") and text.strip():
                    # Process the recognized text
                    translated_text = UniversalTranslator(text)
                    modified_query = QueryModifier(translated_text)
                    
                    # Update UI in main thread
                    self.root.after(0, lambda q=modified_query: self.process_recognized_speech(q))
                    
            except Exception as e:
                print(f"Speech recognition error: {e}")
                self.root.after(0, lambda: self.update_status(f"❌ Speech error: {str(e)}"))
    
    def process_recognized_speech(self, query):
        """Process recognized speech in main thread"""
        if query and query.strip():
            self.add_message("user", f"🎤 {query}")
            # Only process if backend is available
            if self.backend_loaded:
                threading.Thread(target=self.process_query_background, args=(query,), daemon=True).start()
    
    def clear_chat(self):
        """Clear the chat display"""
        # Clear all messages from streaming widget
        for widget in self.streaming_widget.frame.winfo_children():
            widget.destroy()
        
        # Add welcome message
        self.streaming_widget.add_complete_message("system", "🗑️ Chat cleared. Ready for new conversation.")
        self.update_status("✅ Chat cleared")
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
            self.update_status("☀️ Switched to Light theme")
        else:
            ctk.set_appearance_mode("Dark")
            self.update_status("🌙 Switched to Dark theme")
    
    def open_settings(self):
        """Open settings dialog"""
        messagebox.showinfo("Settings", "⚙️ Settings panel coming soon!")
    
    def open_voice_settings(self):
        """Open voice settings dialog"""
        messagebox.showinfo("Voice Settings", "🔊 Voice settings coming soon!")
    
    def on_closing(self):
        """Handle window close event with cleanup"""
        if self.is_mic_on:
            self.stop_speech_recognition()
        
        # Clean up voice visualization components
        if self.voice_waveform:
            self.voice_waveform.destroy()
        
        if messagebox.askokcancel("Quit", f"Do you want to quit {Assistantname}?"):
            self.root.destroy()

# Main execution
if __name__ == "__main__":
    root = ctk.CTk()
    app = JarvisAIApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
