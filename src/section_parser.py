def extract_shadowing_section(text):
    start = text.index("Shadowing")
    end = text.index("Japanese part")

    return text[start:end]