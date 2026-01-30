# 🤖 JARVIS PRIME - Elite Neural Interface

**🎉 A state-of-the-art autonomous AI system featuring predictive neural loading, multi-array sentient logic, and a high-fidelity Cyberpunk interface.**

---

## 🌟 **The Prime Evolution**

JARVIS PRIME is no longer just a chatbot; it is a sophisticated **Neural Command System**. Designed with "Tony Stark" levels of sophistication, Prime features real-time system awareness, a predictive "Pre-Heating" module system, and a dynamic resource manager that ensures your PC remains optimized while Jarvis runs in the background.

---

## 🚀 **Prime Neural Pillars**

### **🧠 Pillar I: Sentience Engine (Stark Protocol)**
- **Witty Professionalism**: Jarvis now communicates with the iconic polite, slightly dry, and sophisticated tone of a digital butler.
- **Sir/Ma'am Mode**: Intelligent addressing based on user profile.
- **Adaptive Sentiment**: Responses shift dynamically based on your current emotional state.

### **🌌 Pillar II: Neural Matrix UI**
- **Neural Array Status**: A real-time grid visualizing the health and status of Vision, Art, Research, and Automation modules.
- **Pulse Core**: A central interface element that pulses in sync with Jarvis's operations and shifts color based on active neural arrays.
- **Glassmorphism Design**: A premium, transparent Cyberpunk aesthetic built on CustomTkinter.

### **⚡ Pillar III: Predictive Resource Manager**
- **Predictive Pre-Heating**: Jarvis monitors your typing in real-time and begins loading heavy modules *before* you even hit Enter.
- **Idle Hibernation**: Non-essential arrays enter deep sleep after 10 minutes of inactivity to release system resources (RAM/CPU).
- **Background Sync**: Zero-hang interface—heavy libraries load on separate threads while you chat.

---

## 🛰️ **Core Expansion Packs**

- **👁️ Vision Array**: Real-time screen analysis and multimodal understanding.
- **🎨 Art Array**: Ultra-HD image generation via Stable Diffusion XL & HuggingFace.
- **🔍 Research Array**: Deep web scraping, citation-backed reporting, and real-time news extraction.
- **⚙️ System Array**: Full Windows automation, app control, and hardware hooks.
- **💻 Code Engine**: Autonomous script execution and self-healing logic.

---

## 📁 **Project Structure**

```
jarvisAI/
├── 📄 .env                    # Environment variables (API keys, settings)
├── 📄 .gitignore              # Git ignore rules
├── 📄 README.md                # This file
├── 📄 Requirements.txt          # Python dependencies
├── 📄 main.py                 # Main application entry point
├── 📄 jarvis.bat              # Windows launcher (Python 3.10)
│
├── 📂 Backend/                # AI and automation modules
│   ├── 🤖 Chatbot.py          # Groq AI chat integration
│   ├── 🧠 Model.py            # Decision making model
│   ├── 🔍 RealtimeSearchEngine.py  # Real-time web search
│   ├── 🖼️ ImageGeneration.py   # AI image generation
│   ├── 🎤 SpeechToText.py      # Speech recognition
│   ├── 🔊 TextToSpeech.py      # Text-to-speech synthesis
│   ├── ⚙️ Automation.py        # System automation
│   └── 📄 __init__.py
│
├── 🎨 Frontend/               # User interface components
│   ├── 🖼️ GUI.py              # Classic Tkinter interface
│   ├── 🎨 GUI_Modern.py         # Modern CustomTkinter interface
│   ├── 🎤 voice_waveform.py      # Voice visualization
│   ├── 💬 streaming_text.py     # Real-time text display
│   ├── 🖼️ Graphics/           # UI graphics and icons
│   └── 📄 __init__.py
│
└── 📂 Data/                  # Application data
    ├── 📝 ChatLog.json         # Chat history
    └── 🎵 speech.mp3            # Temporary audio files
```

---

## 🛠️ **Installation & Setup**

### **📋 Prerequisites**
- **Python 3.10.10** (recommended)
- **Windows OS** (primary platform)
- **Microphone** (for voice features)
- **Internet Connection** (for AI APIs)

### **🚀 Quick Start**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/OpenDesignlabs/jarvis.git
   cd jarvisAI
   ```

2. **Install dependencies**:
   ```bash
   py -m pip install -r Requirements.txt
   ```

3. **Configure API keys**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run Jarvis AI**:
   ```bash
   .\jarvis.bat
   ```

---

## 🔑 **Neural Link Configuration**

### **Primary Neural Keys:**

| Service | Variable | Purpose | Status |
|---------|-----------------|---------|---------|
| **Groq AI** | `GroqAPIKey` | Core Reasoning & Vision | Required |
| **Cohere AI** | `CohereAPIKey` | Decision Matrix (DMM) | Required |
| **Google Gemini** | `GEMINI_API_KEY` | High-Speed Logic (New SDK) | Required |
| **HuggingFace** | `HuggingFaceAPIKey` | Neural Art Engine | Required |

### **📡 System Telemetry (Sentience)**
Jarvis Prime is physically aware of your host environment. He monitors:
- **CPU Digital Fatigue**: Adapts tone and efficiency based on processor load.
- **RAM Allocation**: Actively unloads idle expansion packs to save memory.
- **Energy Reserve**: Adjusts interface brightness and background tasks based on battery levels (Sir/Ma'am).

---

## 🎯 **Usage Guide**

### **🎤 Voice Commands**
```bash
"hello jarvis"              # Start conversation
"what time is it?"          # Get current time
"open notepad"             # Launch Notepad
"search python tutorial"     # Google search
"generate image of a cat"    # Create AI image
"play music"               # Start music
"bye jarvis"               # Exit application
```

### **💬 Text Input**
- Type your message in the input field
- Press Enter or click "Send"
- Jarvis responds with AI-generated content

### **⚙️ System Control**
```bash
"open [application]"        # Launch application
"close [application]"       # Close application
"search [topic]"           # Google search
"volume up"               # Increase volume
"mute"                    # Mute system
```

---

## 🔧 **Technical Details**

### **🐍 Python Version**
- **Primary**: Python 3.10.10
- **Launcher**: `jarvis.bat` forces Python 3.10
- **Compatibility**: All packages tested with Python 3.10

### **📦 Neural Frameworks**
- **Core Engine**: `CustomTkinter`, `python-dotenv`, `google-genai`
- **Logic Matrix**: `groq`, `cohere`, `google-generativeai` (Migrated to `google-genai`)
- **Speech Array**: `pyaudio`, `pygame`, `edge-tts`, `openai-whisper`
- **Automation Kernel**: `AppOpener`, `pywhatkit`, `pyautogui`, `selenium`

### **🔌 Prime API Integrations**
- **Groq Llama 3.3**: The main neural processor for advanced reasoning.
- **Gemini 2.0/SDK**: High-speed secondary logic and multimodal analysis.
- **Cohere Command**: High-precision intent classification and decision mapping.
- **Semantic Neural Context**: Advanced long-term memory that synthesizes past user behavior into a cohesive context.
- **HuggingFace SDXL**: Professional-grade image synthesis kernel.

---

## 🎨 **Interface Options**

### **🖼️ Modern GUI (Default)**
- **Framework**: CustomTkinter
- **Features**: Dark/light themes, modern controls
- **Performance**: Optimized for smooth operation
- **Accessibility**: Enhanced visual feedback

### **🎨 Classic GUI (Fallback)**
- **Framework**: Standard Tkinter
- **Features**: Basic interface, reliable operation
- **Compatibility**: Works on all Python versions

---

## 🔍 **Troubleshooting**

### **❌ Common Issues**

#### **Voice Recognition Not Working**
```bash
# Check PyAudio installation
py -c "import pyaudio; print('PyAudio available')"

# Check microphone permissions
# Ensure microphone is connected and enabled
```

#### **Text-to-Speech Issues**
```bash
# Check internet connection
# Edge TTS requires internet connectivity
# Try reinstalling edge-tts
py -m pip install --upgrade edge-tts
```

#### **Application Won't Start**
```bash
# Use the batch file launcher
.\jarvis.bat

# Check Python version
py --version

# Verify dependencies
py -m pip list
```

### **🔧 Solutions**

#### **Python Version Issues**
- **Always use**: `.\jarvis.bat` (forces Python 3.10)
- **Avoid**: `python main.py` (may use Python 3.14)

#### **Missing Packages**
```bash
py -m pip install -r Requirements.txt
```

#### **API Key Problems**
```bash
# Verify .env file exists
# Check API key formats
# Ensure keys are valid and active
```

---

## 🤝 **Development**

### **🔧 Contributing**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### **📝 Reporting Issues**
1. Check existing issues first
2. Provide detailed error messages
3. Include system information
4. Steps to reproduce

### **🧪 Code Style**
- Follow PEP 8 guidelines
- Use descriptive variable names
- Add comments for complex logic
- Maintain consistent formatting

---

## 📄 **Documentation**

### **📖 Available Guides**
- **API_KEYS_STATUS.md**: API key configuration
- **ERRORS_FIXED.md**: Error resolution guide
- **FEATURES_GUIDE.md**: Feature breakdown

### **🔍 Configuration**
- **.env.example**: Environment variables template
- **SECURITY.md**: Security best practices
- **Requirements.txt**: Dependency list

---

## 🎊 **Project Status**

### **✅ Current Version**
- **Version**: 1.0.0
- **Status**: Stable and functional
- **Compatibility**: Python 3.10.10
- **Platform**: Windows (primary)

### **🚀 Upcoming Features**
- [ ] Mobile application
- [ ] Web interface
- [ ] Plugin system
- [ ] Multi-language support
- [ ] Cloud synchronization

---

## 📞 **Support**

### **🤝 Community**
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Join community discussions
- **Wiki**: Find additional documentation

### **📧 Technical Support**
- **Installation help**: Setup and configuration
- **API key issues**: Troubleshoot API connections
- **Feature requests**: Suggest new capabilities

---

## 📜 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🎯 **Acknowledgments**

### **🤖 AI Services**
- **Groq**: For conversational AI capabilities
- **Cohere**: For decision-making models
- **HuggingFace**: For image generation
- **Edge TTS**: For text-to-speech synthesis

### **🛠️ Libraries**
- **OpenAI Whisper**: For speech recognition
- **CustomTkinter**: For modern UI components
- **PyAudio**: For audio processing
- **Edge-TTS**: For voice synthesis
- **Selenium**: For web automation

---

## 🚀 **Getting Started**

**Ready to use Jarvis AI?**

1. **Run the launcher**: `.\jarvis.bat`
2. **Configure your API keys** in `.env`
3. **Start talking**: "Hello Jarvis!"
4. **Explore features**: Try voice commands and system control

**🎉 Welcome to Jarvis AI - Your intelligent assistant is ready to help!**

---

*Last updated: January 2026*
