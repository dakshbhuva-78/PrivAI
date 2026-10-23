
import random
import streamlit as st

st.set_page_config(
    page_title="PrivAI | Offline PII Shield",
    page_icon="🔐",
    layout="wide"
)

from app_core import detect, redact

st.title("🔐 PrivAI")
st.caption(
    "Offline Intelligent Document Privacy Shield • Local baseline prototype"
)

st.info(
    "Privacy note: this demo processes text in this running Python app. "
    "It makes no API or cloud calls. This prototype uses pattern matching "
    "plus a simple name heuristic; it is not yet a fine-tuned SLM."
)

# Different sample sentences for testing
SAMPLE_TEXTS = [
    (
        "Name: Rahul Patel can be contacted at "
        "rahul.patel@example.com or +91-9876543210. "
        "ID: 1234 5678 9012."
    ),
    (
        "Name: Priya Sharma. Her email is priya.sharma@gmail.com "
        "and her phone number is +91-8765432109."
    ),
    (
        "Name: Amit Shah. Contact: amit.shah@example.com. "
        "PAN ID: ABCDE1234F."
    ),
    (
        "Hello, I am Daksh Bhuva from group DBEUX, "
        "group ID ERF232. My email is dakshbh23@gmail.com."
    ),
    (
        "Name: Neha Verma. Email: neha.verma@example.com. "
        "Mobile: 9876543210. Aadhaar ID: 2345 6789 0123."
    ),
    (
        "Name: Karan Mehta can be reached at "
        "karan.mehta@example.com or +91-9123456780. "
        "PAN ID: ABCDE1234F."
    ),
]

# Initialize the input text on the first run
if "input_text" not in st.session_state:
    st.session_state.input_text = SAMPLE_TEXTS[0]


def load_sample():
    current_text = st.session_state.input_text

    # Choose a sample different from the current text
    choices = [
        sample for sample in SAMPLE_TEXTS
        if sample != current_text
    ]

    st.session_state.input_text = random.choice(choices)

    # Clear previous results
    st.session_state["findings"] = []
    st.session_state["redacted"] = None


text = st.text_area(
    "Paste sample text",
    key="input_text",
    height=160
)

c1, c2 = st.columns(2)

with c1:
    if st.button(
        "Detect & redact",
        type="primary",
        use_container_width=True
    ):
        findings = detect(text)
        st.session_state["findings"] = findings
        st.session_state["redacted"] = redact(text, findings)

with c2:
    st.button(
        "Load sample",
        use_container_width=True,
        on_click=load_sample
    )

# Display detection results
if (
    "findings" in st.session_state
    and st.session_state.get("redacted") is not None
):
    findings = st.session_state["findings"]

    st.subheader("Redacted output")
    st.code(st.session_state["redacted"] or "No output yet")

    st.subheader(
        f"Detection report ({len(findings)} finding(s))"
    )

    if findings:
        st.dataframe(
            [
                {
                    "PII type": item["type"],
                    "Detected value": item["value"]
                }
                for item in findings
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.write("No supported PII patterns detected.")

st.divider()

st.caption(
    "Current baseline supports email, Indian mobile number, "
    "Aadhaar-like 12-digit number, PAN-like ID, and names after "
    "simple context cues. Results can be missed or incorrectly "
    "flagged; do not use with real sensitive data."
)