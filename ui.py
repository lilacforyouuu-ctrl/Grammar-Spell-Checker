import tkinter as tk
from tkinter import scrolledtext

# ---------------- FUNCTIONS ---------------- #

def check_text():
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Corrected text will appear here.")
    output_box.config(state="disabled")
    status.config(text="✓ Text Checked Successfully")

def clear_text():
    input_box.delete("1.0", tk.END)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")
    status.config(text="● Ready")

# ---------------- WINDOW ---------------- #

root = tk.Tk()
root.title("SpellSync")
root.geometry("900x680")   # Reduced height
root.configure(bg="#FCF8F8")
root.resizable(False, False)

# ---------------- LOGO ---------------- #

logo_title = tk.Label(
    root,
    text="SpellSync",
    font=("Gabriola", 42),
    bg="#FCF8F8",
    fg="#4A70A9"
)
logo_title.pack(pady=(2, 0))

# ---------------- MAIN TITLE ---------------- #

title = tk.Label(
    root,
    text="✨ Spell & Grammar Checker ✨",
    font=("Georgia", 24, "bold"),
    bg="#FCF8F8",
    fg="#4A70A9"
)
title.pack(pady=(0, 2))

subtitle = tk.Label(
    root,
    text="NLP Based Text Assistant",
    font=("Segoe UI", 11),
    bg="#FCF8F8",
    fg="#5D866C"
)
subtitle.pack(pady=(0, 5))

# ---------------- MAIN CARD ---------------- #

card = tk.Frame(
    root,
    bg="#EFECE3",
    padx=20,
    pady=10
)
card.pack(padx=30, pady=2, fill="both", expand=True)

# ---------------- INPUT SECTION ---------------- #

input_label = tk.Label(
    card,
    text="📝 Enter Text",
    font=("Georgia", 12, "bold"),
    bg="#EFECE3",
    fg="#4A70A9"
)
input_label.pack(anchor="w")

input_box = scrolledtext.ScrolledText(
    card,
    height=7,
    font=("Calibri", 12),
    bg="white",
    relief="flat"
)
input_box.pack(fill="x", pady=(5, 10))

# ---------------- BUTTONS ---------------- #

button_frame = tk.Frame(card, bg="#EFECE3")
button_frame.pack(pady=5)

tk.Button(
    button_frame,
    text="🎤 Voice",
    bg="#8FABD4",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    width=12,
    pady=8
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="🌐 Translate",
    bg="#4A70A9",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    width=12,
    pady=8
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="✓ Check",
    bg="#5D866C",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    width=12,
    pady=8,
    command=check_text
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="🗑 Clear",
    bg="#C2A68C",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    width=12,
    pady=8,
    command=clear_text
).grid(row=0, column=3, padx=5)

tk.Button(
    button_frame,
    text="✖ Exit",
    bg="#F5AFAF",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    width=12,
    pady=8,
    command=root.destroy
).grid(row=0, column=4, padx=5)

# ---------------- OUTPUT SECTION ---------------- #

output_label = tk.Label(
    card,
    text="✨ Corrected Output",
    font=("Georgia", 12, "bold"),
    bg="#EFECE3",
    fg="#4A70A9"
)
output_label.pack(anchor="w", pady=(15, 0))

output_box = scrolledtext.ScrolledText(
    card,
    height=7,
    font=("Calibri", 12),
    bg="white",
    relief="flat"
)
output_box.pack(fill="x", pady=(5, 8))
output_box.config(state="disabled")

# ---------------- STATUS BAR ---------------- #

status = tk.Label(
    root,
    text="● Ready",
    bg="#8FABD4",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    pady=5
)
status.pack(fill="x", padx=30, pady=(0, 3))

# ---------------- FOOTER ---------------- #

footer = tk.Label(
    root,
    text="Developed by Saraah • Yashika • Bisteerna • Bastav • Riyan• Siddharth",
    bg="#FCF8F8",
    fg="#4A70A9",
    font=("Georgia", 10, "italic"),
    pady=5
)
footer.pack(side="bottom", fill="x")

root.mainloop()
