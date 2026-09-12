import os
import language_tool_python as ltp

# Force Java path routing inside the brain engine
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-17"

try:
    # Initialize the local standalone language engine
    tool = ltp.LanguageTool('en-US')
except Exception as e:
    print(f"Engine local startup warning: {e}")
    tool = None

def fix_sentence_context(text):
    if not tool:
        return text
    try:
        # Split text by punctuation to isolate sentences
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        corrected_sentences = []

        for sentence in sentences:
            current = sentence
            # Run up to 3 passes per sentence so rules don't collide
            for _ in range(3):
                matches = tool.check(current)
                if not matches:
                    break
                current = ltp.utils.correct(current, matches)
            corrected_sentences.append(current)

        return " ".join(corrected_sentences)
    except Exception as e:
        print(f"Processing error: {e}")
        return text