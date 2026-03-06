import uuid, random
from datetime import datetime
import streamlit as st
from db_common import get_conn, init_db

st.set_page_config(page_title="Studie Start", page_icon="▶️", layout="centered")

BOT_A_URL = "https://verhandlung.streamlit.app"
BOT_B_URL = "https://verhandlung123.streamlit.app"


# ----------------------------
# DB helpers
# ----------------------------
def init_assignments_db():
    init_db()  # erstellt alle Tabellen

def get_or_create_assignment(pid: str):
    init_assignments_db()
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT order_code FROM assignments WHERE pid = %s", (pid,))
    row = cur.fetchone()

    if row:
        order_code = row[0]
    else:
        order_code = random.choice(["AB", "BA"])
        cur.execute(
            "INSERT INTO assignments (pid, order_code, created_ts) VALUES (%s, %s, %s)",
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


chat_txt = export_all_chats_to_txt(bot_variant=bot_variant_for_queries)



import uuid, random
from datetime import datetime
import streamlit as st
from db_common import get_conn, init_db

st.set_page_config(page_title="Studie Start", page_icon="▶️", layout="centered")

BOT_A_URL = "https://verhandlung.streamlit.app"
BOT_B_URL = "https://verhandlung123.streamlit.app"


# ----------------------------
# DB helpers
# ----------------------------
def init_assignments_db():
    init_db()  # erstellt alle Tabellen

def get_or_create_assignment(pid: str):
    init_assignments_db()
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT order_code FROM assignments WHERE pid = %s", (pid,))
    row = cur.fetchone()

    if row:
        order_code = row[0]
    else:
        order_code = random.choice(["AB", "BA"])
        cur.execute(
            "INSERT INTO assignments (pid, order_code, created_ts) VALUES (%s, %s, %s)",
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

next_label = "▶️ Verhandlung 1 starten"


# ----------------------------
# 4) UI / Layout (neu)
# ----------------------------
st.markdown(
    """
    <style>
      .subtle { color: rgba(49, 51, 63, 0.72); }
      .pill {
        display:inline-block; padding: 6px 10px; border-radius: 999px;
        border: 1px solid rgba(49, 51, 63, 0.16);
        background: rgba(255,255,255,0.55);
        font-size: 0.85rem; color: rgba(49, 51, 63, 0.82);
        margin-right: 8px; margin-bottom: 8px;
      }
      .wrap { border: 1px solid rgba(49,51,63,0.14); border-radius: 18px;
              padding: 18px 18px; background: rgba(255,255,255,0.6); }
      .stepgrid { display: grid; grid-template-columns: 1fr; gap: 10px; margin-top: 12px; }
      .step {
        border: 1px solid rgba(49,51,63,0.12);
        border-radius: 14px;
        padding: 12px 12px;
        background: rgba(255,255,255,0.68);
      }
      .step strong { font-size: 1.02rem; }
      .smallmono {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        font-size: 0.88rem; color: rgba(49,51,63,0.75);
      }
      .divider { height: 1px; background: rgba(49,51,63,0.12); margin: 12px 0; }
      div.stLinkButton > a {
        padding: 0.95rem 1.05rem !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
      }
      .warnbox {
        border: 1px solid rgba(255, 165, 0, 0.35);
        background: rgba(255, 165, 0, 0.10);
        padding: 10px 12px;
        border-radius: 12px;
      }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎯 Verhandlungsstudie – Start")
st.markdown(
    "<div class='subtle'>Bitte folgen Sie den Schritten in der Reihenfolge. "
    "Das <b>Scoreboard</b> wird nur angezeigt, wenn <b>beide Verhandlungen</b> und <b>beide Fragebögen</b> vollständig abgeschlossen wurden.</div>",
    unsafe_allow_html=True
)

# Meta-Pills
st.markdown(
    f"""
    <span class="pill">Dauer gesamt: ca. 10–16 Min.</span>
    <span class="pill">2 Verhandlungen + 2 Fragebögen</span>
    <span class="pill">Scoreboard am Ende (nur vollständig)</span>
    """,
    unsafe_allow_html=True
)

st.write("")

# Hauptkarte
st.markdown('<div class="wrap">', unsafe_allow_html=True)

# Kurze, klare Schrittübersicht
st.markdown("### Ablauf (bitte genau so durchführen)")
st.markdown(
    """
    <div class="stepgrid">
      <div class="step"><strong>1) Verhandlung 1</strong><br><span class="subtle">Verhandeln Sie wie gewohnt. Sie können einen Deal schließen oder abbrechen.</span></div>
      <div class="step"><strong>2) Fragebogen 1</strong><br><span class="subtle">Bitte vollständig ausfüllen und absenden – erst danach geht es weiter.</span></div>
      <div class="step"><strong>3) Verhandlung 2</strong><br><span class="subtle">Es folgt eine zweite Verhandlung. Sie werden dabei <b>Unterschiede im Bot-Verhalten</b> bemerken – genau das untersuchen wir.</span></div>
      <div class="step"><strong>4) Fragebogen 2</strong><br><span class="subtle">Bitte erneut vollständig ausfüllen und absenden.</span></div>
      <div class="step"><strong>5) Scoreboard</strong><br><span class="subtle">Wird <b>nur</b> freigeschaltet, wenn Schritt 1–4 abgeschlossen sind.</span></div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Teilnehmerinfo (dezent)
st.markdown(
    f"<div class='smallmono'>Teilnehmer-ID: {pid} · Reihenfolge (intern): {order_code}</div>",
    unsafe_allow_html=True
)

st.write("")

# Verständnis-Check (reduziert Fehlbedienung / Abbrüche)
ack = st.checkbox(
    "Ich habe verstanden: Ich mache Verhandlung 1 → Fragebogen 1 → Verhandlung 2 → Fragebogen 2 (erst dann sehe ich das Scoreboard)."
)

if ack:
    st.link_button(next_label, next_url, use_container_width=True)
    st.caption("Sie starten erst nach Klick auf „Verhandlung 1 starten“.")
else:
    st.markdown(
        "<div class='warnbox'>✅ Setzen Sie bitte zuerst das Häkchen oben. "
        "Danach erscheint der Start-Button zur Verhandlung 1.</div>",
        unsafe_allow_html=True
    )

# Kompakte Infos/Disclaimer (eingeklappt, damit es übersichtlich bleibt)
with st.expander("ℹ️ Kurzinfo (anonym, fiktiv, freiwillig)"):
    st.markdown(
        """
- **Fiktives Szenario** im Rahmen einer Studie (kein realer Kaufvertrag, keine Kosten).
- Es werden **anonyme, nicht personenbezogene** Daten gespeichert und wissenschaftlich ausgewertet.
- Teilnahme ist **freiwillig**. Bitte führen Sie die Schritte **ohne Unterbrechung** durch.
        """
    )

st.markdown("</div>", unsafe_allow_html=True)
