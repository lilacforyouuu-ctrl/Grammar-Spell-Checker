import tkinter as tk
from spellchecker import SpellChecker

# Initialize the spelling brain
spell = SpellChecker()

def fix_text():
    # Take what the user typed in the box
    input_text = user_input.get("1.0", tk.END).strip()
    
    # Split into words and fix them
    words = input_text.split()
    corrected_words = [spell.correction(word) if spell.correction(word) else word for word in words]
    
    # Show the fixed text in the output box
    result_text = " ".join(corrected_words)
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result_text)
    output_box.config(state=tk.DISABLED)

# Build the window
window = tk.Tk()
window.title("Class 10 CBSE AI Project")
window.geometry("450x350")

# Input Section
tk.Label(window, text="Type a misspelled sentence:", font=("Arial", 11)).pack(pady=5)
user_input = tk.Text(window, height=4, width=45)
user_input.pack()

# Button
check_button = tk.Button(window, text="✨ Fix Spelling ✨", command=fix_text, bg="#4A90E2", fg="white", font=("Arial", 10, "bold"))
check_button.pack(pady=15)

# Output Section
tk.Label(window, text="AI Corrected Result:", font=("Arial", 11)).pack(pady=5)
output_box = tk.Text(window, height=4, width=45, state=tk.DISABLED)
output_box.pack()

window.mainloop()