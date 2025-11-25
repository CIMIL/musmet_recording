import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading

class RCController:
    def __init__(self, root):
        self.root = root
        self.root.title("RC Controller")
        self.running = False
        self.port = 22345  # Default port from your example
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # IP Address inputs
        self.ip_entries = []
        for i in range(4):
            frame = ttk.Frame(self.root)
            frame.grid(row=i, column=0, padx=5, pady=5, sticky='ew')
            
            ttk.Label(frame, text=f"Device {i+1} IP:").pack(side='left')
            ip_entry = ttk.Entry(frame, width=35)
            ip_entry.pack(side='left', padx=5)
            ip_entry.insert(0, "localhost")  # Default value
            self.ip_entries.append(ip_entry)
            
            # Test button for individual devices
            # ttk.Button(frame, text="Test", 
            #           command=lambda idx=i: self.test_connection(idx)).pack(side='left', padx=5)

        # Control buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=4, column=0, pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="Start All", command=self.start_all)
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="Stop All", 
                                 command=self.stop_all, state=tk.DISABLED)
        self.stop_btn.pack(side='left', padx=5)

        # Status bar
        self.status_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.status_var, 
                relief='sunken', anchor='w').grid(row=5, column=0, sticky='ew')

        # Configure grid
        self.root.columnconfigure(0, weight=1)
        
    def send_command(self, ip, command):
        """Threaded command sender with error handling"""
        try:
            with socket.create_connection((ip, self.port), timeout=2) as s:
                s.sendall(f"{command}\n".encode())
                return True
        except Exception as e:
            self.status_var.set(f"Error connecting to {ip}: {str(e)}")
            return False

    def test_connection(self, idx):
        """Test individual device connection"""
        ip = self.ip_entries[idx].get()
        if self.send_command(ip, "ping"):
            messagebox.showinfo("Success", f"{ip} responded successfully!")

    def start_all(self):
        """Start all devices"""
        self.running = True
        self.start_btn['state'] = tk.DISABLED
        self.stop_btn['state'] = tk.NORMAL
        self.status_var.set("Starting devices...")
        
        for idx, entry in enumerate(self.ip_entries):
            ip = entry.get()
            threading.Thread(
                target=self.send_command,
                args=(ip, "start"),
                daemon=True
            ).start()

    def stop_all(self):
        """Stop all devices"""
        self.running = False
        self.stop_btn['state'] = tk.DISABLED
        self.start_btn['state'] = tk.NORMAL
        self.status_var.set("Stopping devices...")
        
        for idx, entry in enumerate(self.ip_entries):
            ip = entry.get()
            threading.Thread(
                target=self.send_command,
                args=(ip, "stop"),
                daemon=True
            ).start()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x250")
    app = RCController(root)
    root.mainloop()
