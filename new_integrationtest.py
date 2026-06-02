# new_integrationtest.py
from word_analyzer import count_words_and_chars, find_misspelled_words
from nlp_brain import fix_sentence_context

def run_integration_test(text):
    print("--- Running Full Integration Test ---")
    print(f"Testing text: '{text}'\n")
    
    # 1. Run Developer B's Word Analyzer
    metrics = count_words_and_chars(text)
    print(f"Word Count: {metrics['word_count']}")
    print(f"Character Count: {metrics['character_count']}")
    
    misspelled = find_misspelled_words(text)
    print(f"Misspelled Words Found: {misspelled}")
    
    # 2. Run Developer A's AI Engine
    print("\n--- Running AI Context Engine ---")
    corrected = fix_sentence_context(text)
    print(f"Fixed Text: '{corrected}'")

if __name__ == "__main__":
    sample = "I stuy englh"
    run_integration_test(sample)