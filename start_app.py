import sqlite3, uuid, random
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Studie Start", page_icon="▶️")

BOT_A_URL = "https://verhandlung.streamlit.app"
BOT_B_URL = "https://verhandlung123.streamlit.app"
DB_PATH = "assignments.sqlite3"

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

# 1) pid aus URL oder neu generieren
pid = st.query_params.get("pid", None)
if not pid:
    pid = f"p-{uuid.uuid4().hex[:10]}"
    st.query_params["pid"] = pid

# 2) Reihenfolge fixieren (persistiert)
order_code = get_or_create_assignment(pid)
st.query_params["order"] = order_code

st.title("Start der Studie")
st.write(f"Deine Teilnehmer-ID: `{pid}`")
st.write(f"Zugewiesene Reihenfolge: **{order_code}** (zufällig)")

# 3) Links generieren
if order_code == "AB":
    first_url  = f"{BOT_A_URL}?pid={pid}&order=AB&step=1"
    second_url = f"{BOT_B_URL}?pid={pid}&order=AB&step=2"
    first_label, second_label = "Starte Bot A (1/2)", "Danach: Bot B (2/2)"
else:
    first_url  = f"{BOT_B_URL}?pid={pid}&order=BA&step=1"
    second_url = f"{BOT_A_URL}?pid={pid}&order=BA&step=2"
    first_label, second_label = "Starte Bot B (1/2)", "Danach: Bot A (2/2)"

st.link_button(first_label, first_url, use_container_width=True)
st.caption("Wenn du fertig bist, kommst du am Ende automatisch/über den Link zum zweiten Teil.")

st.markdown("---")
st.link_button(second_label, second_url, use_container_width=True)
st.caption("Den zweiten Link brauchst du erst nach Abschluss von Teil 1.")
