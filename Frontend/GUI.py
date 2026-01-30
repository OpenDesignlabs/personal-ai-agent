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
from PIL import Image, ImageTk, ImageOps, ImageFilter

# Custom Widget Imports
from Frontend.voice_waveform import VoiceWaveform
from Frontend.streaming_text import StreamingTextWidget, TypingIndicator

# Add parent directory for backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class JarvisAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS PRIME - Neural Interface")
        
        # Set window size and appearance
        self.root.geometry("1400x900")
        ctk.set_appearance_mode("Dark")
        
        self.setup_vars()
        self.setup_ui()
        
        # Start background processes
        self.root.after(1000, self.lazy_import_backend)
        self.animate_ui()
        self.update_stats_loop()

    def setup_vars(self):
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        self.env_vars = dotenv_values(env_path)
        self.username = self.env_vars.get("Username", "Sir")
        self.assistant_name = self.env_vars.get("Assistantname", "Jarvis")
        
        self.is_mic_on = False
        self.backend_loaded = False
        self.loaded_modules = set() # Active neural arrays
        self.module_last_used = {} # Timestamps for idle-hibernation
        self.module_memory_map = { 
            "vision": 450, "research": 180, "automation": 120, "art": 850, "code": 320
        }
        self.loading_lock = threading.Lock()
        self.expansion_stats = {} 
        self.active_array_colors = {"vision": "#ff00ff", "art": "#ffcc00", "research": "#00ff00"}
        
        self.stop_speech_event = threading.Event()
        self.speech_thread = None
        self.wake_word_active = True
        self.wake_word = self.assistant_name.lower()
        
        # Animation variables
        self.core_zoom = 1.0
        self.core_direction = 1
        
        # Start the Neural Garbage Collector (Idle Monitor)
        threading.Thread(target=self.neural_resource_monitor, daemon=True).start()

    def setup_ui(self):
        # Master Layout Configuration
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Background Base Frame
        self.bg_frame = ctk.CTkFrame(self.root, fg_color="#050505", corner_radius=0)
        self.bg_frame.grid(row=0, column=0, sticky="nsew")
        self.bg_frame.grid_columnconfigure(0, weight=3) # Chat area
        self.bg_frame.grid_columnconfigure(1, weight=1) # Dashboard area
        self.bg_frame.grid_rowconfigure(0, weight=1)

        # --- LEFT: PRIMARY NEXUS (Chat & Interaction) ---
        self.nexus_frame = ctk.CTkFrame(self.bg_frame, fg_color="transparent", corner_radius=0)
        self.nexus_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.nexus_frame.grid_columnconfigure(0, weight=1)
        self.nexus_frame.grid_rowconfigure(0, weight=1)

        # Neural Terminal (Chat)
        self.chat_container = ctk.CTkFrame(self.nexus_frame, fg_color="#0a0a0b", corner_radius=20, border_width=1, border_color="#1a1a1c")
        self.chat_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 20))
        self.chat_container.grid_columnconfigure(0, weight=1)
        self.chat_container.grid_rowconfigure(0, weight=1)

        self.chat_widget = StreamingTextWidget(self.chat_container, width=800, height=600)
        self.chat_widget.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.typing_indicator = TypingIndicator(self.chat_widget.frame)

        # Floating Interaction Nexus (Input)
        self.input_nexus = ctk.CTkFrame(self.nexus_frame, fg_color="#0f0f12", corner_radius=30, height=80, border_width=1, border_color="#26262b")
        self.input_nexus.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.input_nexus.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkEntry(self.input_nexus, placeholder_text=f"Awaiting Directives, {self.username}...", 
                                        height=60, corner_radius=25, border_width=0, fg_color="transparent", 
                                        font=ctk.CTkFont(size=15, family="Segoe UI Semibold"))
        self.input_entry.grid(row=0, column=0, padx=(25, 10), sticky="ew")
        self.input_entry.bind("<Return>", self.handle_text_input)
        self.input_entry.bind("<KeyRelease>", self.predictive_preheat)

        self.mic_prime = ctk.CTkButton(self.input_nexus, text="🎤", width=50, height=50, corner_radius=25, 
                                       fg_color="#1a1a1c", hover_color="#2a2a2e", font=ctk.CTkFont(size=18),
                                       command=self.toggle_microphone)
        self.mic_prime.grid(row=0, column=1, padx=(0, 10))

        self.send_prime = ctk.CTkButton(self.input_nexus, text="➤", width=50, height=50, corner_radius=25, 
                                        fg_color="#00d4ff", text_color="#000000", font=ctk.CTkFont(size=18),
                                        command=self.handle_text_input)
        self.send_prime.grid(row=0, column=2, padx=(0, 15))

        # --- RIGHT: SYSTEM INTELLIGENCE (Dashboard) ---
        self.dash_frame = ctk.CTkFrame(self.bg_frame, fg_color="transparent", corner_radius=0)
        self.dash_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.dash_frame.grid_columnconfigure(0, weight=1)

        # Neural Core Visualization
        self.core_frame = ctk.CTkFrame(self.dash_frame, fg_color="#0a0a0b", corner_radius=25, border_width=1, border_color="#1a1a1c")
        self.core_frame.grid(row=0, column=0, sticky="ew", pady=(10, 20))
        
        self.core_canvas = ctk.CTkCanvas(self.core_frame, width=300, height=300, bg="#0a0a0b", highlightthickness=0)
        self.core_canvas.pack(pady=20)
        self.load_neural_core()

        self.prime_status = ctk.CTkLabel(self.core_frame, text="SYSTEM STABLE", font=ctk.CTkFont(size=12, weight="bold", family="Orbitron"), text_color="#00d4ff")
        self.prime_status.pack(pady=(0, 20))

        # Telemetry Bento Box
        self.telemetry_bento = ctk.CTkFrame(self.dash_frame, fg_color="transparent")
        self.telemetry_bento.grid(row=1, column=0, sticky="nsew")
        self.telemetry_bento.grid_columnconfigure((0, 1), weight=1)

        self.cpu_card = self.create_bento_card(self.telemetry_bento, "CPU NODE", "0%", 0, 0)
        self.ram_card = self.create_bento_card(self.telemetry_bento, "RAM ARRAY", "0%", 0, 1)
        self.bat_card = self.create_bento_card(self.telemetry_bento, "ENERGY", "0%", 1, 0)
        self.net_card = self.create_bento_card(self.telemetry_bento, "UPLINK", "ACTIVE", 1, 1)

        # Neural Matrix Card
        self.matrix_card = ctk.CTkFrame(self.dash_frame, fg_color="#0a0a0b", corner_radius=20, border_width=1, border_color="#1a1a1c")
        self.matrix_card.grid(row=2, column=0, sticky="ew", pady=20)
        
        ctk.CTkLabel(self.matrix_card, text="NEURAL ARRAY SYNC", font=ctk.CTkFont(size=10, weight="bold", family="Orbitron"), text_color="#555555").pack(pady=(15, 5))
        
        self.matrix_grid = ctk.CTkFrame(self.matrix_card, fg_color="transparent")
        self.matrix_grid.pack(padx=20, pady=10, fill="x")
        self.matrix_grid.grid_columnconfigure((0, 1), weight=1)
        
        self.expansion_stats['vision'] = self.create_indicator(self.matrix_grid, "VISION", 0, 0)
        self.expansion_stats['research'] = self.create_indicator(self.matrix_grid, "SEARCH", 0, 1)
        self.expansion_stats['automation'] = self.create_indicator(self.matrix_grid, "SYSTEM", 1, 0)
        self.expansion_stats['art'] = self.create_indicator(self.matrix_grid, "ART", 1, 1)

        # Real-time Monologue Feeder
        self.monologue_frame = ctk.CTkFrame(self.dash_frame, fg_color="#070708", corner_radius=15, height=150)
        self.monologue_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        self.monologue_frame.pack_propagate(False)
        
        self.monologue_label = ctk.CTkLabel(self.monologue_frame, text="INTERNAL TELEMETRY FEED", font=ctk.CTkFont(size=9, weight="bold"), text_color="#333333")
        self.monologue_label.pack(pady=5)
        
        self.monologue_text = ctk.CTkTextbox(self.monologue_frame, fg_color="transparent", font=ctk.CTkFont(size=10, family="Consolas"), text_color="#005555")
        self.monologue_text.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_telemetry("Neural Interface initialized successfully.")

    def create_bento_card(self, parent, title, value, r, c):
        card = ctk.CTkFrame(parent, fg_color="#0a0a0b", corner_radius=15, border_width=1, border_color="#1a1a1c", height=100)
        card.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
        card.grid_propagate(False)
        
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=9, weight="bold"), text_color="#555555").pack(pady=(12, 0))
        val_lbl = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=18, weight="bold"), text_color="#ffffff")
        val_lbl.pack(pady=(2, 5))
        
        # Subtle progress line at bottom
        line = ctk.CTkFrame(card, height=2, fg_color="#00d4ff", width=60)
        line.pack(pady=(0, 10))
        return val_lbl

    def create_indicator(self, parent, name, r, c):
        lbl = ctk.CTkLabel(parent, text=f"• {name}", font=ctk.CTkFont(size=9, weight="bold"), text_color="#333333")
        lbl.grid(row=r, column=c, padx=10, pady=5, sticky="w")
        return lbl

    def load_neural_core(self):
        try:
            core_path = os.path.join(os.path.dirname(__file__), "Graphics", "neural_core.png")
            if os.path.exists(core_path):
                self.core_img_base = Image.open(core_path).convert("RGBA")
                self.update_core_image()
            else:
                self.log_telemetry("Core Graphic missing, using Placeholder.")
                # Create a simple glowing sphere if image is missing
                self.core_img_base = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
                self.update_core_image()
        except Exception as e:
            self.log_telemetry(f"Core Graphic Initialization Error: {e}")
            self.core_img_base = Image.new("RGBA", (300, 300), (10, 10, 12, 255))

    def update_core_image(self):
        if not hasattr(self, 'core_img_base'): return
        size = int(300 * self.core_zoom)
        resized = self.core_img_base.resize((size, size), Image.Resampling.LANCZOS)
        self.core_tk = ImageTk.PhotoImage(resized)
        self.core_canvas.delete("all")
        self.core_canvas.create_image(150, 150, image=self.core_tk)

    def log_telemetry(self, text):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.monologue_text.insert("end", f"[{ts}] {text.upper()}\n")
        self.monologue_text.see("end")

    # --- System Logic ---
    def lazy_import_backend(self):
        if not self.backend_loaded:
            try:
                self.update_status("SYNCING KERNEL")
                self.log_telemetry("Accessing kernel arrays...")
                
                global ChatBot, FirstLayerDMM, get_system_stats, start_scheduler, add_task
                from Backend.Chatbot import ChatBot
                from Backend.Model import FirstLayerDMM
                from Backend.SystemHealth import get_system_stats
                from Backend.Scheduler import start_scheduler, add_task
                
                start_scheduler(lambda t: self.chat_widget.add_complete_message("system", f"⏰ REMINDER: {t}"))
                self.log_telemetry("Temporal scheduler online.")

                global SpeechRecognition, QueryModifier, UniversalTranslator, text_to_speech
                from Backend.SpeechToText import SpeechRecognition, QueryModifier, UniversalTranslator
                from Backend.TextToSpeech import text_to_speech

                self.backend_loaded = True
                self.update_status("STABLE")
                self.log_telemetry("Neuro-linguistic link established.")
                
                if self.wake_word_active and not self.speech_thread:
                    self.speech_thread = threading.Thread(target=self.speech_recognition_loop, daemon=True)
                    self.speech_thread.start()
            except Exception as e:
                self.update_status("BRAIN ERROR")
                self.log_telemetry(f"Critical link failure: {e}")
                self.chat_widget.add_complete_message("error", f"Neural Link Failure: {e}")

    def ensure_expansion(self, pack_name):
        if pack_name in self.loaded_modules:
            self.module_last_used[pack_name] = time.time()
            return True
        
        with self.loading_lock:
            if pack_name in self.loaded_modules: return True
            
            try:
                self.update_status(f"SYNCING {pack_name}")
                self.log_telemetry(f"Initializing {pack_name} neural expansion...")
                
                if pack_name in self.expansion_stats:
                    self.expansion_stats[pack_name].configure(text_color="#ffcc00") 
                
                if pack_name == "vision":
                    from Backend.Vision import analyze_screen
                    globals()["analyze_screen"] = analyze_screen
                elif pack_name == "automation":
                    from Backend.Automation import Automation
                    globals()["Automation"] = Automation
                elif pack_name == "code":
                    from Backend.CodeInterpreter import dynamic_agent
                    globals()["dynamic_agent"] = dynamic_agent
                elif pack_name == "research":
                    from Backend.RealtimeSearchEngine import RealtimeSearchEngine
                    globals()["RealtimeSearchEngine"] = RealtimeSearchEngine
                elif pack_name == "art":
                    from Backend.ImageGeneration import GenerateImages
                    globals()["GenerateImages"] = GenerateImages
                
                self.loaded_modules.add(pack_name)
                self.module_last_used[pack_name] = time.time()
                
                if pack_name in self.expansion_stats:
                    mem = self.module_memory_map.get(pack_name, 0)
                    self.expansion_stats[pack_name].configure(text=f"• {pack_name.upper()} [{mem}MB]", text_color="#00d4ff")
                
                self.log_telemetry(f"{pack_name.upper()} array synchronized.")
                self.update_status("STABLE")
                return True
            except Exception as e:
                self.log_telemetry(f"Array fault in {pack_name}: {e}")
                if pack_name in self.expansion_stats:
                    self.expansion_stats[pack_name].configure(text_color="#ff4444")
                return False

    def neural_resource_monitor(self):
        while not self.stop_speech_event.is_set():
            time.sleep(60)
            now = time.time()
            for pack, last_used in list(self.module_last_used.items()):
                if pack in self.loaded_modules and (now - last_used) > 600:
                    self.loaded_modules.remove(pack)
                    self.root.after(0, lambda p=pack: self.expansion_stats[p].configure(text=f"• {p.upper()}", text_color="#333333"))
                    self.log_telemetry(f"{pack.upper()} entering hibernation.")

    def predictive_preheat(self, event=None):
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

    def animate_ui(self):
        # Neural Core Pulsation
        pulse_speed = 0.005 if self.is_mic_on else 0.002
        if self.core_direction == 1:
            self.core_zoom += pulse_speed
            if self.core_zoom >= 1.05: self.core_direction = -1
        else:
            self.core_zoom -= pulse_speed
            if self.core_zoom <= 0.95: self.core_direction = 1
        
        self.update_core_image()

        # Dynamic Status Color
        if self.is_mic_on:
            colors = ["#00d4ff", "#ff00ff", "#ffffff"]
            target = colors[int(time.time() * 2) % len(colors)]
            self.prime_status.configure(text_color=target)
        else:
            self.prime_status.configure(text_color="#00d4ff")

        self.root.after(30, self.animate_ui)

    def update_stats_loop(self):
        if self.backend_loaded:
            try:
                stats = get_system_stats()
                self.cpu_card.configure(text=stats['CPU'])
                self.ram_card.configure(text=stats['RAM'])
                self.bat_card.configure(text=stats['Battery'])
            except: pass
        self.root.after(3000, self.update_stats_loop)

    def update_status(self, text):
        self.prime_status.configure(text=text.upper())

    # --- Interaction Logic ---
    def handle_text_input(self, event=None):
        query = self.input_entry.get().strip()
        if not query: return
        self.input_entry.delete(0, tk.END)
        self.chat_widget.add_complete_message("user", query)
        self.log_telemetry(f"Processing command: {query}")
        threading.Thread(target=self.process_query_task, args=(query,), daemon=True).start()

    def process_query_task(self, query):
        if not self.backend_loaded: return
        self.root.after(0, self.typing_indicator.show)
        
        try:
            commands = FirstLayerDMM(query)
            responses = []
            
            for cmd in commands:
                self.log_telemetry(f"Executing: {cmd}")
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
                        # Use global analyze_screen
                        res = globals()["analyze_screen"](cmd.removeprefix("vision "))
                        self.stream_response(f"SURVEILLANCE DATA: {res}")
                        responses.append(res)
                elif cmd.startswith("complex "):
                    if self.ensure_expansion("code"):
                        res = globals()["dynamic_agent"](cmd.removeprefix("complex "))
                        self.stream_response(res)
                        responses.append(res)
                elif cmd.startswith("generate image "):
                    if self.ensure_expansion("art"):
                        globals()["GenerateImages"](cmd.removeprefix("generate image "))
                        self.chat_widget.add_complete_message("assistant", "SYNTHESIZED ART RENDERED SUCCESSFULLY.")
                elif cmd.startswith(("open ", "close ", "play ", "system ", "google search ")):
                    if self.ensure_expansion("automation"):
                        asyncio.run(globals()["Automation"]([cmd]))
                        self.chat_widget.add_complete_message("system", f"AUTOMATION SUCCESS: {cmd}")
            
            if responses and "text_to_speech" in globals():
                threading.Thread(target=globals()["text_to_speech"], args=("\n".join(responses),), daemon=True).start()
            
            self.root.after(0, self.typing_indicator.hide)
            self.log_telemetry("Directive complete.")
        except Exception as e:
            self.log_telemetry(f"Execution error: {e}")
            self.chat_widget.add_complete_message("error", f"Neural Execution Error: {e}")
            self.root.after(0, self.typing_indicator.hide)

    def stream_response(self, text):
        self.root.after(0, lambda: self.chat_widget.start_streaming("assistant"))
        words = text.split()
        for word in words:
            self.root.after(0, lambda w=word: self.chat_widget.add_text(w + " ", 0.02))
            time.sleep(0.02)
        self.root.after(0, self.chat_widget.finish_streaming)

    def toggle_microphone(self):
        if not self.is_mic_on:
            self.is_mic_on = True
            self.mic_prime.configure(fg_color="#ff004c", text="🛑")
            self.log_telemetry("Microphone array active. Listening...")
            # Use self.waveform
        else:
            self.is_mic_on = False
            self.mic_prime.configure(fg_color="#1a1a1c", text="🎤")
            self.log_telemetry("Microphone array disconnected.")

    def speech_recognition_loop(self):
        while not self.stop_speech_event.is_set():
            if not self.backend_loaded:
                time.sleep(1)
                continue
            try:
                # Use global SpeechRecognition
                from Backend.SpeechToText import SpeechRecognition
                text = SpeechRecognition()
                if text and not text.startswith("[") and text.strip():
                    if not self.is_mic_on and self.wake_word in text.lower():
                        self.root.after(0, self.toggle_microphone)
                    elif self.is_mic_on:
                        from Backend.SpeechToText import UniversalTranslator
                        if UniversalTranslator: text = UniversalTranslator(text)
                        self.root.after(0, lambda t=text: self.handle_voice_input(t))
                        self.root.after(2000, self.toggle_microphone)
            except: pass
            time.sleep(0.1)

    def handle_voice_input(self, text):
        self.chat_widget.add_complete_message("user", f"🎤 {text}")
        threading.Thread(target=self.process_query_task, args=(text,), daemon=True).start()

    def on_closing(self):
        self.stop_speech_event.set()
        # root.destroy() is handled by main.py after cleanup