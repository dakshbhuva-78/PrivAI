"""Small smoke-test evaluation on synthetic examples only; not a general accuracy claim."""
from app_core import detect

CASES = [
    ("Email: test@example.com", {"EMAIL"}),
    ("Contact: +91-9876543210", {"PHONE"}),
    ("ID: 1234 5678 9012", {"AADHAAR_LIKE_ID"}),
    ("Name: Rahul Patel, email rahul@example.com", {"NAME (heuristic)", "EMAIL"}),
]
labels = {"EMAIL", "PHONE", "AADHAAR_LIKE_ID", "PAN_LIKE_ID", "NAME (heuristic)"}
tp=fp=fn=0
for text, expected in CASES:
    got={x["type"] for x in detect(text)}
    tp += len(got & expected)
    fp += len(got - expected)
    fn += len(expected - got)
    print(f"TEXT: {text}\n expected={sorted(expected)}\n detected={sorted(got)}\n")
precision=tp/(tp+fp) if tp+fp else 0
recall=tp/(tp+fn) if tp+fn else 0
f1=2*precision*recall/(precision+recall) if precision+recall else 0
print("SYNTHETIC SMOKE TEST ONLY — not a validated benchmark")
print(f"TP={tp} FP={fp} FN={fn}")
print(f"Precision={precision:.3f} Recall={recall:.3f} F1={f1:.3f}")
print("These results cover only the tiny examples above; do not present them as real-world model accuracy.")
