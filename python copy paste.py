import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import pyautogui
import time
import threading

class TextTyper:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Typer")
        
        self.text = ""
        self.typing = False
        
        self.load_button = tk.Button(root, text="Load TXT", command=self.load_text)
        self.load_button.pack(pady=10)
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=50)
        self.text_area.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Status: Waiting for cursor to be idle...")
        self.status_label.pack(pady=10)
        
    def load_text(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text = file.read()
            self.text_area.insert(tk.END, self.text)
            messagebox.showinfo("Info", "Text loaded successfully!")
            self.start_detection()
        
    def start_detection(self):
        threading.Thread(target=self.detect_cursor_idle).start()
    
    def detect_cursor_idle(self):
        while True:
            initial_pos = pyautogui.position()
            time.sleep(5) 
            current_pos = pyautogui.position()
            
            if initial_pos == current_pos: 
                self.status_label.config(text="Status: Typing started...")
                self.type_text()
                break
            else:
                self.status_label.config(text="Status: Waiting for cursor to be idle...")
    
    def type_text(self):
        self.typing = True
        for char in self.text:
            if not self.typing:
                break
            pyautogui.write(char)
            time.sleep(0.05)  
        self.status_label.config(text="Status: Typing completed.")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TextTyper(root)
    root.mainloop()
