import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import asyncio
import sys
import os
from dotenv import dotenv_values

# Add the parent directory to sys.path for backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
env_vars = dotenv_values(os.path.join(os.path.dirname(__file__), '..', '.env'))
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Jarvis")

class JarvisAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{Assistantname} AI Assistant")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#1a1a1a")
        
        # Performance optimizations
        self.root.tk.call('tk', 'scaling', 1.0)  # Prevent scaling issues
        self.root.option_add('*tearOff', False)  # Disable tear-off menus
        
        # Initialize variables
        self.is_mic_on = False
        self.speech_thread = None
        self.stop_speech_event = threading.Event()
        
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
                
                # Import modules with error handling
                from Backend.Chatbot import ChatBot
                self.update_status("Loading Chatbot...")
                
                from Backend.Model import FirstLayerDMM
                self.update_status("Loading Decision Model...")
                
                from Backend.Automation import Automation
                self.update_status("Loading Automation...")
                
                # Try to import optional modules
                try:
                    from Backend.RealtimeSearchEngine import RealtimeSearchEngine
                    self.update_status("Loading Search Engine...")
                except ImportError:
                    print("⚠️ RealtimeSearchEngine not available")
                    RealtimeSearchEngine = None
                
                try:
                    from Backend.ImageGeneration import GenerateImages
                    self.update_status("Loading Image Generation...")
                except ImportError:
                    print("⚠️ ImageGeneration not available")
                    GenerateImages = None
                
                try:
                    from Backend.TextToSpeech import text_to_speech
                    self.update_status("Loading Text-to-Speech...")
                except ImportError:
                    print("⚠️ Text-to-Speech not available")
                    text_to_speech = None
                
                try:
                    from Backend.SpeechToText import SpeechRecognition, QueryModifier, UniversalTranslator
                    self.update_status("Loading Speech Recognition...")
                except ImportError:
                    print("⚠️ Speech Recognition not available")
                    SpeechRecognition = None
                    QueryModifier = None
                    UniversalTranslator = None
                
                self.backend_loaded = True
                self.update_status("Backend modules loaded successfully")
                
            except Exception as e:
                print(f"❌ Backend loading error: {e}")
                self.update_status(f"Error loading backend: {str(e)}")
                messagebox.showerror("Backend Error", f"Failed to load backend modules: {str(e)}")
    
    def create_widgets(self):
        """Create and arrange all UI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text=f"{Assistantname} AI Assistant",
            font=("Arial", 18, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        title_label.pack(pady=(0, 20))
        
        # Chat display area
        self.create_chat_area(main_frame)
        
        # Input area
        self.create_input_area(main_frame)
        
        # Control buttons
        self.create_control_buttons(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_chat_area(self, parent):
        """Create the chat display area"""
        chat_frame = tk.Frame(parent, bg="#1a1a1a")
        chat_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Chat display with scrollbar
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Arial", 11),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="#ffffff",
            selectbackground="#0078d7",
            state=tk.DISABLED
        )
        self.chat_display.pack(fill="both", expand=True)
        
        # Configure text tags for different message types
        self.chat_display.tag_configure("user", foreground="#87CEEB")
        self.chat_display.tag_configure("assistant", foreground="#98FB98")
        self.chat_display.tag_configure("system", foreground="#FFB6C1")
        self.chat_display.tag_configure("error", foreground="#FF6B6B")
    
    def create_input_area(self, parent):
        """Create the input area"""
        input_frame = tk.Frame(parent, bg="#1a1a1a")
        input_frame.pack(fill="x", pady=(0, 10))
        
        # Input field
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            bd=5
        )
        self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.process_input)
        
        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.process_input,
            bg="#0078d7",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=20,
            cursor="hand2"
        )
        self.send_button.pack(side="right")
    
    def create_control_buttons(self, parent):
        """Create control buttons"""
        control_frame = tk.Frame(parent, bg="#1a1a1a")
        control_frame.pack(fill="x", pady=(0, 10))
        
        # Microphone button
        self.mic_button = tk.Button(
            control_frame,
            text="🎤 Start Listening",
            command=self.toggle_microphone,
            bg="#28a745",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=20,
            cursor="hand2"
        )
        self.mic_button.pack(side="left", padx=(0, 10))
        
        # Clear chat button
        clear_button = tk.Button(
            control_frame,
            text="Clear Chat",
            command=self.clear_chat,
            bg="#dc3545",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=20,
            cursor="hand2"
        )
        clear_button.pack(side="left", padx=(0, 10))
        
        # Exit button
        exit_button = tk.Button(
            control_frame,
            text="Exit",
            command=self.on_closing,
            bg="#6c757d",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=20,
            cursor="hand2"
        )
        exit_button.pack(side="right")
    
    def create_status_bar(self, parent):
        """Create status bar"""
        self.status_label = tk.Label(
            parent,
            text="Ready",
            font=("Arial", 9),
            fg="#888888",
            bg="#1a1a1a",
            anchor="w"
        )
        self.status_label.pack(fill="x", side="bottom")
    
    def update_chat_display(self, message, tag="assistant"):
        """Update the chat display with a new message"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n\n", tag)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def update_status(self, status):
        """Update the status bar"""
        self.status_label.config(text=status)
        self.root.update_idletasks()
    
    def process_input(self, event=None):
        """Process text input from the entry field"""
        query = self.input_field.get().strip()
        if not query:
            return
        
        # Clear input field
        self.input_field.delete(0, tk.END)
        
        # Display user message
        self.update_chat_display(f"{Username}: {query}", "user")
        
        # Process query in background thread
        threading.Thread(target=self.process_query_background, args=(query,), daemon=True).start()
    
    def process_query_background(self, query):
        """Process query in background thread"""
        try:
            # Load backend if not already loaded
            self.lazy_import_backend()
            
            if not self.backend_loaded:
                self.update_chat_display("❌ Backend modules not available", "error")
                return
            
            self.update_status("Processing query...")
            
            # Show typing indicator
            self.root.after(0, lambda: self.update_chat_display("🤔 Thinking...", "system"))
            
            # Get commands from FirstLayerDMM
            try:
                commands = FirstLayerDMM(query)
                self.update_status(f"Commands identified: {len(commands)}")
            except Exception as e:
                self.root.after(0, lambda: self.update_chat_display(f"❌ Error in command processing: {str(e)}", "error"))
                self.update_status("Error in command processing")
                return
            
            responses = []
            
            for command in commands:
                try:
                    if command.startswith("exit"):
                        self.root.after(0, self.on_closing)
                        return
                    
                    elif command.startswith("general "):
                        response = ChatBot(command.removeprefix("general "))
                        responses.append(response)
                    
                    elif command.startswith("realtime "):
                        if RealtimeSearchEngine:
                            response = RealtimeSearchEngine(command.removeprefix("realtime "))
                            responses.append(response)
                        else:
                            responses.append("⚠️ Realtime search not available")
                    
                    elif command.startswith("generate image "):
                        if GenerateImages:
                            GenerateImages(command.removeprefix("generate image "))
                            responses.append("✅ Images generated and displayed.")
                        else:
                            responses.append("⚠️ Image generation not available")
                    
                    elif command.startswith(("open ", "close ", "play ", "content ", 
                                           "google search ", "youtube search ", "system ")):
                        if Automation:
                            asyncio.run(Automation([command]))
                            responses.append("✅ Task executed successfully.")
                        else:
                            responses.append("⚠️ Automation not available")
                    
                    else:
                        responses.append(f"❓ Unrecognized command: {command}")
                
                except Exception as e:
                    error_msg = f"❌ Error executing '{command}': {str(e)}"
                    responses.append(error_msg)
                    print(f"Command execution error: {e}")
            
            # Display response
            full_response = "\n".join(responses) if responses else "No response generated."
            self.root.after(0, lambda: self.update_chat_display(f"{Assistantname}: {full_response}", "assistant"))
            
            # Convert response to speech in background
            if responses and text_to_speech:
                try:
                    threading.Thread(target=text_to_speech, args=(full_response,), daemon=True).start()
                except Exception as e:
                    print(f"TTS error: {e}")
            
            self.update_status("Ready")
            
        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)}"
            self.root.after(0, lambda: self.update_chat_display(error_msg, "error"))
            self.update_status("Error occurred")
            print(f"Process query error: {e}")
    
    def toggle_microphone(self):
        """Toggle microphone on/off"""
        if not self.is_mic_on:
            self.start_speech_recognition()
        else:
            self.stop_speech_recognition()
    
    def start_speech_recognition(self):
        """Start speech recognition"""
        try:
            self.lazy_import_backend()
            
            if not self.backend_loaded:
                messagebox.showerror("Error", "Backend modules not loaded")
                return
            
            self.is_mic_on = True
            self.mic_button.config(text="🛑 Stop Listening", bg="#dc3545")
            self.stop_speech_event.clear()
            self.update_status("Listening...")
            
            # Start speech recognition in background thread
            self.speech_thread = threading.Thread(target=self.speech_recognition_loop, daemon=True)
            self.speech_thread.start()
            
        except Exception as e:
            messagebox.showerror("Speech Recognition Error", f"Failed to start speech recognition: {str(e)}")
            self.is_mic_on = False
            self.mic_button.config(text="🎤 Start Listening", bg="#28a745")
    
    def stop_speech_recognition(self):
        """Stop speech recognition"""
        self.is_mic_on = False
        self.mic_button.config(text="🎤 Start Listening", bg="#28a745")
        self.stop_speech_event.set()
        self.update_status("Ready")
    
    def speech_recognition_loop(self):
        """Speech recognition loop running in background thread"""
        while not self.stop_speech_event.is_set() and self.is_mic_on:
            try:
                if SpeechRecognition:
                    text = SpeechRecognition()
                    
                    if text and not text.startswith("[") and text.strip():
                        # Process the recognized text
                        if QueryModifier and UniversalTranslator:
                            translated_text = UniversalTranslator(text)
                            modified_query = QueryModifier(translated_text)
                        else:
                            modified_query = text
                        
                        # Update UI in main thread
                        self.root.after(0, lambda q=modified_query: self.process_recognized_speech(q))
                else:
                    # Speech recognition not available
                    self.root.after(0, lambda: self.update_status("⚠️ Speech recognition not available"))
                    break
                    
            except Exception as e:
                print(f"Speech recognition error: {e}")
                self.root.after(0, lambda: self.update_status(f"Speech error: {str(e)}"))
                break
    
    def process_recognized_speech(self, query):
        """Process recognized speech in main thread"""
        if query and query.strip():
            self.update_chat_display(f"🎤 Heard: {query}", "user")
            threading.Thread(target=self.process_query_background, args=(query,), daemon=True).start()
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.update_status("Chat cleared")
    
    def on_closing(self):
        """Handle window close event"""
        if self.is_mic_on:
            self.stop_speech_recognition()
        
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisAIApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()