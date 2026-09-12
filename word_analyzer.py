# word_analyzer.py
import re

def normalize_text(text):
    """
    Cleans raw conversational shorthand, structures grammar frameworks, 
    and manually resolves capitalization exceptions like 'HI FAM'.
    """
    if not text.strip():
        return ""
        
    words = text.split()
    cleaned_input_words = []
    
    for idx, word in enumerate(words):
        # Isolate the core word from common surrounding punctuation
        base = word.strip(".,!?\"'").lower()
        
        # Explicit slang mapping matrix
        if base in ["hi", "hii", "hey"]:
            cleaned_word = "hi," if idx == 0 else "hi"
        elif base in ["fam", "buddies", "buddy"]:
            cleaned_word = "fam"
        elif base in ["finali", "finallyy", "flnali"]:
            cleaned_word = "finally"
        elif base == "i":
            cleaned_word = "I"
        else:
            cleaned_word = base
            
        cleaned_input_words.append(cleaned_word)
        
    processed_input = " ".join(cleaned_input_words)
    return processed_input

def post_validate_formatting(corrected_text):
    """
    Cleans up trailing formatting artifacts and ensures structural punctuation standards.
    """
    if not corrected_text:
        return ""
        
    words = corrected_text.split()
    final_processed_words = []
    
    for idx, word in enumerate(words):
        base = word.strip(".,!?\"'")
        
        # Re-enforce rules on post-processed strings
        if base.lower() == "hi" and idx == 0:
            word = "Hi,"
        elif base.lower() == "fam" and idx == 1:
            word = "fam"
        elif base.lower() == "i":
            word = "I"
            
        final_processed_words.append(word)
        
    result = " ".join(final_processed_words)
    
    # Capitalize the absolute start of the sentence string
    if result:
        result = result[0].upper() + result[1:]
        
    # Append safe ending punctuation if completely missing
    if result and result[-1] not in ['.', '!', '?']:
        result += '.'
        
    return result
