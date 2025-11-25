import tkinter as tk
from tkinter import ttk, messagebox
import soundcard as sc
import pylsl
import threading
import numpy as np
from queue import Queue
import time

class AudioStreamGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Stream & Recorder")
        self.running = False
        self.status_queue = Queue()
        self.recorder = None
        self.writer = None
        
        self.create_widgets()
        self.check_status()
        
        self.mics = sc.all_microphones()
        self.mic_names = [str(mic) for mic in self.mics]
        self.source_combobox['values'] = self.mic_names

    def create_widgets(self):
        # Input Source
        ttk.Label(self.root, text="Input Source:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.source_combobox = ttk.Combobox(self.root, state="readonly")
        self.source_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Filename
        ttk.Label(self.root, text="Filename:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.filename_entry = ttk.Entry(self.root)
        self.filename_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Controls
        self.start_btn = ttk.Button(self.root, text="Start Stream", command=self.start_streaming)
        self.start_btn.grid(row=2, column=0, padx=5, pady=5)
        
        self.stop_btn = ttk.Button(self.root, text="Stop Stream", command=self.stop_streaming, state=tk.DISABLED)
        self.stop_btn.grid(row=2, column=1, padx=5, pady=5)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var, relief='sunken', anchor='w').grid(
            row=3, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        self.root.columnconfigure(1, weight=1)

    def check_status(self):
        while not self.status_queue.empty():
            message = self.status_queue.get()
            self.status_var.set(message)
        self.root.after(100, self.check_status)

    def start_streaming(self):
        selected_mic = self.source_combobox.current()
        filename = self.filename_entry.get()
        
        if selected_mic == -1:
            messagebox.showerror("Error", "Please select an input source")
            return
        if not filename:
            messagebox.showerror("Error", "Please enter a filename")
            return
            
        self.running = True
        self.start_btn['state'] = tk.DISABLED
        self.stop_btn['state'] = tk.NORMAL
        self.status_queue.put("Streaming...")
        
        self.stream_thread = threading.Thread(
            target=self.stream_audio,
            args=(self.mics[selected_mic], filename),
            daemon=True
        )
        self.stream_thread.start()

    def stop_streaming(self):
        self.running = False
        self.start_btn['state'] = tk.NORMAL
        self.stop_btn['state'] = tk.DISABLED
        self.status_queue.put("Finishing recording...")

    def stream_audio(self, microphone, filename):
        # Add .wav extension if missing
        if not filename.endswith('.wav'):
            filename += '.wav'
        
        # LSL Stream Setup
        info = pylsl.StreamInfo(
            name='AudioStream',
            type='Audio',
            channel_count=microphone.channels,
            nominal_srate=48000,
            channel_format='float32',
            source_id=filename
        )
        outlet = pylsl.StreamOutlet(info)
        
        # Create soundcard recorder with file output
        try:
            with microphone.recorder(samplerate=48000) as mic, \
                 sc.Writer(filename, samplerate=48000, channels=microphone.channels) as writer:
                
                self.status_queue.put(f"Recording to {filename}")
                while self.running:
                    audio_data = mic.record(numframes=1024)
                    outlet.push_chunk(audio_data.T.tolist())
                    writer.write(audio_data)
                
                self.status_queue.put(f"Saved: {filename}")
        except Exception as e:
            self.status_queue.put(f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x180")
    app = AudioStreamGUI(root)
    root.mainloop()
