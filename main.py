import tkinter as tk
from tkinter import ttk, messagebox

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Invisible Text Steganography")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#333")

        # --- Zero-Width Characters ---
        # We use these to encode the binary data invisible to the eye
        self.ZW_ZERO = '\u200b'  # Zero Width Space (Binary 0)
        self.ZW_ONE = '\u200c'   # Zero Width Non-Joiner (Binary 1)
        self.ZW_JOINER = '\u200d' # Zero Width Joiner (Start/End Marker)

        # Tabs
        tab_control = ttk.Notebook(root)
        self.tab_hide = ttk.Frame(tab_control)
        self.tab_reveal = ttk.Frame(tab_control)
        tab_control.add(self.tab_hide, text='  Hide Message  ')
        tab_control.add(self.tab_reveal, text='  Reveal Message  ')
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        self.setup_hide_tab()
        self.setup_reveal_tab()

    def setup_hide_tab(self):
        frame = ttk.Frame(self.tab_hide, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Hide a Secret", style="Header.TLabel").pack(pady=(0, 15))

        # Secret
        ttk.Label(frame, text="1. Secret Message (Emojis supported):").pack(anchor="w")
        self.secret_entry = tk.Entry(frame, width=50, font=("Segoe UI", 10))
        self.secret_entry.pack(fill="x", pady=(5, 15))

        # Cover
        ttk.Label(frame, text="2. Cover Text (Visible to everyone):").pack(anchor="w")
        self.cover_entry = tk.Entry(frame, width=50, font=("Segoe UI", 10))
        self.cover_entry.pack(fill="x", pady=(5, 15))

        # Button
        ttk.Button(frame, text="Hide Message Inside Text", command=self.hide_message).pack(pady=5)

        # Output
        ttk.Label(frame, text="Result (Copy this):").pack(anchor="w")
        self.hide_output = tk.Text(frame, height=5, font=("Segoe UI", 10), wrap="word")
        self.hide_output.pack(fill="x", pady=5)
        
        ttk.Button(frame, text="Copy Result to Clipboard", command=self.copy_to_clipboard).pack(pady=5)

    def setup_reveal_tab(self):
        frame = ttk.Frame(self.tab_reveal, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Reveal a Secret", style="Header.TLabel").pack(pady=(0, 15))

        # Input
        ttk.Label(frame, text="Paste the text containing hidden message:").pack(anchor="w")
        self.reveal_input = tk.Text(frame, height=6, font=("Segoe UI", 10), wrap="word")
        self.reveal_input.pack(fill="x", pady=(5, 15))

        # Button
        ttk.Button(frame, text="Reveal Hidden Message", command=self.reveal_message).pack(pady=5)

        # Output
        ttk.Label(frame, text="Hidden Message Found:").pack(anchor="w")
        self.reveal_output = tk.Entry(frame, font=("Segoe UI", 12, "bold"), fg="#2e7d32")
        self.reveal_output.pack(fill="x", pady=5)

    # --- Core Logic ---

    def str_to_binary(self, text):
        """Converts string to binary using UTF-8 encoding (supports emojis)."""
        # Encode to bytes first to handle special chars correctly
        bytes_data = text.encode('utf-8')
        # Convert bytes to a long string of bits
        binary_string = ''.join(format(byte, '08b') for byte in bytes_data)
        return binary_string

    def binary_to_str(self, binary_str):
        """Converts binary string back to text."""
        try:
            # Split into 8-bit chunks
            bytes_list = []
            for i in range(0, len(binary_str), 8):
                byte_chunk = binary_str[i:i+8]
                if len(byte_chunk) == 8:
                    bytes_list.append(int(byte_chunk, 2))
            
            # Convert list of integers back to bytes, then decode UTF-8
            return bytes(bytes_list).decode('utf-8', errors='replace')
        except Exception as e:
            return "Error decoding text."

    def hide_message(self):
        secret = self.secret_entry.get()
        cover = self.cover_entry.get()

        if not secret or not cover:
            messagebox.showwarning("Missing Info", "Please enter both secret and cover text.")
            return

        # 1. Convert secret to binary (UTF-8 safe)
        binary_secret = self.str_to_binary(secret)

        # 2. Convert to Zero-Width Chars
        hidden_payload = ""
        for bit in binary_secret:
            if bit == '0':
                hidden_payload += self.ZW_ZERO
            else:
                hidden_payload += self.ZW_ONE
        
        # 3. Inject: [JOINER] + [PAYLOAD] + [JOINER]
        # We put it after the first character of the cover text
        full_stego = self.ZW_JOINER + hidden_payload + self.ZW_JOINER
        
        if len(cover) > 0:
            final_text = cover[:1] + full_stego + cover[1:]
        else:
            final_text = full_stego

        # 4. Display Result
        self.hide_output.delete("1.0", tk.END)
        self.hide_output.insert("1.0", final_text)

    def reveal_message(self):
        # FIX: Use "end-1c" to avoid getting the extra newline Tkinter adds
        stego_text = self.reveal_input.get("1.0", "end-1c")
        
        extracted_binary = ""
        is_recording = False
        
        # Parse through the text to find the zero-width sandwich
        for char in stego_text:
            if char == self.ZW_JOINER:
                if not is_recording:
                    is_recording = True # Found Start
                else:
                    break # Found End
            elif is_recording:
                if char == self.ZW_ZERO:
                    extracted_binary += '0'
                elif char == self.ZW_ONE:
                    extracted_binary += '1'
        
        self.reveal_output.delete(0, tk.END)
        
        if extracted_binary:
            decoded_msg = self.binary_to_str(extracted_binary)
            self.reveal_output.insert(0, decoded_msg)
        else:
            self.reveal_output.insert(0, "No hidden message found.")

    def copy_to_clipboard(self):
        # FIX: Use "end-1c" to get EXACT text (prevents missing chars at boundaries)
        text = self.hide_output.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update() # Keeps clipboard available even if app closes
        messagebox.showinfo("Success", "Copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()