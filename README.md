# 🧠 Adobe India Hackathon – “Connecting the Dots” Challenge

By: Awesome Hackers  
Track: PDF Structure & Intelligence  
Submission: Round 1A ✅ + Round 1B ✅  
Platform: Docker (AMD64, CPU-only, Offline)

---

## 📘 ROUND 1A – Document Outline Extractor

### 🎯 Goal:
Given a raw PDF, extract its **title** and hierarchical **headings** (H1, H2, H3) with **page numbers** in under 10 seconds.

### 🛠 How It Works:
- Uses **PyMuPDF (fitz)** to extract structured text
- Applies font-size + bold heuristics to determine heading levels
- Skips empty/junk blocks for cleaner outlines

### 📤 Output Format:
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History", "page": 3 }
  ]
}
```
## 🧠 ROUND 1B – Persona-Driven Document Intelligence
### 🎯 Goal:
Given a set of PDFs, a persona, and their job-to-be-done, extract and rank the most relevant sections + summary for that persona.

## 📥 Input:
- input/ folder with PDFs
- persona_config.json with format:
```json
{
  "persona": "Student",
  "job_to_be_done": "Summarize reaction kinetics for exam",
  "documents": ["chem1.pdf", "chem2.pdf"]
}
```
## 📤 Output Format:
```json
{
  "metadata": { ... },
  "extracted_sections": [
    {
      "document": "chem1.pdf",
      "page": 4,
      "section_title": "Reaction Kinetics Overview",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "chem1.pdf",
      "refined_text": "Rate laws describe how reaction rate depends on concentration...",
      "page": 4
    }
  ]
}
```
# 🐳 Docker Instructions
## Build Image:
### Round 1A:
```json
docker build --platform linux/amd64 -t pdf_outline_extractor .
```
### Round 1B:
```json
docker build --platform linux/amd64 -t pdf_persona_engine .
```
## Run Container:
### Round 1A:
```json
docker run --rm \
-v ${PWD}/input:/app/input \
-v ${PWD}/output:/app/output \
--network none \
pdf_outline_extractor
```
### Round 1B:
```json 
docker run --rm \
-v ${PWD}/input:/app/input \
-v ${PWD}/output:/app/output \
-v ${PWD}/persona_config.json:/app/persona_config.json \
--network none \
pdf_persona_engine
```

## 📂 Folder Structure:
```json
adobe_hackathon/
├── app/
│   ├── extractor.py         # Round 1A
│   └── persona_engine.py    # Round 1B
├── input/                   # Place PDFs here
├── output/                  # Output JSONs
├── persona_config.json      # Round 1B input config
├── Dockerfile
└── README.md
```

## ✅ Constraints Met

| Constraint        | Status                                 |
| ----------------- | -------------------------------------- |
| ⏱ Execution Time  | ✅ < 10s (1A), < 60s (1B)               |
| 📦 Model Size     | ✅ No model used (1A), < 1GB logic (1B) |
| 💻 CPU-only       | ✅ Fully CPU-compatible                 |
| 🌐 Offline Mode   | ✅ No internet dependencies             |
| 🐳 Docker (amd64) | ✅ Compatible & tested                  |


## Authors:
- Kartik Singh
- Kanika Goyal
- Krishna Gupta

## 💬 Note for Judges:
This solution is modular, fast, and compliant with all challenge rules. No internet. No bloat.
Just clean AI-powered document understanding — built to win 🏆