import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox
import datetime
import threading
import queue

class VoiceRecorder:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_recording = False
        self.is_paused = False
        self.audio_queue = queue.Queue()
        self.recorded_text = []
        
    def start_recording(self):
        try:
            # Test microphone access
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Microphone initialized successfully")
        except Exception as e:
            error_msg = f"Error accessing microphone: {str(e)}"
            print(error_msg)
            messagebox.showerror("Microphone Error", error_msg)
            return False
            
        self.is_recording = True
        self.is_paused = False
        self.recorded_text = []
        threading.Thread(target=self._record_audio, daemon=True).start()
        return True
        
    def stop_recording(self):
        self.is_recording = False
        self.is_paused = False
        
    def pause_recording(self):
        self.is_paused = not self.is_paused
        return self.is_paused
        
    def _record_audio(self):
        try:
            with sr.Microphone() as source:
                print("Starting recording thread")
                while self.is_recording:
                    if not self.is_paused:
                        try:
                            print("Listening...")
                            audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                            print("Audio captured, processing...")
                            self.audio_queue.put(audio)
                            threading.Thread(target=self._process_audio, daemon=True).start()
                        except sr.WaitTimeoutError:
                            continue
                        except Exception as e:
                            print(f"Error during recording: {e}")
                            status_label.config(text=f"Error: {str(e)}", fg="red")
        except Exception as e:
            print(f"Fatal error in recording thread: {e}")
            status_label.config(text=f"Fatal error: {str(e)}", fg="red")
                        
    def _process_audio(self):
        try:
            audio = self.audio_queue.get()
            print("Processing audio...")
            text = self.recognizer.recognize_google(audio, language="en-IN")
            print(f"Recognized text: {text}")
            self.recorded_text.append(text)
            status_label.config(text=f"Recording... ({len(self.recorded_text)} segments)", fg="blue")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
            status_label.config(text="Network error ⚠️", fg="red")
        except Exception as e:
            print(f"Error processing audio: {e}")
            status_label.config(text=f"Error: {str(e)}", fg="red")

def start_recording():
    if recorder.start_recording():
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        pause_button.config(state=tk.NORMAL)
        status_label.config(text="Recording... 🎤", fg="blue")

def stop_recording():
    recorder.stop_recording()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    pause_button.config(state=tk.DISABLED)
    
    # Save the recorded text
    if recorder.recorded_text:
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"note_{now}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(" ".join(recorder.recorded_text))
        status_label.config(text=f"Note saved as {filename} ✅", fg="green")
        messagebox.showinfo("Success", f"Note saved as:\n{filename}")
    else:
        status_label.config(text="No audio recorded ❌", fg="red")

def toggle_pause():
    is_paused = recorder.pause_recording()
    if is_paused:
        pause_button.config(text="▶️ Resume")
        status_label.config(text="Recording paused ⏸️", fg="orange")
    else:
        pause_button.config(text="⏸️ Pause")
        status_label.config(text="Recording... 🎤", fg="blue")

# GUI Setup
window = tk.Tk()
window.title("Voice to Text Note App")
window.geometry("400x250")
window.configure(bg="#f2f2f2")

label = tk.Label(window, text="🎙️ Voice Note Recorder", font=("Arial", 14), bg="#f2f2f2")
label.pack(pady=20)

button_frame = tk.Frame(window, bg="#f2f2f2")
button_frame.pack(pady=10)

recorder = VoiceRecorder()

start_button = tk.Button(button_frame, text="🎤 Start Recording", font=("Arial", 12), 
                        command=start_recording, bg="#4CAF50", fg="white", padx=10, pady=5)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="⏹️ Stop", font=("Arial", 12),
                       command=stop_recording, bg="#f44336", fg="white", padx=10, pady=5,
                       state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=5)

pause_button = tk.Button(button_frame, text="⏸️ Pause", font=("Arial", 12),
                        command=toggle_pause, bg="#FFA500", fg="white", padx=10, pady=5,
                        state=tk.DISABLED)
pause_button.pack(side=tk.LEFT, padx=5)

status_label = tk.Label(window, text="", font=("Arial", 12), bg="#f2f2f2")
status_label.pack(pady=20)

window.mainloop()