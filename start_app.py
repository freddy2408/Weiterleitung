import sqlite3, uuid, random
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Studie Start", page_icon="▶️", layout="centered")

BOT_A_URL = "https://verhandlung.streamlit.app"
BOT_B_URL = "https://verhandlung123.streamlit.app"
DB_PATH = "assignments.sqlite3"


# ----------------------------
# DB helpers
# ----------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            pid TEXT PRIMARY KEY,
            order_code TEXT,
            created_ts TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_or_create_assignment(pid: str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT order_code FROM assignments WHERE pid = ?", (pid,))
    row = c.fetchone()

    if row:
        order_code = row[0]
    else:
        order_code = random.choice(["AB", "BA"])
        c.execute(
            "INSERT INTO assignments (pid, order_code, created_ts) VALUES (?, ?, ?)",
            (pid, order_code, datetime.utcnow().isoformat())
        )
        conn.commit()

    conn.close()
    return order_code


# ----------------------------
# 1) pid aus URL oder neu generieren
# ----------------------------
pid = st.query_params.get("pid", None)
if not pid:
    pid = f"p-{uuid.uuid4().hex[:10]}"
    st.query_params["pid"] = pid

# 2) Reihenfolge fixieren (persistiert)
order_code = get_or_create_assignment(pid)
st.query_params["order"] = order_code


# ----------------------------
# 3) Ziel-URL bestimmen (nur 1 Button)
# ----------------------------
if order_code == "AB":
    next_url = f"{BOT_A_URL}?pid={pid}&order=AB&step=1"
else:
    next_url = f"{BOT_B_URL}?pid={pid}&order=BA&step=1"

next_label = "Weiter zu Verhandlung 1"


# ----------------------------
# 4) UI / Layout
# ----------------------------
st.markdown(
    """
    <style>
      .subtitle { color: rgba(49, 51, 63, 0.7); margin-top: 0.2rem; }
      .badge {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        border: 1px solid rgba(49, 51, 63, 0.18);
        font-size: 0.85rem;
        color: rgba(49, 51, 63, 0.8);
        background: rgba(255,255,255,0.55);
      }
      .card {
        border: 1px solid rgba(49, 51, 63, 0.15);
        border-radius: 16px;
        padding: 18px 18px;
        background: rgba(255,255,255,0.6);
      }
      .meta {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        font-size: 0.9rem;
        color: rgba(49, 51, 63, 0.75);
        margin-top: 8px;
      }
      div.stLinkButton > a {
        padding: 0.9rem 1.0rem !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

left, right = st.columns([0.88, 0.12], vertical_alignment="top")
with left:
    st.title("Start der Verhandlung")
    st.markdown('<div class="subtitle">Klicken Sie auf „Weiter zu Verhandlung 1“, um die erste Verhandlung zu starten.</div>', unsafe_allow_html=True)
    st.markdown('<span class="badge">Teil 1 von 2</span> &nbsp; <span class="badge">Dauer: ca. 5–8 Min.</span>', unsafe_allow_html=True)

with right:
    with st.popover("ℹ️", help="Info / Disclaimer"):
        st.markdown(
            """
**Disclaimer**

- Die folgende Verhandlung ist ein **fiktives** Szenario im Rahmen einer wissenschaftlichen Studie. Es kommt kein realer Kaufvertrag zustande und es entstehen keine Kosten oder Verpflichtungen.
- Es werden ausschließlich anonyme, nicht personenbezogene Daten gespeichert. Die erhobenen Daten lassen keine Rückschlüsse auf einzelne Personen zu und werden ausschließlich für wissenschaftliche Auswertungen im Rahmen eines Bachelorprojekts verwendet.
- Die Teilnahme ist freiwillig.
- Es werden zwei Verhandlungen durchgeführt. Sobald die erste Verhanldung abgeschlossen ist (also nach Annahme oder Abbruch), erscheint ein Fragebogen, welcher auszufüllen ist.
- Nach abgesendetem Fragebogen erscheint "Weiter zu Teil 2", welches zur zweiten Verhandlung weiterleitet. Nach dem Beenden der zweiten Verhandlung und Absenden des zweiten Fragebogens ist das Experiment beendet und das Fenster kann geschlossen werden.
            """
        )

st.write("")

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(f'<div class="meta">Teilnehmer-ID: {pid} · Reihenfolge: {order_code}</div>', unsafe_allow_html=True)

st.write("")
st.link_button(next_label, next_url, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.caption("Sie starten erst nach Klick auf „Weiter zu Verhandlung 1“.")

