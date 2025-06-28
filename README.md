# 🧞‍♂️ shellgenie

> ✨ *“Your wish is my command.”*  
Speak or type your intent — and ShellGenie turns it into an actual shell command using **AI**.

---

## 🚀 What is ShellGenie?

**ShellGenie** is a voice-enabled command-line tool that uses **Google Gemini AI** to convert natural language (spoken or typed) into executable shell commands.

No need to remember terminal syntax — just say it like a human.

---

## 🔥 Features

- 🗣️ **Voice input** (uses `speech_recognition`)
- 🤖 **AI-generated commands** via Google Gemini
- 💬 **Voice output** of the command (via `pyttsx3`)
- 🧠 Context-aware: understands your OS & shell
- ⚙️ Works on **PowerShell**, **Bash**, **Zsh**, and more
- 🚫 Optional confirmation before running commands
- 🗂️ Stores API key securely in your home directory

---

## 📦 Installation

### 1. Clone the repo
git clone https://github.com/your-username/shellgenie.git
cd shellgenie

### 2. Install required packages
pip install requests speechrecognition pyttsx3
ℹ️ If pip is missing, run:
py -m ensurepip --upgrade

### 3. Set up your API key
py nlp-shell.py --setup

### ⚡ Usage
👉 Text query (default mode)
py nlp-shell.py "show running processes"

🗣️ Voice mode
py nlp-shell.py --voice

✅ Skip confirmation
py nlp-shell.py "disk usage" --no-confirm

🔧 Reset API key
py nlp-shell.py --setup

### 💡 Examples
You Say or Type	ShellGenie Executes
what’s my IP	Invoke-RestMethod ifconfig.me
list all files	Get-ChildItem or ls -la
current directory	pwd or Get-Location
how much disk is used	df -h or Get-PSDrive

### 🧩 Flags
Flag	Description
--voice	Use voice input
--no-confirm	Auto-execute without asking confirmation
--setup	Set up or reset your Gemini API key

### ⚙️ How It Works
Listens to your voice or reads text

Sends it to Gemini API with shell + OS context

Parses the best shell command

Speaks it aloud and executes it (optionally asks first)

### 🧪 Tested Environments
✅ Windows 10/11 (PowerShell)

✅ Ubuntu/Linux (bash)

✅ macOS (zsh/bash)

✅ Python 3.10+

### 🧠 Future Ideas
1.Add Whisper or Vosk for offline voice recognition

2.Support multi-step command chains

3.Cross-platform desktop UI

4.Command history / learning from user usage

### 🤝 Contributing
Pull requests and issues are welcome! If you love voice interfaces, CLI tools, or AI — let’s build together.

### 📄 License
MIT License — use it freely, modify, and share with credits.

👨‍💻 Built with ❤️ by Rajat Petkar

Let me know if you'd like:
- A project badge section
- A cool logo or banner
- GitHub Pages documentation setup
