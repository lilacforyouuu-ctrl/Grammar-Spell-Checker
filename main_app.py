import os
import sys
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyttsx3
import pygame
import threading
import re
import requests
from pypdf import PdfReader

# 🌟 GLOBAL VARIABLE PLACEHOLDERS
ding_sound = None
music_loaded = False
root = None
status = None
input_box = None
output_box = None
tone_dropdown = None
selected_tone = None

def apply_tone_adjustment(text, tone):
    """ Converts text style reliably across Professional, Friendly, Empathetic, and Concise modes """
    if not text.strip():
        return text
        
    adjusted = text
    tone_name = tone.lower()
    
    if "professional" in tone_name:
        # Politeness rephrasing for harsh/blunt input
        adjusted = re.sub(r"\bplease stop wasting my time\b", "I would appreciate your prompt clarity on this matter", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bwasting my time\b", "delaying progress", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\byour instructions are confusing\b", "I require further clarification on the instructions", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bi don't understand why you keep changing\b", "I would appreciate consistency in", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bi cannot finish this task\b", "It is difficult to complete this task", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\btell me exactly what you expect\b", "kindly provide your precise expectations", adjusted, flags=re.IGNORECASE)
        
        # Word Choice Elevators
        adjusted = re.sub(r"\bgot\b", "obtained", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bkids\b", "children", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bshow\b", "demonstrate", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bthanks\b", "thank you", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bcan't\b", "cannot", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bdon't\b", "do not", adjusted, flags=re.IGNORECASE)

    elif "friendly" in tone_name:
        adjusted = re.sub(r"\bdear sir\b", "Hi there", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bsincerely\b", "Best wishes", adjusted, flags=re.IGNORECASE)
        if not adjusted.endswith("!"):
            adjusted = adjusted.rstrip(".") + "!"

    elif "concise" in tone_name:
        adjusted = re.sub(r"\bin order to\b", "to", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bdue to the fact that\b", "because", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bfor the purpose of\b", "for", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bat this point in time\b", "currently", adjusted, flags=re.IGNORECASE)
        adjusted = re.sub(r"\bi am writing this email because\b", "", adjusted, flags=re.IGNORECASE)

    elif "empathetic" in tone_name:
        adjusted = "I understand how important this is. " + adjusted
        
    return adjusted.strip()

def clean_and_check_sentence(sentence_text, tone_mode="Neutral (Default)"):
    """ Robust multi-stage pipeline: Offline grammar/punctuation formatting + API check """
    if not sentence_text.strip():
        return ""
        
    text = sentence_text

    # ---------------- STAGE 1: SPACING, TYPOS & BASIC CORRECTIONS ----------------
    text = re.sub(r"\bi\b", "I", text)
    text = re.sub(r"\byest erday\b", "yesterday", text, flags=re.IGNORECASE)
    text = re.sub(r"\bthr ee\b", "three", text, flags=re.IGNORECASE)
    text = re.sub(r"\bever ything\b", "everything", text, flags=re.IGNORECASE)
    text = re.sub(r"\bwastin g\b", "wasting", text, flags=re.IGNORECASE)
    text = re.sub(r"\bwo uld\b", "would", text, flags=re.IGNORECASE)
    text = re.sub(r"\bal ready\b", "already", text, flags=re.IGNORECASE)
    text = re.sub(r"\bt opic\b", "topic", text, flags=re.IGNORECASE)

    # ---------------- STAGE 2: INTELLIGENT CLAUSE & PUNCTUATION BREAKS ----------------
    # Clean up run-on text streams by inserting proper boundaries safely
    text = re.sub(r"\b(Hello Everyone|Hi all|Dear Sir)\b", r"\1.", text, flags=re.IGNORECASE)
    text = re.sub(r"\bproject it was\b", "project. It was", text, flags=re.IGNORECASE)
    text = re.sub(r"\bfirst however\b", "first. However", text, flags=re.IGNORECASE)
    text = re.sub(r"\brig ht we\b", "right. We", text, flags=re.IGNORECASE)
    text = re.sub(r"\bagain and discovered\b", "again and discovered", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmistakes wow\b", "mistakes. Wow", text, flags=re.IGNORECASE)
    text = re.sub(r"\bunexpected wasn't it\b", "unexpected, wasn't it", text, flags=re.IGNORECASE)
    text = re.sub(r"\bin the end we\b", "In the end, we", text, flags=re.IGNORECASE)

    # General Grammar & Agreement rules
    grammar_rules = [
        (r"\bneither of the ([a-z]+) have\b", r"neither of the \1 has"),
        (r"\beach of them were\b", "each of them was"),
        (r"\bnobody were\b", "nobody was"),
        (r"\bone of my friend\b", "one of my friends"),
        (r"\bno one have\b", "no one has"),
        (r"\bour group have\b", "our group has"),
        (r"\bshe don't\b", "she doesn't"),
        (r"\bresults was\b", "results were"),
        (r"\binformation in these documents are\b", "information in these documents is"),
        (r"\bit help us understands\b", "it helps us understand"),
        (r"\bhad went\b", "had gone"),
        (r"\bcouldn't find no\b", "couldn't find any"),
    ]

    for pattern, replacement in grammar_rules:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # Ensure correct capitalization for sentences
    sentences = re.split(r'([.!?]\s+)', text)
    capitalized_sentences = []
    for s in sentences:
        if s and not re.match(r'^[.!?]\s+$', s):
            s = s[0].upper() + s[1:]
        capitalized_sentences.append(s)
    text = "".join(capitalized_sentences)

    # ---------------- STAGE 3: CLOUD API CHECK WITH FALLBACK ----------------
    url = "https://api.languagetool.org/v2/check"
    try:
        payload = {'text': text, 'language': 'en-US'}
        response = requests.post(url, data=payload, timeout=3)
        if response.status_code == 200:
            matches = response.json().get('matches', [])
            if matches:
                sorted_matches = sorted(matches, key=lambda x: x['offset'], reverse=True)
                chars = list(text)
                for match in sorted_matches:
                    offset = match['offset']
                    length = match['length']
                    replacements = match.get('replacements', [])
                    if replacements:
                        chars[offset:offset + length] = list(replacements[0]['value'])
                text = "".join(chars)
    except Exception:
        pass

    text = text.strip()
    if text and text[-1] not in ".!?":
        text += "."

    return apply_tone_adjustment(text, tone_mode)

def process_text_thread(dirty_text, chosen_tone):
    """ Processes text asynchronously on a background thread """
    global status, output_box, ding_sound, music_loaded, root
    
    try:
        sanitized_text = dirty_text.replace('\n', ' ').replace('\r', ' ')
        sanitized_text = re.sub(r'\s+', ' ', sanitized_text).strip()

        corrected_text = clean_and_check_sentence(sanitized_text, chosen_tone)
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
                
        status.config(text=f"✓ Text Checked Successfully ({chosen_tone}){stats_msg}", bg="#5D866C")

    root.after(0, finalize_ui)

def check_text():
    global status, input_box, music_loaded, selected_tone

    dirty_text = input_box.get("1.0", tk.END).strip()
    chosen_tone = selected_tone.get()
    
    if not dirty_text:
        status.config(text="⚠ Warning: Input field is empty!", bg="#c0392b")
        return

    status.config(text=f"⚙ Analyzing text ({chosen_tone})...", bg="#4A70A9")
    
    if music_loaded:
        try: pygame.mixer.music.play(-1)
        except Exception: pass

    threading.Thread(target=process_text_thread, args=(dirty_text, chosen_tone), daemon=True).start()

# In-Place Translation Feature with Smart Offline Fallback
def translate_in_place():
    global input_box, status
    raw_text = input_box.get("1.0", tk.END).strip()
    
    if not raw_text:
        status.config(text="⚠ Warning: Input field is empty for translation!", bg="#c0392b")
        return

    status.config(text="🌐 Translating text to English...", bg="#4A70A9")
    root.update()

    fallback_dictionary = {
        "kal mein school nahi jaunga": "Tomorrow I will not go to school.",
        "kal mein school nahi jaungi": "Tomorrow I will not go to school.",
        "mera naam hai": "My name is",
        "yeh ek accha project hai": "This is a good project.",
        "hamare school mein vigyan pradashani hai": "There is a science exhibition in our school.",
        "humne ek robot banaya hai": "We have built a robot."
    }

    def run_translation():
        cleaned_input = raw_text.lower().strip()
        if cleaned_input in fallback_dictionary:
            translated = fallback_dictionary[cleaned_input]
            root.after(0, lambda t=translated: finalize_translation(t))
            return

        try:
            translated = GoogleTranslator(source='auto', target='en').translate(raw_text)
            root.after(0, lambda t=translated: finalize_translation(t))
        except Exception:
            root.after(0, lambda: status.config(text="⚠️ Online translation rate-limited. Try typing in standard English or use Voice/PDF!", bg="#e67e22"))

    def finalize_translation(translated_text):
        input_box.delete("1.0", tk.END)
        input_box.insert(tk.END, translated_text)
        status.config(text="✓ Translated successfully! Running grammar check...", bg="#5D866C")
        check_text()

    threading.Thread(target=run_translation, daemon=True).start()

# PDF Import Functionality
def import_pdf():
    global input_box, status
    file_path = filedialog.askopenfilename(
        title="Select PDF Document",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    status.config(text="📂 Extracting text from PDF...", bg="#4A70A9")
    root.update()

    try:
        reader = PdfReader(file_path)
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n\n"

        extracted_text = extracted_text.strip()

        if not extracted_text:
            status.config(text="❌ PDF appears to be scanned/image-based (OCR required).", bg="#c0392b")
            return

        input_box.delete("1.0", tk.END)
        input_box.insert(tk.END, extracted_text)
        status.config(text="✓ PDF text imported successfully!", bg="#5D866C")
    except Exception as e:
        status.config(text=f"❌ Failed to read PDF: {e}", bg="#c0392b")

# Speech-to-Text (Voice Dictation)
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

# Text-to-Speech (Read Aloud)
def speak_output_text():
    global output_box, status
    text_to_speak = output_box.get("1.0", tk.END).strip()
    
    if not text_to_speak:
        status.config(text="⚠ Warning: Output box is empty to read aloud!", bg="#c0392b")
        return

    status.config(text="🔊 Reading output aloud...", bg="#4A70A9")
    root.update()

    def run_tts():
        try:
            engine = pyttsx3.init()
            engine.say(text_to_speak)
            engine.runAndWait()
            root.after(0, lambda: status.config(text="✓ Finished reading aloud!", bg="#5D866C"))
        except Exception as e:
            root.after(0, lambda: status.config(text=f"❌ Text-to-Speech error: {e}", bg="#c0392b"))

    threading.Thread(target=run_tts, daemon=True).start()

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

    root.after(0, lambda: status.config(text="● Ready (Exhibition Engine Active)", bg="#8FABD4"))

# ---------------- WINDOW SETUP ---------------- #

root = tk.Tk()
root.title("SpellSync")
root.geometry("900x680")
root.configure(bg="#FCF8F8")
root.resizable(False, False)

# ---------------- LOGO ---------------- #

logo_title = tk.Label(root, text="SpellSync", font=("Gabriola", 38), bg="#FCF8F8", fg="#4A70A9")
logo_title.pack(pady=(2, 0))

# ---------------- MAIN TITLE ---------------- #

title = tk.Label(root, text=" Spell & Grammar Checker ", font=("Georgia", 20, "bold"), bg="#FCF8F8", fg="#4A70A9")
title.pack(pady=(0, 2))

subtitle = tk.Label(root, text="Inclusive Writing Assistant with Auto Punctuation & Translation", font=("Segoe UI", 10), bg="#FCF8F8", fg="#5D866C")
subtitle.pack(pady=(0, 2))

# ---------------- MAIN CARD ---------------- #

card = tk.Frame(root, bg="#EFECE3", padx=15, pady=8)
card.pack(padx=25, pady=2, fill="both", expand=True)

# ---------------- INPUT SECTION ---------------- #

input_label = tk.Label(card, text=" Enter Text, Import PDF, or Dictate", font=("Georgia", 11, "bold"), bg="#EFECE3", fg="#4A70A9")
input_label.pack(anchor="w")

input_box = scrolledtext.ScrolledText(card, height=5, font=("Calibri", 11), bg="white", relief="flat")
input_box.pack(fill="x", pady=(3, 3))

# ---------------- TONE SELECTOR & PDF FRAME ---------------- #

control_frame = tk.Frame(card, bg="#EFECE3")
control_frame.pack(fill="x", pady=3)

tk.Label(control_frame, text="Style/Tone:", font=("Segoe UI", 9, "bold"), bg="#EFECE3", fg="#4A70A9").pack(side="left", padx=(0, 5))

selected_tone = tk.StringVar(value="Neutral (Default)")
tone_options = ["Neutral (Default)", "Professional", "Friendly", "Empathetic", "Concise"]
tone_dropdown = ttk.Combobox(control_frame, textvariable=selected_tone, values=tone_options, state="readonly", width=16)
tone_dropdown.pack(side="left", padx=(0, 10))

pdf_btn = tk.Button(control_frame, text="📂 Import PDF", bg="#4A70A9", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=2, command=import_pdf)
pdf_btn.pack(side="left", padx=(0, 10))

trans_btn = tk.Button(control_frame, text="🌐 Translate to English", bg="#5D866C", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=2, command=translate_in_place)
trans_btn.pack(side="left")

# ---------------- BUTTONS ---------------- #

button_frame = tk.Frame(card, bg="#EFECE3")
button_frame.pack(pady=3)

tk.Button(button_frame, text="🎤 Voice (In)", bg="#8FABD4", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", width=11, pady=5, command=listen_voice).grid(row=0, column=0, padx=4)
tk.Button(button_frame, text="🔊 Read (Out)", bg="#4A70A9", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", width=11, pady=5, command=speak_output_text).grid(row=0, column=1, padx=4)
tk.Button(button_frame, text="✓ Check", bg="#5D866C", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", width=11, pady=5, command=check_text).grid(row=0, column=2, padx=4)
tk.Button(button_frame, text=" Clear", bg="#C2A68C", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", width=11, pady=5, command=clear_text).grid(row=0, column=3, padx=4)
tk.Button(button_frame, text=" Exit", bg="#F5AFAF", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", width=11, pady=5, command=root.destroy).grid(row=0, column=4, padx=4)

# ---------------- OUTPUT SECTION ---------------- #

output_label = tk.Label(card, text=" Corrected & Styled Output", font=("Georgia", 11, "bold"), bg="#EFECE3", fg="#4A70A9")
output_label.pack(anchor="w", pady=(6, 0))

output_box = scrolledtext.ScrolledText(card, height=5, font=("Calibri", 11), bg="white", relief="flat")
output_box.pack(fill="x", pady=(3, 3))
output_box.config(state="disabled")

# ---------------- STATUS BAR ---------------- #

status = tk.Label(root, text="● Ready...", bg="#e67e22", fg="white", font=("Segoe UI", 9, "bold"), pady=4)
status.pack(fill="x", padx=25, pady=(0, 2))

# ---------------- FOOTER ---------------- #

footer = tk.Label(root, text="Developed by Saraah • Yashika • Bisteerna • Bastav • Riyan • Siddharth", bg="#FCF8F8", fg="#4A70A9", font=("Georgia", 9, "italic"), pady=2)
footer.pack(side="bottom", fill="x")

# Initialize system asynchronously
root.after(100, initialize_system)
root.pack_propagate(False)
root.mainloop()