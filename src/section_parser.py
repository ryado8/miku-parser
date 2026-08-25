def extract_shadowing_section(text):
    start = text.find("Shadowing")
    end = text.find("Japanese part", start)

    return text[start:end]

def extract_japanese_section(text):
    return text[text.find("Japanese part", text.find("Shadowing")):]
