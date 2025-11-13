# config.py

CHROMEDRIVER_PATH = r"C:\webdrivers\chromedriver.exe"
HEADLESS = False
SCROLL_PAUSE = 1.5
MAX_SCROLLS = 25
OUTPUT_CSV = "twitter_legal_foryou.csv"

COOKIES_DIR = "cookies"  

LEGAL_KEYWORDS = [
    # ⚖️ Core Legal Terms
    "law", "legal", "legislation", "judicial", "justice", "judiciary", "rights",
    "fundamental rights", "constitutional", "constitution", "fundamental duty",

    # 📜 IPC / Criminal / Penal
    "ipc", "crpc", "penal", "section", "bail", "fir", "crime", "criminal",
    "offence", "charge", "accused", "convict", "sentence", "custody", "arrest",
    "remand", "trial", "witness", "evidence", "investigation", "prosecution",
    "judgment", "verdict", "hearing", "petition", "appeal", "order", "rule",
    "notification", "act", "amendment", "ordinance", "lawyer", "advocate",

    # ⚖️ Courts & Judicial Bodies
    "court", "supreme court", "high court", "district court", "magistrate",
    "sessions court", "bench", "tribunal", "nclt", "nclat", "cat", "afta",
    "cbi court", "consumer court", "labour court",

    # 💼 Corporate / Economic Law
    "insolvency", "bankruptcy", "liquidation", "merger", "acquisition",
    "nclt order", "nclat order", "company act", "contract act",
    "arbitration", "mca", "sebi", "cibil", "gst", "income tax",

    # 🚨 Police / Enforcement / Crime
    "police", "cybercrime", "terror", "blast", "attack", "scam", "fraud",
    "money laundering", "ed", "cbi", "ncb", "nia", "raid", "confession",
    "investigation", "charge sheet", "warrant",

    # 🏛️ Miscellaneous Legal Context
    "public interest litigation", "pil", "contempt", "affidavit", "notice",
    "summons", "probation", "juvenile", "bail plea", "custody case",
    "litigation", "lawsuit", "regulation", "policy", "mandamus", "habeas corpus",
    "tribunal", "sentence", "fine", "penalty", "license", "permit"
]


