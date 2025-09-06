"""Simple Speech Recognition Tool - Main Application"""

import speech_recognition as sr
from datetime import datetime

class SimpleSpeechRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def calibrate(self):
        """Calibrate microphone for ambient noise"""
        print("🔧 Calibrating microphone...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Calibration complete!")
            return True
        except Exception as e:
            print(f"⚠️ Calibration failed: {e}")
            return False
    
    def listen_once(self):
        """Listen for speech and return recognized text"""
        try:
            with self.microphone as source:
                print("🎤 Listening... Speak now!")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("🔍 Processing...")
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.WaitTimeoutError:
            return "❌ Timeout - no speech detected"
        except sr.UnknownValueError:
            return "❌ Could not understand audio"
        except sr.RequestError as e:
            return f"❌ Recognition service error: {e}"
    
    def process_command(self, text):
        """Process recognized commands"""
        if text.startswith('❌'):
            return text
            
        text_lower = text.lower()
        
        if 'hello' in text_lower or 'hi' in text_lower:
            return "👋 Hello! Nice to meet you!"
        elif 'time' in text_lower:
            current_time = datetime.now().strftime("%H:%M:%S")
            return f"🕐 Current time: {current_time}"
        elif 'date' in text_lower:
            current_date = datetime.now().strftime("%B %d, %Y")
            return f"📅 Today's date: {current_date}"
        elif any(word in text_lower for word in ['exit', 'quit', 'stop']):
            return "👋 Goodbye!"
        else:
            return f"📝 You said: '{text}'"

def main():
    print("🎙️ Simple Speech Recognition Tool")
    print("=" * 40)
    
    speech = SimpleSpeechRecognition()
    
    
    speech.calibrate()
    
    print("\n💡 Available commands: hello, time, date, exit")
    print("🔄 Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Listen for speech
            recognized_text = speech.listen_once()
            print(f"🎯 Recognized: {recognized_text}")
            
            # Process command
            response = speech.process_command(recognized_text)
            print(f"🤖 Response: {response}")
            
            # Check for exit
            if 'goodbye' in response.lower():
                break
                
            print("-" * 30)
            
    except KeyboardInterrupt:
        print("\n👋 Program stopped by user")

if __name__ == "__main__":
    main()
