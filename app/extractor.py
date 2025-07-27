import fitz  # PyMuPDF
import os
import json
import re


def contains_japanese(text):
    # Matches Japanese Kanji, Hiragana, Katakana
    return re.search(r'[\u3040-\u30ff\u4e00-\u9faf]', text)


def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title = os.path.basename(pdf_path).replace(".pdf", "")
    headings = []

    seen_headings = set()

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line["spans"]
                if not spans:
                    continue

                text = " ".join([span["text"] for span in spans]).strip()

                # ✨ Multilingual-friendly checks
                if not text.strip():
                    continue
                if not re.search(r'[A-Za-z]', text) and not contains_japanese(text):
                    continue
                if text in seen_headings:
                    continue

                font_size = spans[0]["size"]
                font_flags = spans[0]["flags"]
                is_bold = font_flags & 2 != 0  # bold = 2nd bit in flags

                # Heading level logic
                if font_size > 16 or (font_size > 13 and is_bold):
                    level = "H1"
                elif font_size > 13:
                    level = "H2"
                elif font_size > 11:
                    level = "H3"
                else:
                    continue

                headings.append({
                    "level": level,
                    "text": text,
                    "page": page_num
                })
                seen_headings.add(text)

    return {
        "title": title,
        "outline": headings
    }


def main():
    input_dir = os.path.join(os.path.dirname(__file__), "../input")
    output_dir = os.path.join(os.path.dirname(__file__), "../output")

    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            result = extract_outline(pdf_path)
            output_path = os.path.join(output_dir, file.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

    print("✅ Outline extraction complete.")


if __name__ == "__main__":
    main()
