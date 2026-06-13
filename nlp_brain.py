import os
import language_tool_python

# Force Java path routing inside the brain engine
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-17"

try:
    # Initialize the local standalone language engine
    tool = language_tool_python.LanguageTool('en-US')
except Exception as e:
    print(f"Engine local startup warning: {e}")
    tool = None

def fix_sentence_context(text):
    if not tool:
        return text
    try:
        # Pass the dirty text directly to the native grammar engine
        return tool.correct(text)
    except Exception as e:
        print(f"Processing error: {e}")
        return text
