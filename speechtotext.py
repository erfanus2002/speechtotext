import tkinter as tk
from tkinter import filedialog, Text
import whisper
from pydub import AudioSegment
import threading
# Initialize Whisper model
model = whisper.load_model("base",download_root="assets")
# Function to convert audio to text
def convert_audio_to_text(audio_path):
    # Load audio file
    audio = AudioSegment.from_file(audio_path)
    audio.export("temp.wav", format="wav")
    
    # Transcribe audio file
    transcription = model.transcribe("temp.wav")
    return transcription['text']

# Function to handle file dialog and transcription
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.m4a")])
    if file_path:
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, "Transcribing...")
        text_output.update()
        
        # Start a new thread for transcription
        threading.Thread(target=transcribe_file, args=(file_path,)).start()

# Function to transcribe file in a separate thread
def transcribe_file(file_path):
    # Convert audio to text
    transcription = convert_audio_to_text(file_path)
    
    # Update the text output in the main thread
    text_output.after(0, display_transcription, transcription)

# Function to display transcription
def display_transcription(transcription):
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, transcription)

# Set up GUI
root = tk.Tk()
root.title("Audio to Text Converter")

canvas = tk.Canvas(root, height=400, width=600)
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=1, relheight=1)

open_file_button = tk.Button(frame, text="Open Audio File", padx=10, pady=5, fg="white", bg="#263D42", command=open_file)
open_file_button.pack()

text_output = Text(frame)
text_output.pack()

root.mainloop()
