import re
PATTERNS = [
    ("EMAIL", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    ("PHONE", re.compile(r"(?<!\w)(?:\+?91[\s-]?)?[6-9]\d{9}(?!\w)")),
    ("AADHAAR_LIKE_ID", re.compile(r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)")),
    ("PAN_LIKE_ID", re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b", re.I)),
]
NAME_PATTERN = re.compile(r"\b(?:Mr\.?|Mrs\.?|Ms\.?|Name\s*:\s*)\s*([A-Z][a-z]{1,20}\s+[A-Z][a-z]{1,20})\b")
def detect(text):
    found=[]; occupied=[]
    for label, pat in PATTERNS:
        for m in pat.finditer(text):
            found.append({"type":label,"value":m.group(),"start":m.start(),"end":m.end()})
            occupied.append((m.start(),m.end()))
    for m in NAME_PATTERN.finditer(text):
        s,e=m.span(1)
        if not any(s < oe and e > os_ for os_,oe in occupied):
            found.append({"type":"NAME (heuristic)","value":m.group(1),"start":s,"end":e})
    return sorted(found,key=lambda x:x["start"])
def redact(text, findings):
    for item in sorted(findings,key=lambda x:x["start"],reverse=True):
        label=item["type"].replace(" (heuristic)","")
        text=text[:item["start"]]+f"[{label}]"+text[item["end"]:]
    return text
