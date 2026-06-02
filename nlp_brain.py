import language_tool_python

try:
    # Initialize the engine (Switch to 'en-GB' if you want better slang defaults, or keep 'en-US')
    tool = language_tool_python.LanguageTool('en-US')
except Exception as e:
    print(f"Warning: Could not initialize LanguageTool: {e}")
    tool = None

def fix_sentence_context(dirty_text: str) -> str:
    # 1. Handle empty strings or non-string inputs
    if not dirty_text or not isinstance(dirty_text, str) or dirty_text.strip() == "":
        return dirty_text

    # 2. Skip processing if input is just numbers
    if dirty_text.strip().isdigit():
        return dirty_text

    # 3. Fallback if tool failed to start
    if tool is None:
        return dirty_text

    # 🚀 NEW: TEXT NORMALIZATION LAYER (Slang Dictionary)
    slang_lookup = {
        "tmrw": "tomorrow",
        "skool": "school",
        "skul": "school",
        "stuy": "study",
        "englh": "English"
    }
    
    # Split the sentence into individual words to check for slang matches
    words = dirty_text.split()
    cleaned_words = []
    
    for word in words:
        # Strip trailing/leading punctuation attached to the word (like "tmrw!")
        core_word = word.strip(".,!?\"'").lower()
        
        if core_word in slang_lookup:
            # Swap the slang with the correct formal dictionary word
            cleaned_words.append(slang_lookup[core_word])
        else:
            cleaned_words.append(word)
            
    # Reassemble the normalized sentence
    normalized_text = " ".join(cleaned_words)
    # ----------------------------------------------------

    try:
        # 4. Correct text using context (Passing normalized_text now!)
        corrected_text = tool.correct(normalized_text)
        return corrected_text
    except Exception as e:
        print(f"Error during NLP processing: {e}")
        return dirty_text