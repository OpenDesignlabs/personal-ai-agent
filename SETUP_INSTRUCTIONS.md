# 🚀 Jarvis AI - Setup Instructions

## 📋 **How to Get Jarvis AI on GitHub**

Since GitHub is detecting API keys in the commit history, here's how to create a clean repository:

---

## 🔧 **Option 1: Create New Repository (Recommended)**

### **1. Create New Repository:**
1. Go to [GitHub.com](https://github.com)
2. Click **"New repository"**
3. **Repository name**: `jarvis-personal-ai`
4. **Description**: `Advanced AI Assistant with Voice Recognition`
5. **Public** or **Private** (your choice)
6. **❌ Don't** initialize with README, .gitignore, or license
7. Click **"Create repository"**

### **2. Push to New Repository:**
```bash
cd py
git remote set-url origin https://github.com/OpenDesignlabs/jarvis-personal-ai.git
git push -u origin main
```

---

## 🔧 **Option 2: Use GitHub Web Interface**

### **1. Create Repository:**
- Follow steps above to create a new repository

### **2. Upload Files:**
1. Click **"Add file"** → **"Upload files"**
2. Upload these files:
   - `README.md`
   - `jarvis.bat`
   - `.env.example`
   - `.gitignore`
   - `Requirements.txt`
   - `main.py`
   - `Backend/` folder (all files)
   - `Frontend/` folder (all files)

### **3. Commit Changes:**
- Add commit message: "🎉 Jarvis AI - Complete Personal Version"
- Click **"Commit changes"**

---

## 🔧 **Option 3: Use Existing Repository**

### **1. Remove API Keys from History:**
```bash
cd py
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch jarvisAI/.env' \
--prune-empty --tag-name-filter cat -- -- --all
```

### **2. Push Clean Version:**
```bash
git push origin main --force
```

---

## 📁 **Files to Include:**

### **✅ Essential Files:**
- `README.md` - Complete documentation
- `jarvis.bat` - Python 3.10 launcher
- `.env.example` - API keys template
- `.gitignore` - Security rules
- `Requirements.txt` - Dependencies
- `main.py` - Main application

### **✅ Backend Files:**
- `Backend/Chatbot.py` - AI chat integration
- `Backend/Model.py` - Decision making
- `Backend/Automation.py` - System control
- `Backend/SpeechToText.py` - Voice recognition
- `Backend/TextToSpeech.py` - Voice synthesis
- `Backend/ImageGeneration.py` - AI images
- `Backend/RealtimeSearchEngine.py` - Web search

### **✅ Frontend Files:**
- `Frontend/GUI.py` - Classic interface
- `Frontend/GUI_Modern.py` - Modern interface
- `Frontend/streaming_text.py` - Real-time text
- `Frontend/voice_waveform.py` - Voice visualization
- `Frontend/Graphics/` - UI assets

### **❌ Files to Exclude:**
- `.env` - Contains real API keys
- `jarvis.log` - Log files
- `__pycache__/` - Python cache
- `Data/ChatLog.json` - Chat history

---

## 🚀 **After Repository Setup:**

### **For Users:**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/OpenDesignlabs/jarvis-personal-ai.git
   cd jarvis-personal-ai
   ```

2. **Setup Environment**:
   ```bash
   cp jarvisAI/.env.example jarvisAI/.env
   # Edit jarvisAI/.env with your API keys
   ```

3. **Install Dependencies**:
   ```bash
   cd jarvisAI
   py -m pip install -r Requirements.txt
   ```

4. **Run Jarvis AI**:
   ```bash
   .\jarvis.bat
   ```

---

## 🔑 **API Keys Required:**

### **Get API Keys:**
- **Groq**: https://console.groq.com/
- **Cohere**: https://dashboard.cohere.com/
- **HuggingFace**: https://huggingface.co/settings/tokens
- **Gemini** (optional): https://makersuite.google.com/app/apikey

### **Add to .env:**
```env
GroqAPIKey = gsk_your_groq_key_here
CohereAPIKey = your_cohere_key_here
HuggingFaceAPIKey = hf_your_huggingface_key_here
GEMINI_API_KEY = your_gemini_key_here
Username = YourName
Assistantname = Jarvis
AssistantVoice = en-CA-LiamNeural
InputLanguage = en
```

---

## 🎯 **Features Working:**

### **✅ All Features:**
- 🤖 **AI Chat**: Groq API conversations
- 🎤 **Voice Recognition**: Whisper + PyAudio
- 🔊 **Text-to-Speech**: Edge TTS synthesis
- 🔍 **Real-time Search**: Google search
- 🖼️ **Image Generation**: HuggingFace AI
- ⚙️ **System Automation**: App control
- 🎨 **Modern GUI**: CustomTkinter interface

### **✅ Commands:**
- `"hello jarvis"` - Start conversation
- `"open notepad"` - Launch applications
- `"search python"` - Google search
- `"generate image of cat"` - Create AI images
- `"play music"` - Start music
- `"bye jarvis"` - Exit

---

## 🎊 **Final Status:**

**🎉 Your Jarvis AI is ready for GitHub!**

- ✅ **All features working**
- ✅ **Clean codebase**
- ✅ **Complete documentation**
- ✅ **Ready for sharing**
- ✅ **Professional setup**

**Choose any option above to get your Jarvis AI on GitHub!** 🚀
