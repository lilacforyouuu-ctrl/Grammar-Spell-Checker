# Import your functions from word_analyzer.py
from word_analyzer import count_words_and_chars, find_misspelled_words

def run_integration_test(text):
    print("--- Running Integration Test ---")
    print(f"Testing text: '{text}'\n")
    
    # Run the counter and read from its dictionary keys
    metrics = count_words_and_chars(text)
    print(f"Word Count: {metrics['word_count']}")
    print(f"Character Count: {metrics['character_count']}")
    
    # Run the spellchecker
    misspelled = find_misspelled_words(text)
    print(f"Misspelled Words Found: {misspelled}")

if __name__ == "__main__":
    sample = "I stuy englh"
    run_integration_test(sample)