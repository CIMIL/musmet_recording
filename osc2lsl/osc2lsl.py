import tkinter as tk
from tkinter import ttk
import pylsl
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
import threading
import socket

class OSC2LSLBridge:
    def __init__(self, root):
        self.root = root
        self.root.title("OSC to LSL Bridge")
        self.running = False
        self.outlet = None
        self.server = None
        
        # Create GUI elements
        self.create_widgets()
        
        # Get local IP
        self.ip_var.set(self.get_local_ip())
        
    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
        finally:
            s.close()

    def create_widgets(self):
        # IP Address
        ttk.Label(self.root, text="IP Address:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.ip_var = tk.StringVar()
        self.ip_entry = ttk.Entry(self.root, textvariable=self.ip_var)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Port
        ttk.Label(self.root, text="Port:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.port_var = tk.StringVar(value="9000")
        self.port_entry = ttk.Entry(self.root, textvariable=self.port_var)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Status
        self.status_var = tk.StringVar(value="Server Stopped")
        ttk.Label(self.root, textvariable=self.status_var).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Control buttons
        self.start_btn = ttk.Button(self.root, text="Start Server", command=self.start_server)
        self.start_btn.grid(row=3, column=0, padx=5, pady=5)
        
        self.stop_btn = ttk.Button(self.root, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_btn.grid(row=3, column=1, padx=5, pady=5)
        
        self.root.columnconfigure(1, weight=1)

    def osc_handler(self, address, *args):
        if self.outlet:
            try:
                # Convert OSC arguments to float array
                print((address, args))
                self.outlet.push_sample([f"{address} {args}"])
                # data = [float(arg) for arg in args]
                # self.outlet.push_sample(data)
                # print(data)
            except ValueError:
                print(f"Non-numeric OSC data received: {args}")

    def start_server(self):
        if self.running:
            return
            
        ip = self.ip_var.get()
        port = int(self.port_var.get())
        
        # Setup LSL stream
        info = pylsl.StreamInfo(
            name=socket.gethostname()+"-OSC2LSL",
            type="OSC",
            channel_count=1,
            channel_format="string",
            source_id=f"osc_{ip}:{port}"
        )
        self.outlet = pylsl.StreamOutlet(info)
        
        # Setup OSC server
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.osc_handler)
        
        ThreadingOSCUDPServer.allow_reuse_address = True
        self.server = ThreadingOSCUDPServer((ip, port), dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.running = True
        self.server_thread.start()
        
        self.status_var.set(f"Running on {ip}:{port}")
        self.start_btn['state'] = tk.DISABLED
        self.stop_btn['state'] = tk.NORMAL

    def stop_server(self):
        if self.running:
            self.server.shutdown()
            self.server.server_close()  
            self.server_thread.join()
            self.outlet = None
            self.running = False
            self.status_var.set("Server Stopped")
            self.start_btn['state'] = tk.NORMAL
            self.stop_btn['state'] = tk.DISABLED

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x150")
    app = OSC2LSLBridge(root)
    root.mainloop()
