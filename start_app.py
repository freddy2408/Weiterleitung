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
# 4) UI / Layout (kompakt, 1-Blick)
# ----------------------------
st.markdown(
    """
    <style>
      .subtle { color: rgba(49, 51, 63, 0.72); }
      .wrap {
        border: 1px solid rgba(49,51,63,0.14);
        border-radius: 18px;
        padding: 16px 16px;
        background: rgba(255,255,255,0.65);
      }
      .pill {
        display:inline-block; padding: 6px 10px; border-radius: 999px;
        border: 1px solid rgba(49, 51, 63, 0.16);
        background: rgba(255,255,255,0.55);
        font-size: 0.85rem; color: rgba(49, 51, 63, 0.82);
        margin-right: 8px; margin-bottom: 8px;
      }

      /* Kompakter Flow */
      .flowRow {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 8px;
        align-items: stretch;
        margin-top: 10px;
      }
      @media (max-width: 900px) {
        .flowRow { grid-template-columns: 1fr; }
        .arrowInline { display:none; }
      }
      .stepCard {
        border: 1px solid rgba(49,51,63,0.12);
        border-radius: 16px;
        padding: 10px 10px;
        background: rgba(255,255,255,0.76);
        min-height: 78px;
      }
      .stepTop {
        display:flex; align-items:center; justify-content:space-between;
        gap: 8px;
      }
      .stepNum {
        font-weight: 900;
        font-size: 0.92rem;
        color: rgba(49,51,63,0.80);
      }
      .stepIcon {
        font-size: 20px;
        line-height: 20px;
        opacity: 0.95;
      }
      .stepLabel {
        margin-top: 4px;
        font-weight: 800;
        font-size: 0.96rem;
      }
      .arrowInline{
        text-align:center;
        font-size: 18px;
        color: rgba(49,51,63,0.35);
        margin: 0 2px;
        align-self: center;
      }

      /* Akzente (dezent) */
      .accentBlue  { border-left: 6px solid rgba(59, 130, 246, 0.55); }
      .accentGreen { border-left: 6px solid rgba(16, 185, 129, 0.45); }
      .accentAmber { border-left: 6px solid rgba(245, 158, 11, 0.55); }

      /* Scoreboard Hook */
      .hook {
        border: 1px solid rgba(245, 158, 11, 0.25);
        background: rgba(245, 158, 11, 0.10);
        padding: 10px 12px;
        border-radius: 14px;
        margin-top: 12px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap: 10px;
      }
      .hook b { font-weight: 900; }
      .hookSmall { font-size: 0.9rem; color: rgba(49,51,63,0.78); }

      .divider { height: 1px; background: rgba(49,51,63,0.12); margin: 12px 0; }

      .smallmono {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        font-size: 0.86rem; color: rgba(49,51,63,0.70);
      }

      div.stLinkButton > a {
        padding: 0.95rem 1.05rem !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎯 2 Verhandlungen. 2 kurze Umfragen.")
st.markdown("<div class='subtle'>Dauer: ca. <b>5–10 Min.</b> · Am Ende wartet das <b>Scoreboard</b>.</div>", unsafe_allow_html=True)

st.markdown(
    """
    <span class="pill">1-Blick-Ablauf</span>
    <span class="pill">Fiktives Szenario</span>
    <span class="pill">Anonym</span>
    """,
    unsafe_allow_html=True
)

st.write("")
st.markdown('<div class="wrap">', unsafe_allow_html=True)

# Mini-Flow (sehr wenig Text)
st.markdown(
    """
    <div class="flowRow">
      <div class="stepCard accentBlue">
        <div class="stepTop"><div class="stepNum">1</div><div class="stepIcon">💬</div></div>
        <div class="stepLabel">Bot-Verhandlung</div>
      </div>

      <div class="arrowInline">➜</div>

      <div class="stepCard accentGreen">
        <div class="stepTop"><div class="stepNum">2</div><div class="stepIcon">📝</div></div>
        <div class="stepLabel">Kurz-Umfrage</div>
      </div>

      <div class="arrowInline">➜</div>

      <div class="stepCard accentBlue">
        <div class="stepTop"><div class="stepNum">3</div><div class="stepIcon">💬</div></div>
        <div class="stepLabel">Bot-Verhandlung</div>
      </div>

      <div class="arrowInline">➜</div>

      <div class="stepCard accentGreen">
        <div class="stepTop"><div class="stepNum">4</div><div class="stepIcon">📝</div></div>
        <div class="stepLabel">Kurz-Umfrage</div>
      </div>

      <div class="arrowInline">➜</div>

      <div class="stepCard accentAmber">
        <div class="stepTop"><div class="stepNum">5</div><div class="stepIcon">🏆</div></div>
        <div class="stepLabel">Scoreboard</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Scoreboard etwas stärker „verkaufen“, aber kurz
st.markdown(
    """
    <div class="hook">
      <div>
        <div><b>🏆 Scoreboard freischalten</b></div>
        <div class="hookSmall">Nur sichtbar, wenn du <b>beide</b> Verhandlungen & Umfragen abschließt.</div>
      </div>
      <div style="font-size:22px; opacity:0.9;">✨</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Start-Button prominent, ohne Hürde
st.link_button("▶️ Jetzt starten", next_url, use_container_width=True)

# Superkurzer Kontext (1 Zeile), keine Textwand
st.caption("Hinweis: Die beiden Bots verhalten sich leicht unterschiedlich – das ist Absicht.")

# Optional: Teilnehmerinfo sehr dezent (kann auch raus)
st.markdown(
    f"<div class='smallmono'>Teilnehmer-ID: {pid} · Reihenfolge: {order_code}</div>",
    unsafe_allow_html=True
)

with st.expander("ℹ️ Kurzinfo"):
    st.markdown("- Fiktives Szenario · anonym · freiwillig. Bitte in einem Durchlauf abschließen.")

st.markdown("</div>", unsafe_allow_html=True)
