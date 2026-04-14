import streamlit as st
import random
import time

# --- 1. INITIALIZE ---
st.set_page_config(page_title="GB Tetris", layout="centered")

if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = [[1, 1], [1, 1]]


# --- 2. LOGIC ---
def check_collision(r, c, shape):
    for ri, row in enumerate(shape):
        for ci, val in enumerate(row):
            if val:
                new_r, new_c = r + ri, c + ci
                if new_c < 0 or new_c >= 10 or new_r >= 20:
                    return True
                if new_r >= 0 and st.session_state.board[new_r][new_c] == 1:
                    return True
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
        for _ in range(rows_cleared):
            new_board.insert(0, [0 for _ in range(10)])
        st.session_state.board = new_board

    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = random.choice(
        [[[1, 1, 1, 1]], [[1, 1], [1, 1]], [[1, 1, 1], [0, 1, 0]], [[1, 1, 0], [0, 1, 1]]])
    if check_collision(0, 3, st.session_state.curr_shape):
        st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
        st.session_state.score = 0


def move(dr, dc):
    new_r, new_c = st.session_state.curr_pos[0] + dr, st.session_state.curr_pos[1] + dc
    if not check_collision(new_r, new_c, st.session_state.curr_shape):
        st.session_state.curr_pos = [new_r, new_c]
    elif dr > 0:
        lock_and_clear()


def rotate():
    s = st.session_state.curr_shape
    rotated = [list(row) for row in zip(*s[::-1])]
    if not check_collision(st.session_state.curr_pos[0], st.session_state.curr_pos[1], rotated):
        st.session_state.curr_shape = rotated


# --- 3. STYLE & UI ---
st.markdown("""<style>
    .stApp { background-color: #2e2e2e !important; }
    [data-testid="stText"] {
        background-color: #8A9878; color: #101010;
        font-family: monospace; padding: 10px; border: 5px solid #000;
        line-height: 1.0; font-size: 18px; font-weight: bold;
        margin-bottom: 20px;
    }
    div.stButton > button {
        background-color: #3B3B3B !important; color: white !important;
        height: 60px; width: 100% !important; border-radius: 10px;
        font-size: 20px; font-weight: bold;
    }
</style>""", unsafe_allow_html=True)

st.title("🧱 GB-TETRIS")
st.subheader(f"Score: {st.session_state.score}")

# --- 4. THE GAME SCREEN ---
display_board = [row[:] for row in st.session_state.board]
curr_r, curr_c = st.session_state.curr_pos
for r, row in enumerate(st.session_state.curr_shape):
    for c, val in enumerate(row):
        if val and curr_r + r < 20:
            display_board[curr_r + r][curr_c + c] = 1

board_str = "".join(["".join(["🟥" if cell else "⬛" for cell in row]) + "\n" for row in display_board])
st.text(board_str)

# --- 5. THE BUTTONS (UNDER THE GAME) ---
# Using columns to create a "D-Pad" feel
col1, col2, col3 = st.columns(3)
if col1.button("⬅️"): move(0, -1); st.rerun()
if col2.button("⬇️"): move(1, 0); st.rerun()
if col3.button("➡️"): move(0, 1); st.rerun()

col_rot, col_res = st.columns(2)
if col_rot.button("🔄 ROTATE"): rotate(); st.rerun()
if col_res.button("♻️ RESET"): st.session_state.clear(); st.rerun()

# --- 6. GRAVITY ---
time.sleep(1)
move(1, 0)
st.rerun()