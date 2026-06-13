import os
import sys
import tkinter as tk
from tkinter import scrolledtext
import language_tool_python as ltp
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pygame
import threading
import re

# 🔥 FORCE EXPLICIT JAVA BINARY DIRECTORY PATHS TO PREVENT FREEZING
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-17"
os.environ["PATH"] = r"C:\Program Files\Java\jdk-17\bin;" + os.environ["PATH"]

# 🌟 GLOBAL VARIABLE PLACEHOLDERS
tool = None
ding_sound = None
music_loaded = False
root = None
status = None
input_box = None
output_box = None

# ---------------- FUNCTIONS ---------------- #

def clean_and_check_sentence(sentence_text):
    """ Cleans slang and runs NLP context checking cleanly without breaking homophones """
    global tool
    if not sentence_text.strip():
        return ""
        
    # Pre-process conversational patterns
    normalized = sentence_text.replace("me name", "my name is")
    normalized = normalized.replace("Me name", "My name is")
    
    words = normalized.split()
    cleaned_words = []
    
    for idx, word in enumerate(words):
        # Separate the raw punctuation from the base word so it doesn't mask homophones
        base = word.strip(".,!?\"'")
        base_lower = base.lower()
        
        if base_lower in ["hi", "hii", "hey"]:
            cleaned_word = "Hi," if idx == 0 else "hi"
        elif base_lower in ["fam", "buddies", "buddy"]:
            cleaned_word = "family"
        elif base_lower in ["finali", "finallyy", "flnali"]:
            cleaned_word = "finally"
        elif base_lower == "i":
            cleaned_word = "I"
        else:
            cleaned_word = base  # Send clean word WITHOUT punctuation attached
            
        if cleaned_word:
            cleaned_words.append(cleaned_word)
        
    processed_input = " ".join(cleaned_words)
    
    if not processed_input.strip():
        return ""

    # Run LanguageTool matching on clean, unpunctuated text tokens
    matches = tool.check(processed_input)
    corrected = ltp.utils.correct(processed_input, matches)
    
    # Capitalize sentence starter and append neat final punctuation
    if corrected:
        corrected = corrected.strip()
        corrected = corrected[0].upper() + corrected[1:]
        
        # Smart sentence termination check
        if corrected[-1] not in ['.', '!', '?']:
            question_starters = ["what", "why", "how", "who", "where", "when", "which", "whose", "whom", 
                                 "is", "are", "am", "can", "could", "do", "does", "did", "will", "would", "should", "have", "has"]
            first_word = corrected.split()[0].lower().strip(",.!?\"'")
            if first_word in question_starters:
                corrected += '?'
            else:
                corrected += '.'
                
    return corrected

def process_text_thread(dirty_text):
    """ Safely breaks up text into sentences so context maps perfectly without error """
    global status, output_box, ding_sound, music_loaded, root
    
    try:
        # CRITICAL FIX: Sanitize all hidden newlines, trailing tabs, and messy wrap spaces
        sanitized_text = dirty_text.replace('\n', ' ').replace('\r', ' ')
        sanitized_text = re.sub(r'\s+', ' ', sanitized_text).strip()

        # Smart regex split to separate sentences by (. ! ?) while keeping punctuation intact
        raw_sentences = re.split(r'(?<=[.!?])\s+', sanitized_text)
        corrected_sentences = []
        
        for raw_s in raw_sentences:
            if raw_s.strip():
                fixed_s = clean_and_check_sentence(raw_s)
                if fixed_s:
                    corrected_sentences.append(fixed_s)
                    
        corrected_text = " ".join(corrected_sentences)
            
    except Exception as err:
        corrected_text = f"Processing Error: {err}"

    # Stop intermission ambient track as soon as calculation completes
    if music_loaded:
        try: pygame.mixer.music.stop()
        except Exception: pass

    # Update UI components safely back on the main thread
    w_count = len(dirty_text.split())
    c_count = len(dirty_text)
    stats_msg = f"  |  Stats: {w_count} Words, {c_count} Chars"

    def finalize_ui():
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, corrected_text)
        output_box.config(state="disabled")
        
        if ding_sound:
            try: ding_sound.play()
            except Exception: pass
                
        status.config(text=f"✓ Text Checked Successfully{stats_msg}", bg="#5D866C")

    root.after(0, finalize_ui)


def check_text():
    global tool, status, input_box, music_loaded
    
    if tool is None:
        status.config(text="❌ Engine still loading or unavailable!", bg="#c0392b")
        return

    dirty_text = input_box.get("1.0", tk.END).strip()
    
    if not dirty_text:
        status.config(text="⚠ Warning: Input field is empty!", bg="#c0392b")
        return

    status.config(text="⚙ Analyzing text matching absolute grammar matrix...", bg="#4A70A9")
    
    if music_loaded:
        try: pygame.mixer.music.play(-1)
        except Exception: pass

    threading.Thread(target=process_text_thread, args=(dirty_text,), daemon=True).start()


# Popup Box for Translation
def open_translate_window():
    global root, status, input_box
    
    trans_win = tk.Toplevel(root)
    trans_win.title("Regional Translator Box")
    trans_win.geometry("500x350")
    trans_win.configure(bg="#FCF8F8")
    trans_win.resizable(False, False)
    
    tk.Label(
        trans_win, 
        text="Enter Regional Text to Translate:", 
        font=("Georgia", 12, "bold"), 
        bg="#FCF8F8", 
        fg="#4A70A9"
    ).pack(pady=(15, 5), anchor="w", padx=20)
    
    trans_input = scrolledtext.ScrolledText(
        trans_win, 
        height=8, 
        width=52, 
        font=("Calibri", 11), 
        bg="white", 
        relief="solid", 
        bd=1
    )
    trans_input.pack(pady=5, padx=20)
    
    def process_translation():
        raw_text = trans_input.get("1.0", tk.END).strip()
        if not raw_text:
            return
        
        status.config(text="🌐 Translating Regional Context...", bg="#4A70A9")
        root.update()
        
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(raw_text)
            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, translated)
            check_text()
            trans_win.destroy() 
        except Exception as e:
            status.config(text=f"❌ Translation failed: {e}", bg="#c0392b")

    tk.Button(
        trans_win,
        text="Translate & Load to Main App",
        bg="#4A70A9",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        pady=5,
        command=process_translation
    ).pack(pady=15)

def listen_voice():
    global status, input_box, root
    status.config(text="🎤 Listening... Speak now!", bg="#e67e22")
    root.update()

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            spoken_text = recognizer.recognize_google(audio)
            input_box.insert(tk.END, " " + spoken_text)
            status.config(text="● Voice Captured Successfully!", bg="#5D866C")
        except Exception:
            status.config(text="❌ Microphone timeout or disconnected.", bg="#c0392b")

def clear_text():
    global input_box, output_box, status
    input_box.delete("1.0", tk.END)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")
    status.config(text="● Ready", bg="#8FABD4")

# ---------------- CORE LIFECYCLE MANAGEMENT ---------------- #
def async_engine_boot():
    """ Boots up LanguageTool on a separate background thread cleanly """
    global tool, status, root
    try:
        tool = ltp.LanguageTool('en-US')
        root.after(0, lambda: status.config(text="● Ready", bg="#8FABD4"))
    except Exception as e:
        root.after(0, lambda: status.config(text=f"❌ Engine Connection Failure: {e}", bg="#c0392b"))

def initialize_system():
    global ding_sound, music_loaded
    
    try:
        pygame.mixer.init()
        folder_files = os.listdir(".")

        for option in ["ding.wav.mp3", "ding.wav", "ding.mp3"]:
            if option in folder_files:
                ding_sound = pygame.mixer.Sound(option)
                break

        for option in ["intermission_ambient.mp3.mp3", "intermission_ambient.mp3", "intermission_ambient.wav"]:
            if option in folder_files:
                pygame.mixer.music.load(option)
                music_loaded = True
                break
    except Exception:
        pass

    threading.Thread(target=async_engine_boot, daemon=True).start()

# ---------------- WINDOW SETUP ---------------- #

root = tk.Tk()
root.title("SpellSync")
root.geometry("900x680")
root.configure(bg="#FCF8F8")
root.resizable(False, False)

# ---------------- LOGO ---------------- #

logo_title = tk.Label(root, text="SpellSync", font=("Gabriola", 42), bg="#FCF8F8", fg="#4A70A9")
logo_title.pack(pady=(2, 0))

# ---------------- MAIN TITLE ---------------- #

title = tk.Label(root, text=" Spell & Grammar Checker ", font=("Georgia", 24, "bold"), bg="#FCF8F8", fg="#4A70A9")
title.pack(pady=(0, 2))

subtitle = tk.Label(root, text="NLP Based Text Assistant", font=("Segoe UI", 11), bg="#FCF8F8", fg="#5D866C")
subtitle.pack(pady=(0, 5))

# ---------------- MAIN CARD ---------------- #

card = tk.Frame(root, bg="#EFECE3", padx=20, pady=10)
card.pack(padx=30, pady=2, fill="both", expand=True)

# ---------------- INPUT SECTION ---------------- #

input_label = tk.Label(card, text=" Enter Text", font=("Georgia", 12, "bold"), bg="#EFECE3", fg="#4A70A9")
input_label.pack(anchor="w")

input_box = scrolledtext.ScrolledText(card, height=7, font=("Calibri", 12), bg="white", relief="flat")
input_box.pack(fill="x", pady=(5, 10))

# ---------------- BUTTONS ---------------- #

button_frame = tk.Frame(card, bg="#EFECE3")
button_frame.pack(pady=5)

tk.Button(button_frame, text=" Voice", bg="#8FABD4", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", width=12, pady=8, command=listen_voice).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text=" Translate", bg="#4A70A9", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", width=12, pady=8, command=open_translate_window).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="✓ Check", bg="#5D866C", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", width=12, pady=8, command=check_text).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text=" Clear", bg="#C2A68C", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", width=12, pady=8, command=clear_text).grid(row=0, column=3, padx=5)
tk.Button(button_frame, text=" Exit", bg="#F5AFAF", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", width=12, pady=8, command=root.destroy).grid(row=0, column=4, padx=5)

# ---------------- OUTPUT SECTION ---------------- #

output_label = tk.Label(card, text=" Corrected Output", font=("Georgia", 12, "bold"), bg="#EFECE3", fg="#4A70A9")
output_label.pack(anchor="w", pady=(15, 0))

output_box = scrolledtext.ScrolledText(card, height=7, font=("Calibri", 12), bg="white", relief="flat")
output_box.pack(fill="x", pady=(5, 8))
output_box.config(state="disabled")

# ---------------- STATUS BAR ---------------- #

status = tk.Label(root, text="● Loading Language Engine...", bg="#e67e22", fg="white", font=("Segoe UI", 10, "bold"), pady=5)
status.pack(fill="x", padx=30, pady=(0, 3))

# ---------------- FOOTER ---------------- #

footer = tk.Label(root, text="Developed by Saraah • Yashika • Bisteerna • Bastav • Riyan • Siddharth", bg="#FCF8F8", fg="#4A70A9", font=("Georgia", 10, "italic"), pady=5)
footer.pack(side="bottom", fill="x")

# Fire safe asynchronous engine mapping setup
root.after(100, initialize_system)
root.pack_propagate(False)
root.mainloop()

if tool is not None:
    try: tool.close()
    except Exception: pass
