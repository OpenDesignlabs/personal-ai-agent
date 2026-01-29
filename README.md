# 🤖 Jarvis AI - Advanced AI Assistant

**🎉 A powerful AI assistant with voice recognition, real-time search, image generation, and system automation capabilities.**

---

## 🌟 **Overview**

Jarvis AI is a sophisticated AI assistant that combines multiple AI models and services to provide a comprehensive conversational experience. Built with Python 3.10 for maximum compatibility, Jarvis AI features voice interaction, real-time web search, AI-powered image generation, and complete system automation.

---

## 🚀 **Key Features**

### **🎤 Voice Interaction**
- **Speech Recognition**: Whisper-powered voice input with PyAudio
- **Text-to-Speech**: Edge TTS for natural voice synthesis
- **Voice Commands**: Hands-free operation
- **Multi-language Support**: Universal translation capabilities

### **🤖 AI Capabilities**
- **Conversational AI**: Groq API for intelligent responses
- **Decision Making**: Cohere AI for command classification
- **Real-time Search**: Google search integration
- **Image Generation**: HuggingFace AI for visual content

### **⚙️ System Automation**
- **Application Control**: Open/close applications
- **Web Automation**: Browser control and interaction
- **System Commands**: Volume control, system operations
- **Content Creation**: Write code, essays, applications

### **🎨 Modern Interface**
- **CustomTkinter GUI**: Modern, responsive interface
- **Dark/Light Themes**: Customizable appearance
- **Real-time Status**: Live feedback and updates
- **Chat History**: Persistent conversation memory

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

## 🔑 **API Keys Configuration**

### **Required API Keys:**

| Service | API Key Variable | Purpose |
|---------|-----------------|---------|
| **Groq AI** | `GroqAPIKey` | Chat and conversation |
| **Cohere AI** | `CohereAPIKey` | Decision making |
| **HuggingFace** | `HuggingFaceAPIKey` | Image generation |

### **Optional API Keys:**
| Service | API Key Variable | Purpose |
|---------|-----------------|---------|
| **Google Gemini** | `GEMINI_API_KEY` | Additional AI model |

### **🔧 Setup Instructions:**
1. Copy `.env.example` to `.env`
2. Replace placeholder keys with your actual API keys
3. Ensure no spaces around the `=` sign

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

### **📦 Dependencies**
- **Core**: `tkinter`, `python-dotenv`, `requests`
- **AI**: `groq`, `cohere`, `openai-whisper`
- **Audio**: `pyaudio`, `pygame`, `edge-tts`
- **Web**: `selenium`, `webdriver-manager`, `beautifulsoup4`
- **Automation**: `AppOpener`, `pywhatkit`, `keyboard`

### **🔌 API Integrations**
- **Groq**: Llama 3.3-70B-Versatile model
- **Cohere**: Command classification
- **HuggingFace**: Stable Diffusion XL
- **Edge TTS**: Microsoft Edge text-to-speech
- **Google Search**: Real-time web search

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
