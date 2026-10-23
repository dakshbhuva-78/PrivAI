
import random
import streamlit as st
import pandas as pd

from app_core import detect, redact

st.set_page_config(
    page_title="PrivAI | Offline PII Shield",
    page_icon="🔐",
    layout="wide"
)

# -------------------- SAMPLE DATA --------------------

SAMPLE_TEXTS = [
    "Name: Rahul Patel can be contacted at rahul.patel@example.com or +91-9876543210. ID: 1234 5678 9012.",
    "Name: Priya Sharma. Her email is priya.sharma@gmail.com and her phone number is +91-8765432109.",
    "Name: Amit Shah. Contact: amit.shah@example.com. PAN ID: ABCDE1234F.",
    "Hello, I am Daksh Bhuva from group DBEUX, group ID ERF232. My email is dakshbh23@gmail.com.",
    "Name: Neha Verma. Email: neha.verma@example.com. Mobile: 9876543210. Aadhaar ID: 2345 6789 0123.",
    "Name: Karan Mehta can be reached at karan.mehta@example.com or +91-9123456780. PAN ID: ABCDE1234F."
]

# Synthetic examples with expected PII types
CASES = [
    ("Email: test@example.com", {"EMAIL"}),
    ("Contact: +91-9876543210", {"PHONE"}),
    ("ID: 1234 5678 9012", {"AADHAAR_LIKE_ID"}),
    (
        "Name: Rahul Patel, email rahul@example.com",
        {"NAME (heuristic)", "EMAIL"}
    ),
]

# -------------------- SESSION STATE --------------------

if "input_text" not in st.session_state:
    st.session_state.input_text = SAMPLE_TEXTS[0]

if "findings" not in st.session_state:
    st.session_state.findings = []

if "redacted" not in st.session_state:
    st.session_state.redacted = None


def load_sample():
    current = st.session_state.input_text
    choices = [sample for sample in SAMPLE_TEXTS if sample != current]

    st.session_state.input_text = random.choice(choices)
    st.session_state.findings = []
    st.session_state.redacted = None


def evaluate_model():
    tp = fp = fn = 0
    rows = []

    for text, expected in CASES:
        detected = detect(text)
        actual = {item["type"] for item in detected}

        case_tp = len(actual & expected)
        case_fp = len(actual - expected)
        case_fn = len(expected - actual)

        tp += case_tp
        fp += case_fp
        fn += case_fn

        rows.append({
            "Test input": text,
            "Expected types": ", ".join(sorted(expected)),
            "Detected types": ", ".join(sorted(actual)) or "None",
            "TP": case_tp,
            "FP": case_fp,
            "FN": case_fn,
            "Result": "Pass" if actual == expected else "Review"
        })

    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "rows": rows
    }


# -------------------- HEADER --------------------

st.title("🔐 PrivAI")
st.caption("Offline Intelligent Document Privacy Shield")

st.info(
    "Privacy-first baseline prototype. Detection uses local pattern "
    "matching and a simple name heuristic. No external AI API is used. "
    "This is not yet a fine-tuned SLM."
)

demo_tab, evaluation_tab, about_tab = st.tabs([
    "🛡️ Detection Workspace",
    "📊 Evaluation",
    "ℹ️ About PrivAI"
])

# -------------------- DETECTION WORKSPACE --------------------

with demo_tab:
    st.subheader("Detect and redact sensitive information")
    st.write(
        "Paste text below or load a sample to test the supported PII patterns."
    )

    text = st.text_area(
        "Input text",
        key="input_text",
        height=180,
        placeholder="Paste text containing test information..."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔍 Detect & Redact",
            type="primary",
            use_container_width=True
        ):
            findings = detect(text)
            st.session_state.findings = findings
            st.session_state.redacted = redact(text, findings)

    with col2:
        st.button(
            "🎲 Load Different Sample",
            on_click=load_sample,
            use_container_width=True
        )

    if st.session_state.redacted is not None:
        findings = st.session_state.findings

        st.divider()
        st.subheader("Redacted output")

        st.code(
            st.session_state.redacted or "No output generated.",
            language="text"
        )

        st.subheader("Detection report")

        m1, m2 = st.columns(2)
        m1.metric("Findings detected", len(findings))
        m2.metric(
            "PII types found",
            len({item["type"] for item in findings})
        )

        if findings:
            st.dataframe(
                pd.DataFrame([
                    {
                        "PII type": item["type"],
                        "Detected value": item["value"]
                    }
                    for item in findings
                ]),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning(
                "No supported PII patterns detected. "
                "This does not guarantee that the text contains no PII."
            )

# -------------------- EVALUATION --------------------

with evaluation_tab:
    st.subheader("Baseline evaluation")
    st.write(
        "Run the built-in synthetic test cases to compare expected PII "
        "types with the types detected by the current implementation."
    )

    st.warning(
        "These are small synthetic smoke tests, not a validated benchmark. "
        "The metrics below must not be described as real-world accuracy."
    )

    if st.button("▶ Run Evaluation", type="primary"):
        st.session_state.evaluation_results = evaluate_model()

    if "evaluation_results" in st.session_state:
        result = st.session_state.evaluation_results

        c1, c2, c3 = st.columns(3)
        c1.metric("Precision", f"{result['precision']:.1%}")
        c2.metric("Recall", f"{result['recall']:.1%}")
        c3.metric("F1-score", f"{result['f1']:.1%}")

        c4, c5, c6 = st.columns(3)
        c4.metric("True positives (TP)", result["tp"])
        c5.metric("False positives (FP)", result["fp"])
        c6.metric("False negatives (FN)", result["fn"])

        st.subheader("Test case results")
        st.dataframe(
            pd.DataFrame(result["rows"]),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Precision = TP / (TP + FP). Recall = TP / (TP + FN). "
            "F1-score is the harmonic mean of precision and recall. "
            "Metrics are calculated across the listed synthetic examples."
        )

# -------------------- ABOUT --------------------

with about_tab:
    st.subheader("Project overview")

    st.markdown("""
    **Objective:** Detect and redact sensitive information before it
    is shared or processed elsewhere.

    **Current supported patterns**
    - Email addresses
    - Indian mobile numbers
    - Aadhaar-like 12-digit numbers
    - PAN-like IDs
    - Names matching simple context cues

    **Current limitations**
    - Names, addresses, group IDs, and other contextual information may be missed.
    - False positives are possible.
    - No fine-tuned SLM has been integrated yet.

    **Future improvements**
    - Build a larger manually labelled dataset.
    - Evaluate precision, recall, F1-score and per-category results.
    - Improve contextual PII detection.
    - Explore a locally deployed Small Language Model (SLM).
    """)

st.divider()
st.caption(
    "PrivAI • TECHVERSE 2026 • BUDDHI — AI Model Building | "
    "Do not use real sensitive data in this demonstration."
)