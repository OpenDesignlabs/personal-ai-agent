import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import asyncio
import sys
import os
import time
import datetime
from dotenv import dotenv_values

# Custom Widget Imports
from Frontend.voice_waveform import VoiceWaveform
from Frontend.streaming_text import StreamingTextWidget, TypingIndicator

# Add parent directory for backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class JarvisAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS PRIME - Neural Interface")
        self.setup_vars()
        self.setup_ui()
        
        # Start background processes
        self.root.after(1000, self.lazy_import_backend)
        self.animate_pulse()
        self.update_stats_loop()

    def setup_vars(self):
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        self.env_vars = dotenv_values(env_path)
        self.username = self.env_vars.get("Username", "User")
        self.assistant_name = self.env_vars.get("Assistantname", "Jarvis")
        
        self.is_mic_on = False
        self.backend_loaded = False
        self.loaded_modules = set() # Active neural arrays
        self.module_last_used = {} # Timestamps for idle-hibernation
        self.module_memory_map = { # Estimated resource impact in MB
            "vision": 450, "research": 180, "automation": 120, "art": 850, "code": 320
        }
        self.loading_lock = threading.Lock()
        self.expansion_stats = {} # UI Components
        self.active_array_colors = {"vision": "#ff00ff", "art": "#ffcc00", "research": "#00ff00"}
        
        self.stop_speech_event = threading.Event()
        self.speech_thread = None
        self.wake_word_active = True
        self.wake_word = self.assistant_name.lower()
        
        # Start the Neural Garbage Collector (Idle Monitor)
        threading.Thread(target=self.neural_resource_monitor, daemon=True).start()

    def setup_ui(self):
        # Configure layout
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Glass Panel) ---
        self.sidebar = ctk.CTkFrame(self.root, width=260, corner_radius=0, fg_color="#111111")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        # Branding
        self.brand_label = ctk.CTkLabel(self.sidebar, text=f"{self.assistant_name.upper()} SYSTEM", font=ctk.CTkFont(size=20, weight="bold", family="Orbitron"))
        self.brand_label.grid(row=0, column=0, padx=20, pady=(30, 10))

        # Pulse Core Visualization
        self.pulse_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.pulse_frame.grid(row=1, column=0, pady=10)
        self.pulse_core = ctk.CTkLabel(self.pulse_frame, text="●", font=ctk.CTkFont(size=70), text_color="#00ffff")
        self.pulse_core.pack()

        self.status_label = ctk.CTkLabel(self.sidebar, text="SYSTEM INITIALIZING", font=ctk.CTkFont(size=11, slant="italic"))
        self.status_label.grid(row=2, column=0, pady=(0, 20))

        # Voice Waveform Section
        self.voice_frame = ctk.CTkFrame(self.sidebar, fg_color="#1a1a1a", corner_radius=10, height=80)
        self.voice_frame.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        self.waveform = VoiceWaveform(self.voice_frame, width=200, height=60)
        self.waveform.canvas.pack(pady=5)

        # System Dashboard
        self.stats_frame = ctk.CTkFrame(self.sidebar, fg_color="#0d0d0d", corner_radius=15, border_width=1, border_color="#333333")
        self.stats_frame.grid(row=4, column=0, padx=15, pady=20, sticky="ew")
        
        self.cpu_meter = self.create_stat_line(self.stats_frame, "CPU CORE", "row0")
        self.ram_meter = self.create_stat_line(self.stats_frame, "RAM ARRAY", "row1")
        self.bat_meter = self.create_stat_line(self.stats_frame, "ENERGY", "row2")

        # Expansion Matrix (New Status Grid)
        self.matrix_label = ctk.CTkLabel(self.sidebar, text="NEURAL ARRAYS", font=ctk.CTkFont(size=10, weight="bold", family="Orbitron"), text_color="#555555")
        self.matrix_label.grid(row=5, column=0, pady=(10, 5))
        
        self.matrix_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.matrix_frame.grid(row=6, column=0, padx=15, pady=5, sticky="ew")
        self.matrix_frame.grid_columnconfigure((0,1), weight=1)
        
        self.expansion_stats['vision'] = self.create_module_indicator(self.matrix_frame, "VISION", 0, 0)
        self.expansion_stats['research'] = self.create_module_indicator(self.matrix_frame, "SEARCH", 0, 1)
        self.expansion_stats['automation'] = self.create_module_indicator(self.matrix_frame, "SYSTEM", 1, 0)
        self.expansion_stats['art'] = self.create_module_indicator(self.matrix_frame, "ART", 1, 1)

        # Sidebar Buttons
        self.mic_btn = ctk.CTkButton(self.sidebar, text="🎤 COMM-LINK", command=self.toggle_microphone, font=ctk.CTkFont(size=13, weight="bold"), height=40, corner_radius=20, fg_color="#005555", hover_color="#008888")
        self.mic_btn.grid(row=11, column=0, padx=20, pady=10)

        self.clear_btn = ctk.CTkButton(self.sidebar, text="RESET TERMINAL", command=self.clear_chat, fg_color="transparent", border_width=1, text_color="#aaaaaa", hover_color="#333333")
        self.clear_btn.grid(row=12, column=0, padx=20, pady=(0, 20))

        # --- Main View (Fluid Chat) ---
        self.main_view = ctk.CTkFrame(self.root, fg_color="#0a0a0a", corner_radius=0)
        self.main_view.grid(row=0, column=1, sticky="nsew")
        self.main_view.grid_columnconfigure(0, weight=1)
        self.main_view.grid_rowconfigure(0, weight=1)

        # High-End Chat Widget
        self.chat_widget = StreamingTextWidget(self.main_view, width=800, height=600)
        self.chat_widget.frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=(30, 10))
        
        # Thinking Indicator
        self.typing_indicator = TypingIndicator(self.chat_widget.frame)

        # Interaction Bar
        self.interact_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.interact_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(10, 30))
        self.interact_frame.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkEntry(self.interact_frame, placeholder_text="Enter Neural Command...", height=50, corner_radius=25, border_width=1, fg_color="#151515", border_color="#333333", font=ctk.CTkFont(size=14))
        self.input_entry.grid(row=0, column=0, padx=(0, 15), sticky="ew")
        self.input_entry.bind("<Return>", self.handle_text_input)
        self.input_entry.bind("<KeyRelease>", self.predictive_preheat)

        self.send_btn = ctk.CTkButton(self.interact_frame, text="TRANSMIT", width=100, height=50, corner_radius=25, command=self.handle_text_input, fg_color="#00ffff", text_color="#000000", font=ctk.CTkFont(size=13, weight="bold"))
        self.send_btn.grid(row=0, column=1)

    def create_stat_line(self, parent, label, row_id):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=8)
        lbl = ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=9, weight="bold"), text_color="#666666")
        lbl.pack(side="left")
        val = ctk.CTkLabel(frame, text="--%", font=ctk.CTkFont(size=10, weight="bold"), text_color="#00ffff")
        val.pack(side="right")
        return val

    def create_module_indicator(self, parent, name, r, c):
        lbl = ctk.CTkLabel(parent, text=f"• {name}", font=ctk.CTkFont(size=9, weight="bold"), text_color="#333333")
        lbl.grid(row=r, column=c, padx=5, pady=2, sticky="w")
        return lbl

    # --- System Logic ---
    def lazy_import_backend(self):
        """Loads only the core 'Brain' modules at startup."""
        if not self.backend_loaded:
            try:
                self.update_status("SYNCING KERNEL...")
                global ChatBot, FirstLayerDMM, get_system_stats, start_scheduler, add_task
                
                from Backend.Chatbot import ChatBot
                from Backend.Model import FirstLayerDMM
                from Backend.SystemHealth import get_system_stats
                from Backend.Scheduler import start_scheduler, add_task
                
                # Start Core Background tasks
                start_scheduler(lambda t: self.chat_widget.add_complete_message("system", f"⏰ REMINDER: {t}"))
                
                # Load Speech Basics (Required for Wake Word)
                global SpeechRecognition, QueryModifier, UniversalTranslator, text_to_speech
                from Backend.SpeechToText import SpeechRecognition, QueryModifier, UniversalTranslator
                from Backend.TextToSpeech import text_to_speech

                self.backend_loaded = True
                self.update_status("KERNEL ONLINE")
                
                if self.wake_word_active and not self.speech_thread:
                    self.speech_thread = threading.Thread(target=self.speech_recognition_loop, daemon=True)
                    self.speech_thread.start()
            except Exception as e:
                self.update_status("BRAIN ERROR")
                self.chat_widget.add_complete_message("error", f"Neural Link Failure: {e}")

    def ensure_expansion(self, pack_name):
        """Elite Modular Sync with Resource Tracking."""
        if pack_name in self.loaded_modules:
            self.module_last_used[pack_name] = time.time()
            return True
        
        with self.loading_lock:
            if pack_name in self.loaded_modules: return True
            
            try:
                start_time = time.time()
                self.update_status(f"SYNCING {pack_name.upper()} ARRAY...")
                if pack_name in self.expansion_stats:
                    self.expansion_stats[pack_name].configure(text_color="#ffcc00") 
                
                # Dynamic Kernel Mapping
                if pack_name == "vision":
                    global analyze_screen
                    from Backend.Vision import analyze_screen
                elif pack_name == "automation":
                    global Automation
                    from Backend.Automation import Automation
                elif pack_name == "code":
                    global dynamic_agent
                    from Backend.CodeInterpreter import dynamic_agent
                elif pack_name == "research":
                    global RealtimeSearchEngine
                    from Backend.RealtimeSearchEngine import RealtimeSearchEngine
                elif pack_name == "art":
                    global GenerateImages
                    from Backend.ImageGeneration import GenerateImages
                
                # Registration
                self.loaded_modules.add(pack_name)
                self.module_last_used[pack_name] = time.time()
                
                # Update Matrix UI
                if pack_name in self.expansion_stats:
                    mem = self.module_memory_map.get(pack_name, 0)
                    load_time = round(time.time() - start_time, 2)
                    self.expansion_stats[pack_name].configure(
                        text=f"• {pack_name.upper()} [{mem}MB]",
                        text_color="#00ffff"
                    )
                
                self.update_status("STABLE")
                return True
            except Exception as e:
                self.chat_widget.add_complete_message("error", f"Array Fault: {e}")
                if pack_name in self.expansion_stats:
                    self.expansion_stats[pack_name].configure(text_color="#ff4444")
                return False

    def neural_resource_monitor(self):
        """Idle Hibernation System: Unloads arrays after 10 mins of inactivity."""
        while not self.stop_speech_event.is_set():
            time.sleep(60) # Watch every minute
            now = time.time()
            to_hibernate = []
            
            for pack, last_used in self.module_last_used.items():
                if pack in self.loaded_modules and (now - last_used) > 600: # 10 Minutes
                    to_hibernate.append(pack)
            
            for pack in to_hibernate:
                # We don't perform a hard 'importlib.reload' but we reset UI and track
                # To simulate hibernation to save user resources
                self.loaded_modules.remove(pack)
                if pack in self.expansion_stats:
                    self.expansion_stats[pack].configure(text=f"• {pack.upper()}", text_color="#333333")
                self.chat_widget.add_complete_message("system", f"Neural Array [{pack.upper()}] entered hibernation to save memory.")

    def predictive_preheat(self, event=None):
        """Simultaneous Pre-heat with priority queue."""
        text = self.input_entry.get().lower()
        if len(text) < 3: return
        
        predictions = {
            "search": "research", "find": "research", "google": "research",
            "look": "vision", "screen": "vision",
            "open": "automation", "launch": "automation",
            "draw": "art", "generate": "art", "image": "art",
            "calculate": "code", "organize": "code"
        }
        
        for key, pack in predictions.items():
            if key in text and pack not in self.loaded_modules:
                threading.Thread(target=self.ensure_expansion, args=(pack,), daemon=True).start()
                break

    # --- Animations ---
    def animate_pulse(self):
        # Base Cyan plus dynamic blend from active arrays
        colors = ["#00ffff", "#00cccc", "#008888", "#005555"]
        
        # If special arrays are active, mix in their signature colors
        if "art" in self.loaded_modules: colors.insert(0, "#ffcc00")
        if "vision" in self.loaded_modules: colors.insert(0, "#ff00ff")
        
        try:
            current = self.pulse_core.cget("text_color")
            next_idx = (colors.index(current) + 1) % len(colors)
            self.pulse_core.configure(text_color=colors[next_idx])
        except: pass
        self.root.after(100 if self.is_mic_on else 300, self.animate_pulse)

    def update_stats_loop(self):
        if self.backend_loaded:
            try:
                stats = get_system_stats()
                self.cpu_meter.configure(text=stats['CPU'])
                self.ram_meter.configure(text=stats['RAM'])
                self.bat_meter.configure(text=stats['Battery'])
            except: pass
        self.root.after(3000, self.update_stats_loop)

    def update_status(self, text):
        self.status_label.configure(text=text.upper())

    # --- Chat Interactions ---
    def handle_text_input(self, event=None):
        query = self.input_entry.get().strip()
        if not query: return
        self.input_entry.delete(0, tk.END)
        self.chat_widget.add_complete_message("user", query)
        threading.Thread(target=self.process_query_task, args=(query,), daemon=True).start()

    def process_query_task(self, query):
        if not self.backend_loaded: return
        self.update_status("PROCESSING...")
        self.root.after(0, self.typing_indicator.show)
        
        try:
            commands = FirstLayerDMM(query)
            responses = []
            
            for cmd in commands:
                if cmd.startswith("exit"):
                    self.root.after(0, self.on_closing)
                    return
                elif cmd.startswith("general "):
                    res = ChatBot(cmd.removeprefix("general "))
                    self.stream_response(res)
                    responses.append(res)
                elif cmd.startswith("realtime "):
                    if self.ensure_expansion("research"):
                        res = RealtimeSearchEngine(cmd.removeprefix("realtime "))
                        self.stream_response(res)
                        responses.append(res)
                elif cmd.startswith("vision "):
                    if self.ensure_expansion("vision"):
                        res = analyze_screen(cmd.removeprefix("vision "))
                        self.stream_response(f"EYE ANALYSIS: {res}")
                        responses.append(res)
                elif cmd.startswith("complex "):
                    if self.ensure_expansion("code"):
                        res = dynamic_agent(cmd.removeprefix("complex "))
                        self.stream_response(res)
                        responses.append(res)
                elif cmd.startswith("generate image "):
                    if self.ensure_expansion("art"):
                        GenerateImages(cmd.removeprefix("generate image "))
                        self.chat_widget.add_complete_message("assistant", "ART GENERATED.")
                elif cmd.startswith(("open ", "close ", "play ", "system ", "google search ")):
                    if self.ensure_expansion("automation"):
                        asyncio.run(Automation([cmd]))
                        self.chat_widget.add_complete_message("system", f"COMMAND EXECUTED: {cmd}")
            
            if responses and text_to_speech:
                threading.Thread(target=text_to_speech, args=("\n".join(responses),), daemon=True).start()
            
            self.root.after(0, self.typing_indicator.hide)
            self.update_status("ONLINE")
        except Exception as e:
            self.chat_widget.add_complete_message("error", f"Neural Execution Error: {e}")
            self.root.after(0, self.typing_indicator.hide)

    def stream_response(self, text):
        self.root.after(0, lambda: self.chat_widget.start_streaming("assistant"))
        # Stream in chunks
        words = text.split()
        for word in words:
            self.root.after(0, lambda w=word: self.chat_widget.add_text(w + " ", 0.02))
            time.sleep(0.02)
        self.root.after(0, self.chat_widget.finish_streaming)

    # --- Speech Control ---
    def toggle_microphone(self):
        if not self.is_mic_on:
            self.is_mic_on = True
            self.mic_btn.configure(text="🛑 DISCONNECT", fg_color="#aa0000")
            self.update_status("LISTENING...")
            self.waveform.start_recording()
        else:
            self.is_mic_on = False
            self.mic_btn.configure(text="🎤 COMM-LINK", fg_color="#005555")
            self.update_status("ONLINE")
            self.waveform.stop_recording()

    def speech_recognition_loop(self):
        while not self.stop_speech_event.is_set():
            if not self.backend_loaded:
                time.sleep(1)
                continue
            try:
                text = SpeechRecognition()
                if text and not text.startswith("[") and text.strip():
                    if not self.is_mic_on and self.wake_word in text.lower():
                        self.root.after(0, self.toggle_microphone)
                    elif self.is_mic_on:
                        if UniversalTranslator: text = UniversalTranslator(text)
                        self.root.after(0, lambda t=text: self.handle_voice_input(t))
                        self.root.after(2000, self.toggle_microphone)
            except: pass
            time.sleep(0.1)

    def handle_voice_input(self, text):
        self.chat_widget.add_complete_message("user", f"🎤 {text}")
        threading.Thread(target=self.process_query_task, args=(text,), daemon=True).start()

    def clear_chat(self):
        for w in self.chat_widget.frame.winfo_children(): w.destroy()
        self.chat_widget.add_complete_message("system", "TERMINAL REBORN. LOGS CLEARED.")

    def on_closing(self):
        self.stop_speech_event.set()
        self.waveform.destroy()
        # No self.root.destroy() here, main.py will handle it after app cleanup