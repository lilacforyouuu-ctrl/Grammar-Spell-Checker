import language_tool_python

try:
    # Initialize the engine
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

    try:
        # 4. Correct text using context
        corrected_text = tool.correct(dirty_text)
        return corrected_text
    except Exception as e:
        print(f"Error during NLP processing: {e}")
        return dirty_text