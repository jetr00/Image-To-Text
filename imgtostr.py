from PIL import Image
import pytesseract
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

# Tesseract path (edit for your's)
pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract.exe'

def guid():
    win = TkinterDnD.Tk()
    win.title("Image to Text")
    win.geometry("600x500")

    label = tk.Label(win, text="Drag and drop an image or enter path manually:", font=("Arial", 12))
    entry = tk.Entry(win, width=60)

    output_text = tk.Text(win, height=20, width=70, wrap="word")
    scroll = tk.Scrollbar(win, command=output_text.yview)
    output_text.config(yscrollcommand=scroll.set)

    def copy_to_clipboard():
        text = output_text.get(1.0, tk.END).strip()
        if text:
            win.clipboard_clear()
            win.clipboard_append(text)
            win.update() 
            
    def on_submit():
        img_path = entry.get().strip().strip('{').strip('}')
        try:
            text = pytesseract.image_to_string(Image.open(img_path))
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, text)

        except Exception as e:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Error: {e}")
            
        copy_button = tk.Button(win, text="Copy to Clipboard", command=copy_to_clipboard)
        copy_button.pack(pady=5)

    def on_drop(event):
        entry.delete(0, tk.END)
        entry.insert(0, event.data)
        on_submit()

    button = tk.Button(win, text="Extract Text", command=on_submit)

    win.bind('<Return>', lambda event: on_submit())
    entry.drop_target_register(DND_FILES)
    entry.dnd_bind('<<Drop>>', on_drop)

    button.pack(pady=5)
    label.pack(pady=(10, 5))
    entry.pack(pady=2)
    button.pack(pady=5)
    output_text.pack(padx=10, pady=10)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    win.mainloop()

guid()
