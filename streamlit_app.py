import streamlit as st
import random
import time
import streamlit.components.v1 as components

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Brick Game", layout="centered")

if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = [[1, 1], [1, 1]]
    st.session_state.trigger = 0

# --- 2. LOGIC ---
def check_collision(r, c, shape):
    for ri, row in enumerate(shape):
        for ci, val in enumerate(row):
            if val:
                new_r, new_c = r + ri, c + ci
                if new_c < 0 or new_c >= 10 or new_r >= 20: return True
                if new_r >= 0 and st.session_state.board[new_r][new_c] == 1: return True
    return False

def lock_and_clear():
    curr_r, curr_c = st.session_state.curr_pos
    for r, row in enumerate(st.session_state.curr_shape):
        for c, val in enumerate(row):
            if val and curr_r + r < 20:
                st.session_state.board[curr_r + r][curr_c + c] = 1
    new_board = [row for row in st.session_state.board if sum(row) < 10]
    rows_cleared = 20 - len(new_board)
    if rows_cleared > 0:
        st.session_state.score += (rows_cleared * 100)
        for _ in range(rows_cleared): new_board.insert(0, [0 for _ in range(10)])
        st.session_state.board = new_board
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = random.choice([[[1,1,1,1]],[[1,1],[1,1]],[[1,1,1],[0,1,0]],[[1,1,0],[0,1,1]],[[0,1,1],[1,1,0]]])
    if check_collision(0, 3, st.session_state.curr_shape):
        st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
        st.session_state.score = 0

def move(dr, dc):
    nr, nc = st.session_state.curr_pos[0] + dr, st.session_state.curr_pos[1] + dc
    if not check_collision(nr, nc, st.session_state.curr_shape): st.session_state.curr_pos = [nr, nc]
    elif dr > 0: lock_and_clear()

def rotate():
    s = st.session_state.curr_shape
    rotated = [list(row) for row in zip(*s[::-1])]
    if not check_collision(st.session_state.curr_pos[0], st.session_state.curr_pos[1], rotated):
        st.session_state.curr_shape = rotated

# --- 3. CSS ---
st.markdown("""<style>
    .block-container { max-width: 320px !important; padding: 0 !important; }
    .stApp { background-color: #2e2e2e !important; }
    [data-testid="stText"] {
        background-color: #8A9878; color: #101010;
        font-family: monospace; padding: 5px; border: 4px solid #000;
        line-height: 1.0; font-size: 15px; font-weight: bold;
        margin: 0 auto !important; width: 280px !important;
    }
    h3 { text-align: center; color: white; margin: 0; }
</style>""", unsafe_allow_html=True)

# --- 4. DISPLAY ---
st.subheader(f"SCORE: {st.session_state.score}")

display_board = [row[:] for row in st.session_state.board]
curr_r, curr_c = st.session_state.curr_pos
for r, row in enumerate(st.session_state.curr_shape):
    for c, val in enumerate(row):
        if val and curr_r + r < 20: display_board[curr_r + r][curr_c + c] = 1

board_str = "".join(["".join(["🟥" if cell else "⬛" for cell in row]) + "\n" for row in display_board])
st.text(board_str)

# --- 5. THE CUSTOM CONTROLLER (FORCED HORIZONTAL) ---
# This uses raw HTML to ensure buttons never stack
cols = st.columns(1)
with cols[0]:
    c1, c2, c3, c4 = st.columns([1,1,1,2])
    if c1.button("⬅️", key="L"): move(0, -1); st.rerun()
    if c2.button("⬇️", key="D"): move(1, 0); st.rerun()
    if c3.button("➡️", key="R"): move(0, 1); st.rerun()
    if c4.button("🔄 ROT", key="Rot"): rotate(); st.rerun()

if st.button("♻️ RESET", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# --- 6. GRAVITY ---
time.sleep(1)
move(1, 0)
st.rerun()