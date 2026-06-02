from spellchecker import SpellChecker
import re

def count_words_and_chars(text):
    """
    Task 1: Counts exact words and characters.
    """
    char_count = len(text)
    
    # split() automatically handles multiple spaces beautifully
    words = text.split()
    word_count = len(words)
    
    return {
        "word_count": word_count,
        "character_count": char_count
    }


def find_misspelled_words(text):
    """
    Task 2: Finds individual misspelled words.
    """
    if not text.strip():
        return []

    spell = SpellChecker()
    
    # This regex pulls out just words and ignores punctuation (like periods)
    words_only = re.findall(r'\b\w+\b', text.lower())
    
    # Check which words are misspelled
    misspelled = spell.unknown(words_only)
    
    return list(misspelled)

import re
from spellchecker import SpellChecker

def count_words_and_chars(text):
    """
    Task 1: Counts exact words and characters.
    """
    char_count = len(text)
    
    # split() automatically handles multiple spaces beautifully
    words = text.split()
    word_count = len(words)
    
    # This return MUST be inside this function block (indented)
    return {
        "word_count": word_count,
        "character_count": char_count
    }


def find_misspelled_words(text):
    """
    Task 2: Finds individual misspelled words.
    """
    if not text.strip():
        return []
        
    spell = SpellChecker()
    words_only = re.findall(r'\b\w+\b', text.lower())
    misspelled = spell.unknown(words_only)
    return list(misspelled)


# --- This test block always goes at the very bottom of the file ---
if __name__ == "__main__":
    sample_text = "I stuy englh"
    print("--- Developer B Test ---")
    
    # Test the counter dictionary output
    metrics = count_words_and_chars(sample_text)
    print("Metrics:", metrics)
    
    # Test the misspelling list output
    print("Misspelled Words:", find_misspelled_words(sample_text))