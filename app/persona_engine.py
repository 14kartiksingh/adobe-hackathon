import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_persona_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_pages_text(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            pages.append({"page": page_num, "text": text})
    return pages


def compute_relevance(pages, prompt):
    texts = [p["text"] for p in pages]
    tfidf = TfidfVectorizer().fit_transform([prompt] + texts)
    scores = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    return scores


def process_documents(config, input_dir):
    metadata = {
        "persona": config["persona"],
        "job": config["job_to_be_done"],
        "documents": config["documents"],
        "timestamp": str(datetime.now())
    }

    extracted_sections = []
    subsection_analysis = []

    for doc_name in config["documents"]:
        pdf_path = os.path.join(input_dir, doc_name)
        pages = extract_pages_text(pdf_path)
        relevance_scores = compute_relevance(pages, config["job_to_be_done"])

        ranked_pages = sorted(zip(pages, relevance_scores), key=lambda x: x[1], reverse=True)
        top_sections = ranked_pages[:3]  # Top 3 relevant pages

        for rank, (page_data, score) in enumerate(top_sections, start=1):
            extracted_sections.append({
                "document": doc_name,
                "page": page_data["page"],
                "section_title": page_data["text"][:50] + "...",
                "importance_rank": rank
            })

            subsection_analysis.append({
                "document": doc_name,
                "refined_text": page_data["text"][:300],
                "page": page_data["page"]
            })

    return {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }


def main():
    input_dir = "./input"
    output_dir = "./output"
    config_path = "./persona_config.json"

    os.makedirs(output_dir, exist_ok=True)

    config = load_persona_config(config_path)
    result = process_documents(config, input_dir)

    output_file = os.path.join(output_dir, "persona_output.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("✅ persona_output.json generated in output/")


if __name__ == "__main__":
    main()
