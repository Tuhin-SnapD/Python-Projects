"""
Enhanced RoboTalker

A text-to-speech application with multiple TTS engines,
voice selection, and advanced features.
"""

import subprocess
import sys
import os
import time
import threading
from typing import List, Dict, Optional
from enum import Enum


class TTSEngine(Enum):
    """Available TTS engines."""
    WSAY = "wsay"
    PYTHON_TTS = "pyttsx3"
    GOOGLE_TTS = "gtts"
    FESTIVAL = "festival"


class RoboTalker:
    """Enhanced text-to-speech application."""
    
    def __init__(self):
        self.available_engines = self.detect_engines()
        self.current_engine = None
        self.voice_settings = {
            'rate': 150,
            'volume': 1.0,
            'voice': None
        }
        self.is_speaking = False
        
    def detect_engines(self) -> List[TTSEngine]:
        """Detect available TTS engines on the system."""
        available = []
        
        # Check wsay (Windows)
        if self.check_command("wsay"):
            available.append(TTSEngine.WSAY)
        
        # Check pyttsx3
        try:
            import pyttsx3
            available.append(TTSEngine.PYTHON_TTS)
        except ImportError:
            pass
        
        # Check gtts
        try:
            import gtts
            available.append(TTSEngine.GOOGLE_TTS)
        except ImportError:
            pass
        
        # Check festival (Linux)
        if self.check_command("festival"):
            available.append(TTSEngine.FESTIVAL)
        
        return available
    
    def check_command(self, command: str) -> bool:
        """Check if a command is available on the system."""
        try:
            subprocess.run([command, "--help"], 
                         capture_output=True, 
                         timeout=5, 
                         check=False)
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False
    
    def speak_with_wsay(self, text: str) -> bool:
        """Speak text using wsay engine."""
        try:
            subprocess.run(['wsay', text], check=True, timeout=30)
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"❌ wsay error: {e}")
            return False
    
    def speak_with_pyttsx3(self, text: str) -> bool:
        """Speak text using pyttsx3 engine."""
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            
            # Set voice properties
            engine.setProperty('rate', self.voice_settings['rate'])
            engine.setProperty('volume', self.voice_settings['volume'])
            
            if self.voice_settings['voice']:
                voices = engine.getProperty('voices')
                if voices and len(voices) > 0:
                    engine.setProperty('voice', voices[0].id)
            
            engine.say(text)
            engine.runAndWait()
            return True
            
        except Exception as e:
            print(f"❌ pyttsx3 error: {e}")
            return False
    
    def speak_with_gtts(self, text: str) -> bool:
        """Speak text using Google TTS engine."""
        try:
            from gtts import gTTS
            import tempfile
            import platform
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                temp_filename = tmp_file.name
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_filename)
            
            # Play the audio
            system = platform.system()
            if system == "Windows":
                os.startfile(temp_filename)
            elif system == "Darwin":  # macOS
                subprocess.run(['open', temp_filename])
            else:  # Linux
                subprocess.run(['xdg-open', temp_filename])
            
            # Wait a bit for playback
            time.sleep(len(text.split()) * 0.5)  # Rough estimate
            
            # Clean up
            try:
                os.unlink(temp_filename)
            except:
                pass
            
            return True
            
        except Exception as e:
            print(f"❌ Google TTS error: {e}")
            return False
    
    def speak_with_festival(self, text: str) -> bool:
        """Speak text using Festival engine."""
        try:
            subprocess.run(['festival', '--tts'], 
                         input=text.encode(), 
                         check=True, 
                         timeout=30)
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"❌ Festival error: {e}")
            return False
    
    def speak(self, text: str) -> bool:
        """Speak text using the current engine."""
        if not text.strip():
            return False
        
        if not self.current_engine:
            if self.available_engines:
                self.current_engine = self.available_engines[0]
            else:
                print("❌ No TTS engines available!")
                return False
        
        self.is_speaking = True
        
        try:
            if self.current_engine == TTSEngine.WSAY:
                return self.speak_with_wsay(text)
            elif self.current_engine == TTSEngine.PYTHON_TTS:
                return self.speak_with_pyttsx3(text)
            elif self.current_engine == TTSEngine.GOOGLE_TTS:
                return self.speak_with_gtts(text)
            elif self.current_engine == TTSEngine.FESTIVAL:
                return self.speak_with_festival(text)
            else:
                print(f"❌ Unknown engine: {self.current_engine}")
                return False
        finally:
            self.is_speaking = False
    
    def speak_async(self, text: str):
        """Speak text asynchronously."""
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.daemon = True
        thread.start()
    
    def set_voice_rate(self, rate: int):
        """Set the speech rate."""
        self.voice_settings['rate'] = max(50, min(300, rate))
    
    def set_voice_volume(self, volume: float):
        """Set the speech volume."""
        self.voice_settings['volume'] = max(0.0, min(1.0, volume))
    
    def list_voices(self):
        """List available voices for the current engine."""
        if self.current_engine == TTSEngine.PYTHON_TTS:
            try:
                import pyttsx3
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                
                print("\n🎤 Available Voices:")
                for i, voice in enumerate(voices):
                    print(f"{i+1}. {voice.name} ({voice.id})")
                    
            except Exception as e:
                print(f"❌ Error listing voices: {e}")
        else:
            print("Voice listing not supported for this engine.")
    
    def show_engine_info(self):
        """Show information about the current engine."""
        print(f"\n🔧 Current Engine: {self.current_engine.value}")
        print(f"Rate: {self.voice_settings['rate']}")
        print(f"Volume: {self.voice_settings['volume']}")
        print(f"Available engines: {[e.value for e in self.available_engines]}")
    
    def run_interactive(self):
        """Run the interactive RoboTalker interface."""
        print("🤖 ENHANCED ROBOTALKER")
        print("=" * 30)
        
        if not self.available_engines:
            print("❌ No TTS engines detected!")
            print("Please install one of the following:")
            print("- wsay (Windows): https://github.com/p-groarke/wsay")
            print("- pyttsx3: pip install pyttsx3")
            print("- gtts: pip install gtts")
            print("- festival (Linux): sudo apt-get install festival")
            return
        
        # Select engine
        print("Available TTS engines:")
        for i, engine in enumerate(self.available_engines, 1):
            print(f"{i}. {engine.value}")
        
        while True:
            try:
                choice = int(input(f"\nSelect engine (1-{len(self.available_engines)}): ")) - 1
                if 0 <= choice < len(self.available_engines):
                    self.current_engine = self.available_engines[choice]
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a valid number!")
        
        print(f"✅ Using engine: {self.current_engine.value}")
        
        # Main loop
        while True:
            try:
                print(f"\n💬 Enter text to speak (or 'help'/'quit'):")
                text = input("> ").strip()
                
                if text.lower() == 'quit':
                    self.speak("Goodbye! Thanks for using RoboTalker!")
                    print("👋 Goodbye!")
                    break
                elif text.lower() == 'help':
                    self.show_help()
                elif text.lower() == 'info':
                    self.show_engine_info()
                elif text.lower() == 'voices':
                    self.list_voices()
                elif text.lower() == 'rate':
                    self.set_rate_interactive()
                elif text.lower() == 'volume':
                    self.set_volume_interactive()
                elif text.lower() == 'engine':
                    self.change_engine()
                elif text:
                    print(f"🗣️  Speaking: {text}")
                    success = self.speak(text)
                    if not success:
                        print("❌ Failed to speak text!")
                else:
                    print("Please enter some text to speak.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 RoboTalker interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show help information."""
        print("\n📖 ROBOTALKER HELP")
        print("=" * 20)
        print("Commands:")
        print("- help: Show this help")
        print("- info: Show engine information")
        print("- voices: List available voices")
        print("- rate: Change speech rate")
        print("- volume: Change speech volume")
        print("- engine: Change TTS engine")
        print("- quit: Exit RoboTalker")
        print("\nJust type any text to have it spoken!")
    
    def set_rate_interactive(self):
        """Set speech rate interactively."""
        try:
            rate = int(input("Enter speech rate (50-300, default 150): ") or "150")
            self.set_voice_rate(rate)
            print(f"✅ Speech rate set to {rate}")
        except ValueError:
            print("❌ Invalid rate value!")
    
    def set_volume_interactive(self):
        """Set speech volume interactively."""
        try:
            volume = float(input("Enter volume (0.0-1.0, default 1.0): ") or "1.0")
            self.set_voice_volume(volume)
            print(f"✅ Volume set to {volume}")
        except ValueError:
            print("❌ Invalid volume value!")
    
    def change_engine(self):
        """Change TTS engine interactively."""
        print("Available engines:")
        for i, engine in enumerate(self.available_engines, 1):
            print(f"{i}. {engine.value}")
        
        try:
            choice = int(input(f"Select engine (1-{len(self.available_engines)}): ")) - 1
            if 0 <= choice < len(self.available_engines):
                self.current_engine = self.available_engines[choice]
                print(f"✅ Switched to {self.current_engine.value}")
            else:
                print("❌ Invalid choice!")
        except ValueError:
            print("❌ Please enter a valid number!")


def main():
    """Main function to start RoboTalker."""
    try:
        talker = RoboTalker()
        talker.run_interactive()
    except Exception as e:
        print(f"❌ Failed to start RoboTalker: {e}")


if __name__ == "__main__":
    main()
