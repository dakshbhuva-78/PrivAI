# PrivAI — Offline PII Detection & Redaction (Baseline Prototype)

## What it does
A small local demo that detects common PII patterns in pasted text and produces a redacted version plus a detection report.

## Important honesty note
This is a **baseline prototype**, not a fine-tuned Small Language Model (SLM). It currently uses regular expressions for email, Indian mobile number, Aadhaar-like and PAN-like patterns, plus a simple contextual name heuristic. It is useful to demonstrate the workflow and identify the next engineering steps, but it is not production-grade and does not guarantee privacy/security for real records.

## Run locally
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   streamlit run app.py
   # Optional tiny synthetic smoke test:
   python evaluate.py
   ```
4. Open the local URL printed in the terminal. After dependencies are installed, the app does not call external AI APIs.

## Demo sample
`Name: Rahul Patel can be contacted at rahul.patel@example.com or +91-9876543210. ID: 1234 5678 9012.`

## Current limitations
- Name detection is a simple heuristic and may miss names or flag incorrectly.
- Address detection and document/PDF upload are not implemented.
- No SLM fine-tuning, distillation or quantization has been done yet.
- Do not use with real sensitive documents.

## Next steps
- Build a labeled PII dataset and train/test split.
- Add a proper local NER model and compare it with this baseline.
- Report precision, recall and F1 on a held-out dataset.
- Add PDF/DOCX input, manual review, and stronger redaction validation.
