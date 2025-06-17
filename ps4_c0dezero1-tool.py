import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os
import socket
import subprocess
import threading
from datetime import datetime

class PS4LuaTool:
    def __init__(self, root):
        self.root = root
        self.root.title("c0dezer01 ps4 lua tool")
        self.root.geometry("600x550")
        
        # Initialize variables
        self.ps4_ip = tk.StringVar(value="192.168.1.100")
        self.port1 = tk.StringVar(value="9026")
        self.port2 = tk.StringVar(value="9021")
        self.bin_file_path = tk.StringVar()
        
        # Check required files
        self.files_exist = self.check_required_files()
        
        # Create GUI elements
        self.create_widgets()
        
        # Disable buttons if files missing
        if not self.files_exist:
            self.btn_jailbreak.config(state=tk.DISABLED)
            self.btn_binloader.config(state=tk.DISABLED)
        
    def check_required_files(self):
        required_files = ["send_lua.py", "lapse.lua", "bin_loader.lua"]
        missing = [f for f in required_files if not os.path.exists(f)]
        
        if missing:
            self.log_output(f"ERROR: Missing required files: {', '.join(missing)}")
            self.log_output("Place all files in the same directory as this script")
            return False
        return True

    def create_widgets(self):
        # Create main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # IP and Port Configuration
        config_frame = tk.LabelFrame(main_frame, text="Connection Settings", padx=5, pady=5)
        config_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(config_frame, text="PS4 IP Address:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(config_frame, textvariable=self.ps4_ip, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(config_frame, text="Port 1 (LUA):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(config_frame, textvariable=self.port1, width=8).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(config_frame, text="Port 2 (Payload):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(config_frame, textvariable=self.port2, width=8).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Action Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.btn_jailbreak = tk.Button(button_frame, text="Send Jailbreak", command=self.send_jailbreak)
        self.btn_jailbreak.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        self.btn_binloader = tk.Button(button_frame, text="Send Binloader", command=self.send_binloader)
        self.btn_binloader.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        self.btn_select_bin = tk.Button(button_frame, text="Select Bin File", command=self.select_bin_file)
        self.btn_select_bin.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        self.btn_send_payload = tk.Button(button_frame, text="Send Payload", command=self.send_payload)
        self.btn_send_payload.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        # Selected File
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(file_frame, text="Selected Payload:").pack(side=tk.LEFT, padx=5, pady=5)
        tk.Label(file_frame, textvariable=self.bin_file_path, width=50, anchor="w").pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        # Output Console
        console_frame = tk.LabelFrame(main_frame, text="Output Console", padx=5, pady=5)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.console = scrolledtext.ScrolledText(
            console_frame, 
            wrap=tk.WORD, 
            state=tk.DISABLED,
            height=10
        )
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initial log
        self.log_output("c0dezer01 PS4 Lua Tool initialized")
        if self.files_exist:
            self.log_output("All required files found")
        else:
            self.log_output("ERROR: Some required files are missing")

    def log_output(self, message):
        """Append message to the output console with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, formatted_message + "\n")
        self.console.see(tk.END)  # Auto-scroll to bottom
        self.console.config(state=tk.DISABLED)

    def send_jailbreak(self):
        self.log_output("Sending Jailbreak (lapse.lua)...")
        threading.Thread(target=self._execute_command, args=("lapse.lua",)).start()

    def send_binloader(self):
        self.log_output("Sending Binloader (bin_loader.lua)...")
        threading.Thread(target=self._execute_command, args=("bin_loader.lua",)).start()

    def _execute_command(self, lua_file):
        """Execute LUA sending command and capture output"""
        self.status_var.set(f"Sending {lua_file}...")
        try:
            cmd = [
                "python", "send_lua.py",
                self.ps4_ip.get(),
                self.port1.get(),
                lua_file
            ]
            self.log_output(f"Executing: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            # Log output
            if result.stdout:
                self.log_output(result.stdout)
            if result.stderr:
                self.log_output(f"ERROR: {result.stderr}")
            
            self.status_var.set(f"Success: {lua_file} sent")
            self.log_output(f"{lua_file} sent successfully")
        except subprocess.CalledProcessError as e:
            error_msg = f"Command failed with code {e.returncode}: {e.stderr}"
            self.status_var.set(f"Error sending {lua_file}")
            self.log_output(f"ERROR: {error_msg}")
        except Exception as e:
            error_msg = str(e)
            self.status_var.set("Unexpected error")
            self.log_output(f"ERROR: {error_msg}")

    def select_bin_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Payload File",
            filetypes=(("BIN files", "*.bin"), ("All files", "*.*"))
        )
        if file_path:
            self.bin_file_path.set(os.path.basename(file_path))
            self.selected_bin = file_path
            self.log_output(f"Selected payload: {os.path.basename(file_path)}")

    def send_payload(self):
        if not hasattr(self, 'selected_bin'):
            messagebox.showwarning("No File", "Please select a BIN file first")
            return
            
        threading.Thread(target=self._send_bin).start()

    def _send_bin(self):
        """Send binary payload via socket"""
        self.status_var.set("Sending payload...")
        try:
            bin_file = os.path.basename(self.selected_bin)
            self.log_output(f"Sending payload: {bin_file}")
            
            # Read binary file
            with open(self.selected_bin, 'rb') as f:
                payload = f.read()
            
            file_size = len(payload)
            self.log_output(f"Payload size: {file_size} bytes")
            
            # Connect and send
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                self.log_output(f"Connecting to {self.ps4_ip.get()}:{self.port2.get()}...")
                s.connect((self.ps4_ip.get(), int(self.port2.get())))
                
                self.log_output("Connection established, sending payload...")
                s.sendall(payload)
            
            self.status_var.set("Payload sent successfully")
            self.log_output(f"Payload sent successfully: {bin_file}")
        except Exception as e:
            error_msg = str(e)
            self.status_var.set("Payload send failed")
            self.log_output(f"ERROR: {error_msg}")
            messagebox.showerror("Send Error", f"Failed to send payload:\n{error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PS4LuaTool(root)
    root.mainloop()