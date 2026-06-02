import language_tool_python

try:
    tool = language_tool_python.LanguageTool('en-US')
    print("LanguageTool initialized successfully.")
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

    # Track terminal punctuation from the original input text
    clean_stripped = dirty_text.strip()
    ends_with_period = clean_stripped.endswith(".")
    ends_with_exclamation = clean_stripped.endswith("!")
    ends_with_question = clean_stripped.endswith("?")

    # Force string to lowercase immediately so shouty caps don't break token parsing
    normalized_input = dirty_text.lower()

    # TEXT NORMALIZATION LAYER (Slang Dictionary)
    slang_lookup = {
        "tmrw": "tomorrow",
        "skool": "school",
        "skul": "school",
        "stuy": "study",
        "englh": "English",
        "finali": "finally",
        "fam": "family",
        "u": "you",
        "r": "are"
    }
    
    words = normalized_input.split()
    cleaned_words = []
    
    for word in words:
        left_punctuation = ""
        right_punctuation = ""
        
        while word and word[-1] in ".,!?\"';:":
            right_punctuation = word[-1] + right_punctuation
            word = word[:-1]
            
        while word and word[0] in ".,!?\"';:":
            left_punctuation = left_punctuation + word[0]
            word = word[1:]
            
        core_word = word.lower()
        
        if core_word in slang_lookup:
            replacement = slang_lookup[core_word]
            cleaned_words.append(f"{left_punctuation}{replacement}{right_punctuation}")
        else:
            cleaned_words.append(f"{left_punctuation}{word}{right_punctuation}")
            
    normalized_text = " ".join(cleaned_words)

    try:
        # 4. Correct overall grammar and contextual errors using LanguageTool
        corrected_text = tool.correct(normalized_text)
        
        if corrected_text:
            corrected_text = corrected_text.strip()
            
            # FORCE PROPER SENTENCE CASE (First letter capitalized, rest lowercase/clean)
            corrected_text = corrected_text[0].upper() + corrected_text[1:]
            
            # 🛡️ SMART TERMINAL PUNCTUATION PATIENT
            # Case A: User intentionally provided terminal punctuation, ensure it survived
            if ends_with_period or ends_with_exclamation or ends_with_question:
                if ends_with_period and not corrected_text.endswith("."):
                    corrected_text += "."
                elif ends_with_exclamation and not corrected_text.endswith("!"):
                    corrected_text += "!"
                elif ends_with_question and not corrected_text.endswith("?"):
                    corrected_text += "?"
            
            # Case B: User forgot punctuation entirely! Auto-inject a full stop.
            else:
                # Ensure we don't accidentally append a period onto trailing quotes or brackets
                if corrected_text[-1].isalnum():
                    corrected_text += "."
            
        return corrected_text
    except Exception as e:
        print(f"Error during NLP processing: {e}")
        return dirty_text