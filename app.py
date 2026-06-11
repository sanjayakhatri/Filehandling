import streamlit as st
from pathlib import Path

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="FileForge", page_icon="🗂️", layout="centered")

# ── Styling ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0e1117; color: #e2e8f0; }
.stApp { background: #0e1117; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem 4rem; max-width: 700px; }

.hero { text-align:center; padding: 2rem 0 1rem; }
.hero h1 { font-size:2.2rem; font-weight:700; color:#f8fafc; margin:0; letter-spacing:-0.03em; }
.accent { color:#38bdf8; }
.hero-sub { font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#475569;
            letter-spacing:0.1em; text-transform:uppercase; margin-top:0.4rem; }

.card-title { font-family:'JetBrains Mono',monospace; font-size:0.68rem; text-transform:uppercase;
              letter-spacing:0.12em; color:#475569; margin-bottom:0.8rem; }

.stTextInput input, .stTextArea textarea {
    background:#0f172a !important; border:1.5px solid #1e293b !important;
    border-radius:8px !important; color:#e2e8f0 !important;
    font-family:'JetBrains Mono',monospace !important; font-size:0.85rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color:#38bdf8 !important; box-shadow:0 0 0 3px rgba(56,189,248,0.08) !important;
}
label { color:#94a3b8 !important; font-size:0.82rem !important; }

.stButton button {
    background:#38bdf8 !important; color:#0a0f1e !important; border:none !important;
    border-radius:8px !important; font-weight:700 !important; font-size:0.85rem !important;
    padding:0.55rem 1.4rem !important; font-family:'Inter',sans-serif !important;
    transition:all 0.15s ease !important;
}
.stButton button:hover { background:#7dd3fc !important; transform:translateY(-1px) !important; }

.msg-box { border-radius:8px; padding:0.75rem 1rem; font-family:'JetBrains Mono',monospace;
           font-size:0.8rem; margin-top:0.8rem; display:flex; align-items:flex-start; gap:0.6rem; }
.msg-success { background:#052e16; border-left:3px solid #22c55e; color:#bbf7d0; }
.msg-error   { background:#2d0a0a; border-left:3px solid #ef4444; color:#fecaca; }
.msg-info    { background:#0c1a2e; border-left:3px solid #38bdf8; color:#bae6fd; }

.file-content { background:#080d14; border:1px solid #1e293b; border-radius:8px;
                padding:1rem 1.2rem; font-family:'JetBrains Mono',monospace; font-size:0.8rem;
                color:#94a3b8; white-space:pre-wrap; word-break:break-word;
                max-height:300px; overflow-y:auto; margin-top:0.8rem; line-height:1.7; }

.file-pill { display:inline-flex; align-items:center; gap:0.4rem; background:#0f172a;
             border:1px solid #1e293b; border-radius:6px; padding:0.3rem 0.7rem;
             font-family:'JetBrains Mono',monospace; font-size:0.73rem; color:#7dd3fc; margin:0.2rem; }

.divider { border:none; border-top:1px solid #1e293b; margin:1.4rem 0; }

.stRadio > div { gap:0.5rem !important; }
.stRadio label span { font-family:'JetBrains Mono',monospace !important;
                      font-size:0.8rem !important; color:#94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <span style="font-size:2.8rem">🗂️</span>
  <h1>File<span class="accent">Forge</span></h1>
  <p class="hero-sub">Python File Manager · Streamlit UI</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "op" not in st.session_state:
    st.session_state.op = "Create"
if "result" not in st.session_state:
    st.session_state.result = None

# ── Operation tabs ─────────────────────────────────────────────────────────────
cols = st.columns(4)
ops = [("✦", "Create"), ("◎", "Read"), ("⟳", "Update"), ("⌫", "Delete")]
for i, (icon, label) in enumerate(ops):
    with cols[i]:
        if st.button(f"{icon}  {label}", key=f"op_{label}", use_container_width=True):
            st.session_state.op = label
            st.session_state.result = None

op = st.session_state.op
st.markdown(f"<p style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#475569;text-align:center;margin:0.5rem 0 1rem'>Active: <span style='color:#38bdf8'>{op}</span></p>", unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def show_msg(mtype, msg):
    icons = {"success": "✓", "error": "✕", "info": "ℹ"}
    css   = {"success": "msg-success", "error": "msg-error", "info": "msg-info"}
    st.markdown(f'<div class="msg-box {css[mtype]}"><span>{icons[mtype]}</span><span>{msg}</span></div>',
                unsafe_allow_html=True)

def file_pills():
    files = [f.name for f in Path(".").iterdir() if f.is_file()]
    if files:
        pills = "".join(f'<span class="file-pill">📄 {f}</span>' for f in files)
        st.markdown(f"<div style='margin-bottom:0.8rem'>{pills}</div>", unsafe_allow_html=True)

# ── CREATE ─────────────────────────────────────────────────────────────────────
if op == "Create":
    st.markdown('<p class="card-title">// New File</p>', unsafe_allow_html=True)
    name = st.text_input("File name", placeholder="notes.txt", key="c_name")
    data = st.text_area("Content to write", placeholder="Start writing...", height=140, key="c_data")

    if st.button("Create File", key="c_btn"):
        if not name.strip():
            st.session_state.result = ("error", "File name cannot be empty.")
        else:
            path = Path(name.strip())
            if path.exists():
                st.session_state.result = ("error", f"Error: '{name}' already exists.")
            else:
                with open(path, "w") as f:
                    f.write("\n" + data)
                st.session_state.result = ("success", f"File '{name}' successfully created.")

# ── READ ───────────────────────────────────────────────────────────────────────
elif op == "Read":
    st.markdown('<p class="card-title">// Read File</p>', unsafe_allow_html=True)
    file_pills()
    name = st.text_input("File name to read", placeholder="notes.txt", key="r_name")

    if st.button("Read File", key="r_btn"):
        if not name.strip():
            st.session_state.result = ("error", "File name cannot be empty.")
        else:
            path = Path(name.strip())
            if not path.exists():
                st.session_state.result = ("error", f"Error: no such file '{name}'.")
            else:
                st.session_state.result = ("read", path.read_text(), name)

# ── UPDATE ─────────────────────────────────────────────────────────────────────
elif op == "Update":
    st.markdown('<p class="card-title">// Update File</p>', unsafe_allow_html=True)
    name = st.text_input("File name", placeholder="notes.txt", key="u_name")
    sub  = st.radio("Operation", ["Rename file", "Append content", "Overwrite file"],
                    horizontal=True, key="u_sub")

    if sub == "Rename file":
        new_name = st.text_input("New file name", placeholder="renamed.txt", key="u_new")
    else:
        new_data = st.text_area("Content", placeholder="Enter text...", height=120, key="u_data")

    if st.button("Apply", key="u_btn"):
        if not name.strip():
            st.session_state.result = ("error", "File name cannot be empty.")
        else:
            path = Path(name.strip())
            if not path.exists():
                st.session_state.result = ("error", f"No such file: '{name}'.")
            else:
                if sub == "Rename file":
                    if not new_name.strip():
                        st.session_state.result = ("error", "New name cannot be empty.")
                    elif Path(new_name.strip()).exists():
                        st.session_state.result = ("error", f"'{new_name}' already exists.")
                    else:
                        path.rename(Path(new_name.strip()))
                        st.session_state.result = ("success", f"Renamed '{name}' → '{new_name}'.")
                elif sub == "Append content":
                    with open(path, "a") as f:
                        f.write("\n" + new_data)
                    st.session_state.result = ("success", f"Content appended to '{name}'.")
                else:
                    with open(path, "w") as f:
                        f.write("\n" + new_data)
                    st.session_state.result = ("success", f"'{name}' successfully overwritten.")

# ── DELETE ─────────────────────────────────────────────────────────────────────
elif op == "Delete":
    st.markdown('<p class="card-title">// Delete File</p>', unsafe_allow_html=True)
    file_pills()
    name    = st.text_input("File name to delete", placeholder="notes.txt", key="d_name")
    confirm = st.checkbox("I understand this cannot be undone", key="d_confirm")

    if st.button("Delete File", key="d_btn"):
        if not name.strip():
            st.session_state.result = ("error", "File name cannot be empty.")
        elif not confirm:
            st.session_state.result = ("error", "Please tick the confirmation box first.")
        else:
            path = Path(name.strip())
            if not path.exists():
                st.session_state.result = ("error", f"No such file: '{name}'.")
            else:
                path.unlink()
                st.session_state.result = ("success", f"'{name}' successfully deleted.")

# ── Show result ────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result
    if r[0] == "read":
        show_msg("info", f"Showing contents of '{r[2]}'")
        body = r[1] if r[1].strip() else "— file is empty —"
        st.markdown(f'<div class="file-content">{body}</div>', unsafe_allow_html=True)
    else:
        show_msg(r[0], r[1])

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#334155;">
  pip install streamlit &nbsp;·&nbsp;
  <span style="color:#38bdf8">streamlit run app.py</span>
</p>
""", unsafe_allow_html=True)
          
