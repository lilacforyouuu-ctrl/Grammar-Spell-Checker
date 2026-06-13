# main.py
import sys
import os

print("--- Starting SpellSync AI System Platform ---")

# Automatically launch the main application pipeline
try:
    import main_app
except ImportError as e:
    print(f"❌ Critical Launch Error: Could not find application dependencies. {e}")
    print("Ensure 'main_app.py' and 'word_analyzer.py' are in the exact same folder.")
