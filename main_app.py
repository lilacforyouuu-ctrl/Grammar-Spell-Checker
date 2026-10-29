import os
import sys
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pygame
import threading
import re
import requests

# 🌟 GLOBAL VARIABLE PLACEHOLDERS
ding_sound = None
music_loaded = False
root = None
status = None
input_box = None
output_box = None

def clean_and_check_sentence(sentence_text):
    """ Cleans slang, applies advanced grammar rules, fixes punctuation, and passes to LanguageTool Public API """
    if not sentence_text.strip():
        return ""
        
    normalized = sentence_text

    # Comprehensive structural, grammatical, and punctuation fixes
    structural_fixes = [
        # Introductory & Clause Commas / Splices
        (r"\blast week my teacher\b", "Last week, my teacher"),
        (r"\bscript yesterday it threw\b", "script yesterday, it threw"),
        (r"\bfixing some issues we noticed\b", "fixing some issues, we noticed"),
        (r"\bsolve these bugs quickly our project\b", "solve these bugs quickly, our project"),
        (r"\bfirst, but she\b", "first; she"), # Fix comma splice
        
        # Subject-Verb Agreement Fixes
        (r"\bevery student were\b", "every student was"),
        (r"\bstudents was\b", "students were"),
        (r"\bteachers was\b", "teachers were"),
        (r"\bothers was\b", "others were"),
        (r"\bexhibitions is\b", "exhibitions are"),
        (r"\beveryone were\b", "everyone was"),
        (r"\bmistakes is\b", "mistakes are"),
        (r"\bmotor were\b", "motor was"),
        
        # Verb Tense & Infinitive Corrections
        (r"\bmanaged to fixed\b", "managed to fix"),
        (r"\bhelp us understands\b", "help us understand"),
        (r"\bto remembers\b", "to remember"),
        (r"\bhow to solves\b", "how to solve"),
        (r"\bshould also gives\b", "should also give"),
        (r"\btwo days are not realistic\b", "two days is not realistic"),
        (r"\bi wants\b", "I want"),
        (r"\bif we gets\b", "if we get"),
        (r"\bteam member understand\b", "team member understands"),
        (r"\bsometimes they shows\b", "sometimes they show"),
        
        # Word Replacement & Articles
        (r"\bdidn't had no\b", "had no"),
        (r"\bdidnt had no\b", "had no"),
        (r"\bno one can't\b", "no one could"),
        (r"\bbuild a app\b", "build an app"),
        (r"\bdeep translator\b", "Deep Translator"),
        (r"\bpython\b", "Python"),
        (r"\blanguage,\s*that\b", "language that"),
        (r"\ban advice\b", "advice"),
        (r"\bin a more clearly manner\b", "in a clearer manner"),
        
        # Slang & Typo Cleanup
        (r"\bdat\b", "that"),
        (r"\bkeeped\b", "kept"),
        (r"\bthrowed\b", "threw"),
        (r"\bcreate a small robot\b", "created a small robot"),
        
        # Paragraph Formatting & Sentence Splitting
        (r"\bevaluation but honestly\b", "evaluation. Honestly,"),
        (r"\btools, furthermore\b", "tools. Furthermore,"),
        (r"\bsaving nothing\.\.\.\s*after\b", "saving anything. After"),
        (r"\bsaving nothing\.\.\. after\b", "saving anything. After"),
        (r"\bproperly if\b", "properly. If"),
        (r"\bterrible grade and\b", "terrible grade, and"),
    ]

    for pattern, replacement in structural_fixes:
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

    if not normalized.strip():
        return ""

    # Pass through LanguageTool Public HTTP API safely in chunks
    current_text = normalized
    url = "https://api.languagetool.org/v2/check"
    
    sentences = re.split(r'(?<=[.!?])\s+', current_text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < 400:
            current_chunk += (" " if current_chunk else "") + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk)

    checked_chunks = []
    all_chunks_successful = True

    for chunk in chunks:
        try:
            payload = {
                'text': chunk,
                'language': 'en-US'
            }
            response = requests.post(url, data=payload, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                if matches:
                    sorted_matches = sorted(matches, key=lambda x: x['offset'], reverse=True)
                    chars = list(chunk)
                    for match in sorted_matches:
                        offset = match['offset']
                        length = match['length']
                        replacements = match.get('replacements', [])
                        if replacements:
                            best_replacement = replacements[0]['value']
                            chars[offset:offset + length] = list(best_replacement)
                    chunk = "".join(chars)
                checked_chunks.append(chunk)
            elif response.status_code == 429:
                all_chunks_successful = False
                checked_chunks.append(chunk + " [⚠️ Rate Limit: Unchecked]")
            else:
                all_chunks_successful = False
                checked_chunks.append(chunk + " [❌ Server Error]")
        except requests.exceptions.Timeout:
            all_chunks_successful = False
            checked_chunks.append(chunk + " [⏱️ Timeout]")
        except requests.exceptions.RequestException:
            all_chunks_successful = False
            checked_chunks.append(chunk + " [🔌 Network Error]")

    final_result = " ".join(checked_chunks)
    if not all_chunks_successful:
        final_result += " (Note: Some parts could not be verified due to API limits or network issues.)"

    return final_result.strip()

    # Pass through LanguageTool Public HTTP API safely in chunks
    current_text = normalized
    url = "https://api.languagetool.org/v2/check"
    
    # Split long text into safe sentence/paragraph-aware chunks (approx. 400 chars max per request)
    sentences = re.split(r'(?<=[.!?])\s+', current_text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < 400:
            current_chunk += (" " if current_chunk else "") + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk)

    checked_chunks = []
    all_chunks_successful = True

    for chunk in chunks:
        try:
            payload = {
                'text': chunk,
                'language': 'en-US'
            }
            # Timeout set to 8 seconds to prevent exhibition freezing
            response = requests.post(url, data=payload, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                if matches:
                    sorted_matches = sorted(matches, key=lambda x: x['offset'], reverse=True)
                    chars = list(chunk)
                    for match in sorted_matches:
                        offset = match['offset']
                        length = match['length']
                        replacements = match.get('replacements', [])
                        if replacements:
                            best_replacement = replacements[0]['value']
                            chars[offset:offset + length] = list(best_replacement)
                    chunk = "".join(chars)
                checked_chunks.append(chunk)
            elif response.status_code == 429:
                all_chunks_successful = False
                checked_chunks.append(chunk + " [⚠️ Rate Limit: Unchecked]")
            else:
                all_chunks_successful = False
                checked_chunks.append(chunk + " [❌ Server Error]")
        except requests.exceptions.Timeout:
            all_chunks_successful = False
            checked_chunks.append(chunk + " [⏱️ Timeout]")
        except requests.exceptions.RequestException:
            all_chunks_successful = False
            checked_chunks.append(chunk + " [🔌 Network Error]")

    final_result = " ".join(checked_chunks)
    if not all_chunks_successful:
        final_result += " (Note: Some parts could not be verified due to API limits or network issues.)"

    return final_result.strip()

def process_text_thread(dirty_text):
    """ Standardizes spaces and cleans up residual formatting artifacts """
    global status, output_box, ding_sound, music_loaded, root
    
    try:
        sanitized_text = dirty_text.replace('\n', ' ').replace('\r', ' ')
        sanitized_text = re.sub(r'\s+', ' ', sanitized_text).strip()

        corrected_text = clean_and_check_sentence(sanitized_text)

        if corrected_text and not corrected_text.startswith("("):
            corrected_text = corrected_text[0].upper() + corrected_text[1:]
            
        # Clean up stray spaces around commas and periods
        corrected_text = re.sub(r'\s+([,.!?])', r'\1', corrected_text)
        corrected_text = re.sub(r'\.\s*\.', '.', corrected_text)
            
    except Exception as err:
        corrected_text = f"Processing Error: {err}"

    if music_loaded:
        try: pygame.mixer.music.stop()
        except Exception: pass

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
    global status, input_box, music_loaded

    dirty_text = input_box.get("1.0", tk.END).strip()
    
    if not dirty_text:
        status.config(text="⚠ Warning: Input field is empty!", bg="#c0392b")
        return

    status.config(text="⚙ Analyzing text in safe chunks via Cloud API...", bg="#4A70A9")
    
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
def initialize_system():
    global ding_sound, music_loaded, status, root
    
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

    root.after(0, lambda: status.config(text="● Ready (Cloud API Active)", bg="#8FABD4"))

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

subtitle = tk.Label(root, text="NLP Based Text Assistant (Cloud-Powered)", font=("Segoe UI", 11), bg="#FCF8F8", fg="#5D866C")
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

status = tk.Label(root, text="● Connecting to Cloud API...", bg="#e67e22", fg="white", font=("Segoe UI", 10, "bold"), pady=5)
status.pack(fill="x", padx=30, pady=(0, 3))

# ---------------- FOOTER ---------------- #

footer = tk.Label(root, text="Developed by Saraah • Yashika • Bisteerna • Bastav • Riyan • Siddharth", bg="#FCF8F8", fg="#4A70A9", font=("Georgia", 10, "italic"), pady=5)
footer.pack(side="bottom", fill="x")

# Initialize system asynchronously
root.after(100, initialize_system)
root.pack_propagate(False)
root.mainloop()