import threading
import time
import customtkinter as ctk

# Global variables for Username and Assistantname
Username = "User"
Assistantname = "Jarvis"

class StreamingTextWidget:
    def __init__(self, parent, width=800, height=200):
        self.parent = parent
        self.width = width
        self.height = height
        
        # Create scrollable frame for streaming text
        self.frame = ctk.CTkScrollableFrame(
            parent,
            width=width,
            height=height,
            corner_radius=8,
            fg_color="transparent"
        )
        
        # Current streaming message
        self.current_message = None
        self.current_label = None
        self.streaming_text = ""
        self.is_streaming = False
        
    def start_streaming(self, msg_type, prefix=""):
        """Start streaming a new message"""
        # Create new message frame
        self.current_message = ctk.CTkFrame(self.frame, corner_radius=8)
        self.current_message.grid(row=len(self.frame.winfo_children()), column=0, padx=5, pady=5, sticky="ew")
        self.current_message.grid_columnconfigure(0, weight=1)
        
        # Set color based on message type
        if msg_type == "user":
            fg_color = "#0078d7"
            text_color = "#ffffff"
        elif msg_type == "assistant":
            fg_color = "#28a745"
            text_color = "#ffffff"
        elif msg_type == "system":
            fg_color = "#6c757d"
            text_color = "#ffffff"
        else:  # error
            fg_color = "#dc3545"
            text_color = "#ffffff"
        
        # Create label for streaming text
        self.current_label = ctk.CTkLabel(
            self.current_message,
            text=prefix,
            font=ctk.CTkFont(size=12),
            fg_color=fg_color,
            text_color=text_color,
            corner_radius=8,
            wraplength=750,
            justify="left"
        )
        self.current_label.grid(row=0, column=0, padx=10, pady=8, sticky="ew")
        
        self.streaming_text = prefix
        self.is_streaming = True
        
        # Scroll to bottom
        self.frame._parent_canvas.yview_moveto(1.0)
        
    def add_text(self, text_chunk, delay=0.03):
        """Add a chunk of text to the streaming message"""
        if not self.is_streaming or not self.current_label:
            return
            
        self.streaming_text += text_chunk
        self.current_label.configure(text=self.streaming_text)
        
        # Scroll to bottom
        self.frame._parent_canvas.yview_moveto(1.0)
        
        # Small delay for typing effect
        time.sleep(delay)
        
    def finish_streaming(self):
        """Finish the current streaming message"""
        self.is_streaming = False
        self.current_message = None
        self.current_label = None
        self.streaming_text = ""
        
    def add_complete_message(self, msg_type, content):
        """Add a complete message without streaming"""
        message_frame = ctk.CTkFrame(self.frame, corner_radius=8)
        message_frame.grid(row=len(self.frame.winfo_children()), column=0, padx=5, pady=5, sticky="ew")
        message_frame.grid_columnconfigure(0, weight=1)
        
        # Set color based on message type
        if msg_type == "user":
            fg_color = "#0078d7"
            text_color = "#ffffff"
            prefix = f"👤 {Username}:"
        elif msg_type == "assistant":
            fg_color = "#28a745"
            text_color = "#ffffff"
            prefix = f"🤖 {Assistantname}:"
        elif msg_type == "system":
            fg_color = "#6c757d"
            text_color = "#ffffff"
            prefix = "ℹ️ System:"
        else:  # error
            fg_color = "#dc3545"
            text_color = "#ffffff"
            prefix = "❌ Error:"
        
        # Message content
        message_label = ctk.CTkLabel(
            message_frame,
            text=f"{prefix} {content}",
            font=ctk.CTkFont(size=12),
            fg_color=fg_color,
            text_color=text_color,
            corner_radius=8,
            wraplength=750,
            justify="left"
        )
        message_label.grid(row=0, column=0, padx=10, pady=8, sticky="ew")
        
        # Scroll to bottom
        self.frame._parent_canvas.yview_moveto(1.0)

class TypingIndicator:
    def __init__(self, parent):
        self.parent = parent
        self.is_visible = False
        self.dots = 0
        self.indicator_frame = None
        self.indicator_label = None
        self.animation_thread = None
        
    def show(self, message="AI is typing"):
        """Show typing indicator"""
        if self.is_visible:
            return
            
        self.is_visible = True
        
        # Create indicator frame
        self.indicator_frame = ctk.CTkFrame(self.parent, corner_radius=8)
        self.indicator_frame.grid(row=len(self.parent.winfo_children()), column=0, padx=5, pady=5, sticky="ew")
        self.indicator_frame.grid_columnconfigure(0, weight=1)
        
        # Create indicator label
        self.indicator_label = ctk.CTkLabel(
            self.indicator_frame,
            text=f"🤔 {message}...",
            font=ctk.CTkFont(size=12, slant="italic"),
            fg_color="#6c757d",
            text_color="#ffffff",
            corner_radius=8,
            wraplength=750,
            justify="left"
        )
        self.indicator_label.grid(row=0, column=0, padx=10, pady=8, sticky="ew")
        
        # Start animation
        self.animation_thread = threading.Thread(target=self._animate_dots, daemon=True)
        self.animation_thread.start()
        
        # Scroll to bottom
        self.parent._parent_canvas.yview_moveto(1.0)
        
    def hide(self):
        """Hide typing indicator"""
        if not self.is_visible:
            return
            
        self.is_visible = False
        
        # Remove indicator
        if self.indicator_frame:
            self.indicator_frame.destroy()
            self.indicator_frame = None
            self.indicator_label = None
            
    def _animate_dots(self):
        """Animate typing dots"""
        while self.is_visible:
            self.dots = (self.dots + 1) % 4
            dots_text = "." * self.dots
            
            if self.indicator_label:
                self.indicator_label.configure(text=f"🤔 AI is typing{dots_text}")
            
            time.sleep(0.5)
