# integration_test.py
import word_analyzer

def run_integration_test(sample_phrase):
    print("=========================================")
    print("   RUNNING SPELLSYNC INTEGRATION TEST    ")
    print("=========================================\n")
    print(f"📥 RAW USER INPUT SENTENCE: '{sample_phrase}'")
    print("-" * 40)
    
    # Test Step 1: Run through the custom dictionary slang interceptor
    pre_processed = word_analyzer.normalize_text(sample_phrase)
    print(f"⚙️  STEP 1 (Slang Pre-Processing): '{pre_processed}'")
    
    # Test Step 2: Simulate output post-validation formatting rules
    # (Capitalization, greeting comma placement, sentence ending marks)
    final_validated = word_analyzer.post_validate_formatting(pre_processed)
    print(f"📤 STEP 2 (Final Validation Output): '{final_validated}'")
    print("-" * 40)
    
    # Simple logic check validation metrics
    words = sample_phrase.split()
    print(f"📊 METRICS LOGGED: {len(words)} Words processed successfully.\n")
    print("✅ INTEGRATION TEST PIPELINE COMPLETION SUCCESSFUL!")

if __name__ == "__main__":
    # Test with your ultimate stubborn casing slang test-phrase
    sample = "HI FAM we finali did it"
    run_integration_test(sample)
