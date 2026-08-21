from pypdf import PdfReader
from src import section_parser

def extract_text_from_pdf(filename):
    reader = PdfReader(filename)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

text = extract_text_from_pdf('pdfs/1-3.pdf')

def extract_shadowing_section(text):
    start = text.find("Shadowing")
    end = text.find("Japanese part", start)

    return text[start:end]

shadowing = extract_shadowing_section(text)

print(shadowing)