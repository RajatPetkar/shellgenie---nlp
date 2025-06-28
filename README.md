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

### ✅ Step-by-Step Terminal Setup for shellgenie
- ⚠️ Assumes you're on Windows and using Python 3.x (with py command available).

### 🧩 Step 1: Prepare Directory
- mkdir "$env:USERPROFILE\Scripts"
- copy "C:\Your\Path\To\nlp-shell.py" "$env:USERPROFILE\Scripts\nlp-shell.py"
- Replace the path if your script is elsewhere.

### 🧾 Step 2: Create a Batch Wrapper
- $batch = '@echo off
py "%USERPROFILE%\Scripts\nlp-shell.py" %*'
$batch | Out-File -FilePath "$env:USERPROFILE\Scripts\nlp.bat" -Encoding ascii

### 🛣️ Step 3: Add Scripts to PATH (if not already)

$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$env:USERPROFILE\Scripts*") {
    $newPath = "$currentPath;$env:USERPROFILE\Scripts"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "✅ Added to PATH. Please restart terminal."
}

### 🐍 Step 4: Ensure Python & Pip Work
Check if Python & Pip are available:
py --version
py -m ensurepip --upgrade

### 📦 Step 5: Install Python Dependencies
- py -m pip install requests speechrecognition pyttsx3
- If any of these fail, install pip first:
- py -m ensurepip --default-pip'
  
### ⚙️ Step 6: Run Initial Setup for API Key
- nlp --setup
- Enter your Gemini API key (from https://makersuite.google.com/app/apikey) when prompted.

### 🎤 Step 7: Run Voice or Text Commands
** Text mode:
- nlp "list all files"
  
** Voice mode:
- nlp --voice

- ✨ You can also use --no-confirm to skip prompt and auto-run the command.

🧪 Test It Works
Try saying or typing:
what's my ip
You should see the AI-generated shell command and hear it via voice.

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
