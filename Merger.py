import customtkinter as ctk
from pypdf import PdfReader, PdfWriter
from tkinter import filedialog
import os 
import sys

selected_files = []
writer = PdfWriter()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("PDF Merger")
root.geometry("800x800")

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

root.after(200, lambda: root.iconbitmap(resource_path("merge.ico")))

ctk.CTkLabel(root, text="PDF Merger", font=("Arial", 20, "bold")).pack(pady=10)
output = ctk.CTkTextbox(root, height=200, width=400,font= ("Arial",14))
output.pack()
ctk.CTkLabel(root, text="Upload your Files", font=("Arial", 16, "bold")).pack()

def make_button(text, command, fg_color, hover_color):
    ctk.CTkButton(
        root,
        text=text,
        command=command,
        width=200,
        height=40,
        corner_radius=10,
        fg_color=fg_color,
        hover_color=hover_color,
        font=("Arial", 14, "bold")
    ).pack(pady=5)

def select():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    selected_files.extend(files)
    output.delete("1.0", ctk.END)
    for file in selected_files:
        output.insert(ctk.END, f"Files selected: {os.path.basename(file)}\n")

def merge(filename):
    writer = PdfWriter()
    for file in selected_files:
        reader = PdfReader(file)
        for page in reader.pages:
            writer.add_page(page)
    with open(filename, "wb") as output_file:
        writer.write(output_file)
    output.insert(ctk.END, f"Saved as {filename}\n")


def show_save_popup():
    if len(selected_files) < 2:
        output.insert(ctk.END, "Please upload more than 1 file\n")
        return
    popup = ctk.CTkToplevel(root)
    popup.title("Save As")
    popup.geometry("400x200")

    ctk.CTkLabel(popup, text="Enter name for merged PDF:").pack(pady=10)
    
    entry_name = ctk.CTkEntry(popup, width=250)
    entry_name.pack(pady=5)

    def confirm():
        name = entry_name.get().strip()
        if not name:
            return
        if not name.endswith(".pdf"):
            name += ".pdf"
        merge(name)
        popup.destroy()   

    ctk.CTkButton(popup, text="Merge", command=confirm, width=200,height=50,corner_radius=10,fg_color="#2ecc71",hover_color="#27ae60",font=("Arial", 14, "bold")).pack(pady=10)

make_button("Upload To Merge",select, "#e74c3c","#c0392b")
make_button("Merge",show_save_popup,"#2ecc71","#27ae60")

root.mainloop()