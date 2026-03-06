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



# ----------------------------
# 4) UI / Layout (Flow-Grafik)
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
      .wrap {
        border: 1px solid rgba(49,51,63,0.14);
        border-radius: 18px;
        padding: 18px 18px;
        background: rgba(255,255,255,0.6);
      }

      /* Flow Grafik */
      .flow {
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
        margin-top: 10px;
      }
      .node {
        position: relative;
        border: 1px solid rgba(49,51,63,0.12);
        border-radius: 16px;
        padding: 12px 12px;
        background: rgba(255,255,255,0.72);
      }
      .node .title {
        font-weight: 800;
        font-size: 1.02rem;
        margin-bottom: 2px;
      }
      .node .desc {
        color: rgba(49,51,63,0.75);
        font-size: 0.92rem;
        line-height: 1.25rem;
      }
      .tag {
        display:inline-block;
        font-size: 0.78rem;
        padding: 2px 8px;
        border-radius: 999px;
        border: 1px solid rgba(49,51,63,0.14);
        background: rgba(246,248,252,0.9);
        margin-top: 8px;
        color: rgba(49,51,63,0.75);
      }

      .arrow {
        text-align: center;
        font-size: 22px;
        line-height: 22px;
        color: rgba(49, 51, 63, 0.45);
        margin: -2px 0;
      }

      /* dezente Akzentfarbe */
      .accent {
        border-left: 6px solid rgba(59, 130, 246, 0.55); /* blau, soft */
        padding-left: 10px;
      }
      .accent2 {
        border-left: 6px solid rgba(16, 185, 129, 0.45); /* grün, soft */
        padding-left: 10px;
      }
      .accent3 {
        border-left: 6px solid rgba(245, 158, 11, 0.40); /* amber, soft */
        padding-left: 10px;
      }

      .divider { height: 1px; background: rgba(49,51,63,0.12); margin: 14px 0; }
      .smallmono {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        font-size: 0.88rem; color: rgba(49,51,63,0.70);
      }

      div.stLinkButton > a {
        padding: 0.95rem 1.05rem !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
      }

      .warnbox {
        border: 1px solid rgba(59, 130, 246, 0.28);
        background: rgba(59, 130, 246, 0.08);
        padding: 10px 12px;
        border-radius: 12px;
        color: rgba(49,51,63,0.82);
      }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎯 Verhandlungsstudie – Start")
st.markdown(
    "<div class='subtle'>Bitte folgen Sie den Schritten in der Reihenfolge. "
    "Das <b>Scoreboard</b> erscheint nur, wenn <b>beide Verhandlungen</b> und <b>beide Fragebögen</b> vollständig abgeschlossen wurden.</div>",
    unsafe_allow_html=True
)

# Meta-Pills (Dauer angepasst)
st.markdown(
    """
    <span class="pill">Dauer gesamt: ca. 5–10 Min.</span>
    <span class="pill">2 Verhandlungen + 2 Fragebögen</span>
    <span class="pill">Scoreboard am Ende (nur vollständig)</span>
    """,
    unsafe_allow_html=True
)

st.write("")
st.markdown('<div class="wrap">', unsafe_allow_html=True)

st.markdown("### Ablauf (einfach Schritt für Schritt)")

# Flow-Grafik mit Pfeilen
st.markdown(
    """
    <div class="flow">
      <div class="node accent">
        <div class="title">1) Verhandlung 1</div>
        <div class="desc">Verhandeln Sie wie in einem echten Chat. Schließen Sie einen Deal ab oder beenden Sie die Verhandlung.</div>
        <div class="tag">Schritt 1 von 5</div>
      </div>

      <div class="arrow">⬇️</div>

      <div class="node accent2">
        <div class="title">2) Fragebogen 1</div>
        <div class="desc">Bitte vollständig ausfüllen und absenden. Erst danach geht es automatisch weiter.</div>
        <div class="tag">Schritt 2 von 5</div>
      </div>

      <div class="arrow">⬇️</div>

      <div class="node accent">
        <div class="title">3) Verhandlung 2</div>
        <div class="desc">Es folgt eine zweite Verhandlung. Sie werden <b>Unterschiede im Bot-Verhalten</b> bemerken – genau das untersuchen wir.</div>
        <div class="tag">Schritt 3 von 5</div>
      </div>

      <div class="arrow">⬇️</div>

      <div class="node accent2">
        <div class="title">4) Fragebogen 2</div>
        <div class="desc">Bitte erneut vollständig ausfüllen und absenden.</div>
        <div class="tag">Schritt 4 von 5</div>
      </div>

      <div class="arrow">⬇️</div>

      <div class="node accent3">
        <div class="title">5) Scoreboard</div>
        <div class="desc"><b>Nur wenn</b> Schritt 1–4 abgeschlossen sind, wird das Scoreboard freigeschaltet.</div>
        <div class="tag">Schritt 5 von 5</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Teilnehmerinfo dezent
st.markdown(
    f"<div class='smallmono'>Teilnehmer-ID: {pid} · Reihenfolge (intern): {order_code}</div>",
    unsafe_allow_html=True
)

st.write("")

# Verständnis-Check: Button erst dann anzeigen
ack = st.checkbox(
    "Ich habe verstanden: Verhandlung 1 → Fragebogen 1 → Verhandlung 2 → Fragebogen 2 (erst dann Scoreboard)."
)

if ack:
    st.link_button("▶️ Verhandlung 1 starten", next_url, use_container_width=True)
    st.caption("Tipp: Am besten ohne Unterbrechung durchführen.")
else:
    st.markdown(
        "<div class='warnbox'>✅ Setzen Sie bitte das Häkchen – danach erscheint der Start-Button.</div>",
        unsafe_allow_html=True
    )

with st.expander("ℹ️ Kurzinfo (fiktiv, anonym, freiwillig)"):
    st.markdown(
        """
- **Fiktives Szenario** im Rahmen einer Studie (keine realen Zahlungen/Verträge).
- Es werden **anonyme, nicht personenbezogene** Daten gespeichert und wissenschaftlich ausgewertet.
- Bitte führen Sie die Schritte **in einem Durchlauf** durch, damit das Scoreboard freigeschaltet wird.
        """
    )

st.markdown("</div>", unsafe_allow_html=True)


