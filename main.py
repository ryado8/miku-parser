from pypdf import PdfReader
from src import section_parser
import re
import argparse
import csv

def extract_text_from_pdf(filename):
    reader = PdfReader(filename)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

def parse_sentences(text):
    text = re.sub(r"^.*?(?=1\.)", "", text)
    entries = re.split(r"(?<!\d)(?=\d{1,2}\.)", text)
    return entries[1:]

def parse_shadowing_entry(entry):
    entry = entry.strip()

    english_match = re.search(r"^\d+\.\s*(.*?)\.", entry)

    if not english_match:
        raise ValueError(f"Could not find English sentence: {entry}")

    english = english_match.group(1)

    japanese_text = entry[english_match.end():]

    japanese_sentences = [
        re.sub(r"\s+", " ", sentence).strip()
        for sentence in japanese_text.split("。")
        if sentence.strip()
    ]

    japanese_1 = japanese_sentences[0] if japanese_sentences else ""
    japanese_2 = japanese_sentences[1] if len(japanese_sentences) > 1 else ""

    return {
        "english": english,
        "japanese_1": japanese_1,
        "japanese_2": japanese_2,
    }

def parse_japanese_part_entry(entry):
    entry = entry.strip()

    entry = re.sub(r"^\d+\.\s*", "", entry)

    parts = [
        re.sub(r"\s+", " ", part).strip()
        for part in entry.split("。")
        if part.strip()
    ]

    japanese_1 = parts[0] if parts else ""
    japanese_2 = parts[1] if len(parts) > 1 else ""
    english = parts[2] if len(parts) > 2 else ""

    return {
        "english": english,
        "japanese_1": japanese_1,
        "japanese_2": japanese_2,
    }

def write_csv(sentences, filename):
    with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=["english", "japanese_1", "japanese_2"],
        )

        writer.writeheader()
        writer.writerows(sentences)

def main():
    parser = argparse.ArgumentParser(
        description="Extract English and Japanese sentences from a PDF."
    )

    parser.add_argument(
        "pdf_filename",
        help="Path to the PDF file",
    )

    args = parser.parse_args()

    pdf_text = extract_text_from_pdf(args.pdf_filename)

    shadowing = section_parser.extract_shadowing_section(pdf_text)
    japanese_part = section_parser.extract_japanese_section(pdf_text)

    shadowing_entries = parse_sentences(shadowing)
    japanese_part_entries = parse_sentences(japanese_part)

    parsed_shadowing = [
        parse_shadowing_entry(entry)
        for entry in shadowing_entries
    ]

    parsed_japanese_part = [
        parse_japanese_part_entry(entry)
        for entry in japanese_part_entries
    ]

    if len(parsed_shadowing) != 15:
        raise ValueError(
            f"Expected 15 Shadowing entries, got {len(parsed_shadowing)}"
        )

    if len(parsed_japanese_part) != 5:
        raise ValueError(
            f"Expected 5 Japanese Part entries, got {len(parsed_japanese_part)}"
        )

    all_sentences = parsed_shadowing + parsed_japanese_part

    if len(all_sentences) != 20:
        raise ValueError(
            f"Expected 20 total sentences, got {len(all_sentences)}"
        )

    output_filename = args.pdf_filename.rsplit(".", 1)[0] + ".csv"

    write_csv(all_sentences, output_filename)

    print(f"Created {output_filename}")


if __name__ == "__main__":
    main()