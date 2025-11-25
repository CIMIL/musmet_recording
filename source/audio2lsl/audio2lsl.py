import tkinter as tk
from tkinter import ttk
import soundcard as sc
import pylsl
import threading
import pythoncom
import wave
import numpy as np
import os
import sys
import socket

class AudioStreamGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LSL Audio Streamer")
        self.running = False
        self.audio_final = []
        
        # Create GUI elements
        self.create_widgets()
        
        # Get available microphones
        self.mics = sc.all_microphones()
        self.mic_names = [str(mic) for mic in self.mics]
        self.source_combobox['values'] = self.mic_names
        
    def create_widgets(self):
        # Source selection
        ttk.Label(self.root, text="Input Source:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.source_combobox = ttk.Combobox(self.root, state="readonly")
        self.source_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Filename entry
        ttk.Label(self.root, text="Filename:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.filename_entry = ttk.Entry(self.root)
        self.filename_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Control buttons
        self.start_btn = ttk.Button(self.root, text="Start Stream", command=self.start_streaming)
        self.start_btn.grid(row=2, column=0, padx=5, pady=5)
        
        self.stop_btn = ttk.Button(self.root, text="Stop Stream", command=self.stop_streaming, state=tk.DISABLED)
        self.stop_btn.grid(row=2, column=1, padx=5, pady=5)
        
        # Configure grid
        self.root.columnconfigure(1, weight=1)
        
    def start_streaming(self):
        
        selected_mic = self.source_combobox.current()
        filename = self.filename_entry.get()
        
        if selected_mic == -1:
            tk.messagebox.showerror("Error", "Please select an input source")
            return
        if not filename:
            tk.messagebox.showerror("Error", "Please enter a filename")
            return
            
        self.running = True
        self.start_btn['state'] = tk.DISABLED
        self.stop_btn['state'] = tk.NORMAL
        
        # Start streaming in separate thread
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

        if self.stream_thread.is_alive():
            self.stream_thread.join(timeout=2)

        self.save_wav()


    
    def stream_audio(self, microphone, filename):
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)  

        actual_rate = microphone.speaker.samplerate if hasattr(microphone, 'speaker') else 48000
        sampling_rate = 48000
        channels = microphone.channels


        print(actual_rate)
        chunk_size = 1024

        # Create LSL stream info
        info = pylsl.StreamInfo(
            name=socket.gethostname()+'-AudioStream',
            type='Audio',
            channel_count=channels,
            nominal_srate=sampling_rate,
            channel_format='float32',
            source_id='soundcard_audio_stream'
        )
        
        # Create LSL outlet
        outlet = pylsl.StreamOutlet(info)
        
        # Start audio stream
        try:
            with microphone.recorder(samplerate=actual_rate) as mic:
                while self.running:
                    audio_data = mic.record(numframes=1024)
                    outlet.push_chunk(audio_data.tolist())
                    # outlet.push_chunk(audio_data)
                    self.audio_final.append(audio_data)

        finally:
            pythoncom.CoUninitialize()  # Cleanup COM [2][7]



    def save_wav(self):
        if not self.audio_final:
            return
            
        # Combine all chunks and convert to PCM-16
        full_audio = np.concatenate(self.audio_final)
        int16_audio = (full_audio * 32767).astype(np.int16)
        self.audio_final = []

        executable_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()

        if os.path.exists(executable_dir + '\\audio') == False:
            os.mkdir(executable_dir + '\\audio')

        channels = self.mics[self.source_combobox.current()].channels

        filename = executable_dir + '\\audio\\' + self.filename_entry.get() + '.wav'
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(48000)
            wav_file.writeframes(int16_audio.tobytes())



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x150")
    app = AudioStreamGUI(root)
    root.mainloop()

