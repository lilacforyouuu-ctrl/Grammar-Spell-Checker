import os
# 1. FORCE PYTHON TO USE JAVA 17
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-17"

import language_tool_python

def fix_sentence_context(dirty_text):
    if not dirty_text.strip():
        return ""
    try:
        tool = language_tool_python.LanguageTool('en-GB')
        matches = tool.check(dirty_text)
        clean_text = language_tool_python.utils.correct(dirty_text, matches)
        return clean_text
    except Exception as e:
        print(f"Error processing text: {e}")
        return dirty_text

if __name__ == "__main__":
    print("--- Testing the AI Logic Engine ---")
    test_sentence = "The children are running inside the skool building."
    print("Original sentence: ", test_sentence)
    print("Processing...")
    corrected = fix_sentence_context(test_sentence)
    print("AI Corrected result:", corrected)