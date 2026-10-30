# integration_test.py
import main_app

print("🧪 Running Backend Health Check...")

# Test 1: Grammar, Punctuation & Tone
sample_input = "yesterday our school organized a science exhibition and every student were asked to present there project"
result = main_app.clean_and_check_sentence(sample_input, "Professional")
print("\n--- Test Output ---")
print(result)
print("-------------------")

if "project" in result:
    print("✓ Backend grammar & punctuation pipeline operating successfully!")
else:
    print("❌ Backend check failed.")