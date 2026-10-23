
# 🔐 PrivAI — Offline Intelligent Document Privacy Shield

**Detect sensitive information. Protect it locally.**

PrivAI is a privacy-focused prototype designed to detect and redact Personally Identifiable Information (PII) from text. It uses local pattern matching and simple contextual heuristics without calling external AI APIs.

## 🚀 Features

- 🔍 Detect supported PII patterns in text
- 🛡️ Redact detected information
- 📋 Display a detection report with PII types and detected values
- 🎲 Load different sample sentences for testing
- 📊 Evaluate the baseline using precision, recall, F1-score, and TP/FP/FN counts
- 🔒 Process text locally when running the app on your own computer
- 🧪 Include synthetic smoke tests for basic evaluation

## 🧰 Technology Stack

- Python
- Streamlit
- Pandas
- Regular expressions and rule-based detection

## 📂 Project Structure

```text
PrivAI/
├── app.py
├── app_core.py
├── evaluate.py
├── requirements.txt
├── README.md
├── data/
│   ├── sample.txt
│   └── dataset_note.md
└── run_windows.bat
```

*Adjust this structure if your actual repository differs.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/PrivAI.git
cd PrivAI
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment (optional but recommended)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## 📊 Evaluation

The evaluation interface uses a small set of synthetic test cases and reports:

- **Precision:** Proportion of detected items that were correct.
- **Recall:** Proportion of expected items that were detected.
- **F1-score:** Harmonic mean of precision and recall.
- **TP:** True positives.
- **FP:** False positives.
- **FN:** False negatives.

These results are preliminary smoke-test measurements, not validated real-world accuracy. The test set is small and does not establish performance on unseen documents.

## 🧠 Current Detection Scope

The baseline is designed to detect supported patterns such as:

- Email addresses
- Indian mobile numbers
- Aadhaar-like 12-digit numbers
- PAN-like identifiers
- Names matching simple contextual heuristics

Detection depends on the implementation in `app_core.py`. Some names, addresses, group IDs, and other contextual information may be missed. False positives are also possible.

## 🔐 Privacy and Limitations

- When run locally, the prototype processes text in the local Python application and does not call external AI APIs.
- Avoid entering real sensitive information in demonstrations.
- If deployed on a hosting platform, text is processed by the hosted application environment rather than your own computer.
- The current implementation is a rule-based baseline, not a fine-tuned Small Language Model (SLM).

## 🔮 Future Improvements

- Build a larger, labelled PII dataset.
- Improve context-aware detection.
- Evaluate precision, recall, and F1-score on a representative test set.
- Add document upload and additional PII categories.
- Explore a locally deployed SLM.
- Investigate model optimization using quantization or distillation.

---

**PrivAI — Detect sensitive information. Protect it locally.**
