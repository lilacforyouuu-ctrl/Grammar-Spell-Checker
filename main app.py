import os
# 1. FORCE PYTHON TO USE JAVA 17 FOR THE AI GRAMMAR ENGINE
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-17"

import tkinter as tk
from tkinter import scrolledtext
import nlp_brain

# Safely bridge Riyan's statistics module
try:
    import word_analyzer
except ImportError:
    word_analyzer = None

# ADVANCED COMPONENT LIBRARIES FOR YOUR SPECIAL FEATURES
from deep_translator import GoogleTranslator
import speech_recognition as sr

# ---------------- FUNCTIONS ---------------- #

def check_text():
    """ Runs your core AI Engine and captures Riyan's word statistics """
    status.config(text="⚙ Processing Text with AI Engine...", bg="#4A70A9")
    root.update()
    
    # Grab raw input from the UI input box
    dirty_text = input_box.get("1.0", tk.END).strip()
    
    if not dirty_text:
        status.config(text="⚠ Warning: Input field is empty!", bg="#c0392b")
        return

    # Run your Context Grammar module
    corrected_text = nlp_brain.fix_sentence_context(dirty_text)
    
    # Calculate metrics using Riyan's logic backend (with automated fallback)
    if word_analyzer and hasattr(word_analyzer, 'get_text_stats'):
        try:
            w_count, c_count = word_analyzer.get_text_stats(dirty_text)
            stats_msg = f"  |  Stats: {w_count} Words, {c_count} Chars"
        except Exception:
            stats_msg = ""
    else:
        w_count = len(dirty_text.split())
        c_count = len(dirty_text)
        stats_msg = f"  |  Stats: {w_count} Words, {c_count} Chars"

    # Display the final corrected text into the output text area
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, corrected_text)
    output_box.config(state="disabled")
    
    status.config(text=f"✓ Text Checked Successfully{stats_msg}", bg="#5D866C")


def translate_text():
    """ Your Feature 1: Hindi/Hinglish to English Live Context Translator """
    status.config(text="🌐 Translating Hindi Context to English...", bg="#4A70A9")
    root.update()
    
    dirty_text = input_box.get("1.0", tk.END).strip()
    
    if not dirty_text:
        status.config(text="⚠ Enter Hindi/Hinglish text first!", bg="#c0392b")
        return
        
    try:
        # Automatically translate input to clean English
        translated = GoogleTranslator(source='auto', target='en').translate(dirty_text)
        
        # Swaps out the original messy text with the fresh translation
        input_box.delete("1.0", tk.END)
        input_box.insert(tk.END, translated)
        
        status.config(text="✓ Hindi Translated to English! Click 'Check' to fix grammar rules.", bg="#5D866C")
    except Exception as e:
        status.config(text=f"❌ Translation failed: {e}", bg="#c0392b")


def listen_voice():
    """ Your Feature 2: Voice Dictation Microphone Engine """
    status.config(text="🎤 Listening... Speak into your microphone now!", bg="#e67e22")
    root.update()
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            # Shortened phrase limit so the UI doesn't hang up too long
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=5)
            
            status.config(text="🛑 Processing audio conversion...", bg="#4A70A9")
            root.update()
            
            spoken_text = recognizer.recognize_google(audio)
            
            # Inserts the captured speech straight into the input block
            input_box.insert(tk.END, " " + spoken_text)
            status.config(text="● Voice Captured Successfully!", bg="#5D866C")
        except sr.UnknownValueError:
            status.config(text="❌ Voice Engine couldn't understand the audio speech.", bg="#c0392b")
        except Exception:
            status.config(text="❌ Microphone connection timed out or missing PyAudio.", bg="#c0392b")


def clear_text():
    input_box.delete("1.0", tk.END)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")
    status.config(text="● Ready", bg="#8FABD4")

# ---------------- WINDOW (BASTAV & BISTEERNA DESIGN) ---------------- #

root = tk.Tk()
root.title("Spell & Grammar Checker")
root.geometry("900x650")
root.configure(bg="#FCF8F8")
root.resizable(False, False)

# ---------------- HEADER ---------------- #

title = tk.Label(
    root,
    text="✨ Spell & Grammar Checker ✨",
    font=("Georgia", 24, "bold"),
    bg="#FCF8F8",
    fg="#4A70A9"
)
title.pack(pady=(15, 0))

subtitle = tk.Label(
    root,
    text="NLP Based Text Assistant",
    font=("Segoe UI", 11),
    bg="#FCF8F8",
    fg="#5D866C"
)
subtitle.pack(pady=(0, 15))

# ---------------- MAIN CARD ---------------- #

card = tk.Frame(
    root,
    bg="#EFECE3",
    padx=25,
    pady=20
)
card.pack(padx=30, pady=10, fill="both", expand=True)

# ---------------- INPUT ---------------- #

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
input_box.pack(fill="x", pady=(5, 15))

# ---------------- BUTTONS ---------------- #

button_frame = tk.Frame(card, bg="#EFECE3")
button_frame.pack(pady=5)

voice_btn = tk.Button(
    button_frame,
    text="🎤 Voice",
    bg="#8FABD4",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    width=12,
    pady=8,
    command=listen_voice
)
voice_btn.grid(row=0, column=0, padx=5)

translate_btn = tk.Button(
    button_frame,
    text="🌐 Translate",
    bg="#4A70A9",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    width=12,
    pady=8,
    command=translate_text
)
translate_btn.grid(row=0, column=1, padx=5)

check_btn = tk.Button(
    button_frame,
    text="✓ Check",
    bg="#5D866C",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    width=12,
    pady=8,
    command=check_text
)
check_btn.grid(row=0, column=2, padx=5)

clear_btn = tk.Button(
    button_frame,
    text="🗑 Clear",
    bg="#C2A68C",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    width=12,
    pady=8,
    command=clear_text
)
clear_btn.grid(row=0, column=3, padx=5)

exit_btn = tk.Button(
    button_frame,
    text="✖ Exit",
    bg="#F5AFAF",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    width=12,
    pady=8,
    command=root.destroy
)
exit_btn.grid(row=0, column=4, padx=5)

# ---------------- OUTPUT ---------------- #

output_label = tk.Label(
    card,
    text="✨ Corrected Output",
    font=("Georgia", 12, "bold"),
    bg="#EFECE3",
    fg="#4A70A9"
)
output_label.pack(anchor="w", pady=(20, 0))

output_box = scrolledtext.ScrolledText(
    card,
    height=7,
    font=("Calibri", 12),
    bg="white",
    relief="flat"
)
output_box.pack(fill="x", pady=(5, 10))
output_box.config(state="disabled")

# ---------------- STATUS ---------------- #

status = tk.Label(
    root,
    text="● Ready",
    bg="#8FABD4",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    pady=6
)
status.pack(fill="x", padx=30, pady=(0, 10))

# ---------------- FOOTER ---------------- #

footer = tk.Label(
    root,
    text="• Developed by SpellSync •",
    bg="#FCF8F8",
    fg="#4A70A9",
    font=("Georgia", 9, "italic")
)
footer.pack(pady=(0, 10))

root.mainloop()