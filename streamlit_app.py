import streamlit as st
import random
from streamlit_javascript import st_javascript

# --- DEVICE DETECTION ---
# This runs a tiny JS snippet to get the window width
width = st_javascript("window.innerWidth")

# We assume PC until the width is confirmed (usually > 768px)
is_mobile = width < 768 if width is not None else False

# --- CONFIG & STATE ---
st.set_page_config(page_title="Responsive Tetris", layout="centered")

if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_pos = [0, 4]
    st.session_state.curr_shape = [[1, 1, 1, 1]]  # Default I-piece


# --- GAME ACTIONS ---
def move(dr, dc):
    new_r = st.session_state.curr_pos[0] + dr
    new_c = st.session_state.curr_pos[1] + dc
    if 0 <= new_c <= 10 - len(st.session_state.curr_shape[0]) and new_r < 20:
        st.session_state.curr_pos = [new_r, new_c]
    elif dr > 0:  # Hit bottom
        st.session_state.curr_pos = [0, 4]
        st.session_state.score += 10


# --- CSS FOR UI ---
st.markdown(f"""
<style>
    .stApp {{
        background-color: {"#A0A09F" if is_mobile else "#2e2e2e"} !important;
        transition: 0.5s;
    }}
    [data-testid="stText"] {{
        background-color: #8A9878;
        color: #101010;
        font-family: monospace;
        padding: 15px;
        border: 10px solid #333;
        border-radius: 5px;
    }}
</style>
""", unsafe_allow_html=True)

# --- UI LAYOUT ---
st.title("🕹️ Retro Tetris")

if is_mobile:
    st.write("📱 **Mobile Mode Active**")
else:
    st.write("💻 **PC Mode Active**")

# Display Board
display_board = [row[:] for row in st.session_state.board]
for r, row in enumerate(st.session_state.curr_shape):
    for c, val in enumerate(row):
        if val: display_board[st.session_state.curr_pos[0] + r][st.session_state.curr_pos[1] + c] = 1

board_output = ""
for row in display_board:
    board_output += "".join(["🟥" if cell else "⬛" for cell in row]) + "\n\n"

st.text(board_output)

# --- CONDITIONAL BUTTONS ---
# We only show the giant Gameboy-style buttons if on mobile
if is_mobile:
    st.write("---")
    col1, col2, col3 = st.columns(3)
    if col1.button("⬅️"): move(0, -1)
    if col2.button("⬇️"): move(1, 0)
    if col3.button("➡️"): move(0, 1)

    colA, colB = st.columns(2)
    if colA.button("🅰️ ROTATE"): pass  # Logic for rotate
    if colB.button("RESET"): st.session_state.clear()
else:
    # On PC, maybe just simple buttons or instructions
    if st.button("Drop Block (Down)"): move(1, 0)
    if st.button("Reset Game"): st.session_state.clear()

st.sidebar.metric("SCORE", st.session_state.score)