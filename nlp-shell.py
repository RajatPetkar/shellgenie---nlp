import os
import sys
import json
import platform
import subprocess
import argparse
from typing import Optional, Dict, Any
import requests
import speech_recognition as sr
import pyttsx3


class ShellCommandConverter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.system = platform.system().lower()
        self.shell = self._detect_shell()
        
    def _detect_shell(self) -> str:
        if self.system == "windows":
            return "powershell"
        else:
            shell = os.environ.get('SHELL', '/bin/bash')
            if 'zsh' in shell:
                return "zsh"
            elif 'bash' in shell:
                return "bash"
            else:
                return "bash"  # default
    
    def _get_system_context(self) -> str:
        contexts = {
            "windows": "Windows PowerShell",
            "darwin": "macOS Terminal (Bash/Zsh)",
            "linux": "Linux Terminal (Bash/Zsh)"
        }
        return contexts.get(self.system, "Unix-like Terminal")
    
    def convert_to_command(self, natural_language: str) -> Optional[str]:
        system_prompt = f"""You are a shell command expert for {self._get_system_context()}.
Convert the user's natural language request into the appropriate shell command.

Rules:
1. Return ONLY the command, no explanations or formatting
2. Use commands appropriate for {self.shell} on {self.system}
3. For common tasks, use the most direct command
4. If the request is unclear, provide the most likely interpretation
5. Don't include dangerous commands (rm -rf, format, etc.)

Examples:
"what's my ip" -> "curl ifconfig.me" (Linux/Mac) or "Invoke-RestMethod ifconfig.me" (PowerShell)
"list files" -> "ls -la" (Linux/Mac) or "Get-ChildItem" (PowerShell)
"current directory" -> "pwd" (Linux/Mac) or "Get-Location" (PowerShell)
"disk usage" -> "df -h" (Linux/Mac) or "Get-PSDrive" (PowerShell)
"""

        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

        
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{system_prompt}\n\nUser request: {natural_language}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 100,
            }
        }
        
        try:
            response = requests.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and len(data['candidates']) > 0:
                    command = data['candidates'][0]['content']['parts'][0]['text'].strip()
                    # Clean up the response
                    command = command.replace('`', '').replace('```', '').strip()
                    return command
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def execute_command(self, command: str, confirm: bool = True) -> bool:
        """Execute the generated command with optional confirmation"""
        
        if confirm:
            print(f"Generated command: {command}")
            response = input("Execute this command? [y/N]: ").lower().strip()
            if response not in ['y', 'yes']:
                print("Command execution cancelled.")
                return False
        
        try:
            if self.system == "windows":
                result = subprocess.run(
                    ["powershell", "-Command", command],
                    capture_output=False,
                    text=True
                )
            else:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=False,
                    text=True
                )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Execution error: {e}")
            return False

def setup_config():
    """Setup configuration file for API key"""
    config_dir = os.path.expanduser("~/.nlp-shell")
    config_file = os.path.join(config_dir, "config.json")
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    if not os.path.exists(config_file):
        print("First time setup - please provide your Google Gemini API key.")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        api_key = input("Enter your Gemini API key: ").strip()
        
        config = {"gemini_api_key": api_key}
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Configuration saved to {config_file}")
        return api_key
    
    with open(config_file, 'r') as f:
        config = json.load(f)
        return config.get("gemini_api_key")
    
def speak(text: str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen() -> Optional[str]:
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎤 Listening... (Speak your shell request)")
        speak("I'm listening. Please say your command.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Recognition error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Convert natural language to shell commands using Gemini AI"
    )
    parser.add_argument(
        "query",
        nargs="*",
        help="Natural language query to convert to shell command"
    )
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Execute command without confirmation"
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Setup or reconfigure API key"
    )
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Use voice input and output"
    )

    args = parser.parse_args()

    if args.setup:
        setup_config()
        return

    api_key = setup_config()
    if not api_key:
        print("Error: No API key configured. Run with --setup to configure.")
        sys.exit(1)

    converter = ShellCommandConverter(api_key)

    try:
        while True:
            if args.query:
                query = " ".join(args.query)
                args.query = None  # clear after first use
            elif args.voice:
                speak("Listening for your command.")
                query = listen()
                if query.strip().lower() in ["exit", "quit", "stop"]:
                    speak("Exiting. Goodbye!")
                    break
            else:
                query = input("🗨️ Enter your command ('exit' to quit): ").strip()
                if query.lower() in ["exit", "quit"]:
                    print("👋 Exiting...")
                    break

            if not query:
                print("No query provided.")
                continue

            command = converter.convert_to_command(query)
            if command:
                print(f"🧠 AI Command: {command}")
                speak(f"Executing: {command}")
                converter.execute_command(command, confirm=False)
            else:
                speak("Sorry, I could not generate a command.")
                print("⚠️ Failed to generate command.")

    except KeyboardInterrupt:
        print("\n👋 Exiting on Ctrl+C...")
        speak("Exiting. Goodbye!")


if __name__ == "__main__":
    main()
    