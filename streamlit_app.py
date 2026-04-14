import streamlit as st
import random
import time

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Stable Tetris", layout="centered")

# Initialize all variables immediately
if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = [[1, 1], [1, 1]]


# --- 2. LOGIC ---
def move(dr, dc):
    new_r = st.session_state.curr_pos[0] + dr
    new_c = st.session_state.curr_pos[1] + dc

    shape_h = len(st.session_state.curr_shape)
    shape_w = len(st.session_state.curr_shape[0])

    if 0 <= new_c <= 10 - shape_w and new_r <= 20 - shape_h:
        st.session_state.curr_pos = [new_r, new_c]
    elif dr > 0:
        # Reset and choose new shape
        st.session_state.curr_pos = [0, 3]
        st.session_state.score += 10
        st.session_state.curr_shape = random.choice([
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[1, 1, 1], [0, 1, 0]]
        ])


def rotate():
    s = st.session_state.curr_shape
    rotated = [list(row) for row in zip(*s[::-1])]
    if st.session_state.curr_pos[1] + len(rotated[0]) <= 10:
        st.session_state.curr_shape = rotated


# --- 3. THE SIDEBAR CONTROLS (THE FIX) ---
# Moving these to the sidebar ensures they NEVER vanish
with st.sidebar:
    st.title("🎮 CONTROLS")
    st.write(f"### SCORE: {st.session_state.score}")
    if st.button("⬅️ MOVE LEFT", use_container_width=True):
        move(0, -1)
        st.rerun()
    if st.button("➡️ MOVE RIGHT", use_container_width=True):
        move(0, 1)
        st.rerun()
    if st.button("⬇️ DROP FAST", use_container_width=True):
        move(1, 0)
        st.rerun()
    if st.button("🔄 ROTATE", use_container_width=True):
        rotate()
        st.rerun()
    st.write("---")
    if st.button("RESET GAME", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- 4. THE SCREEN ---
st.markdown("""
<style>
    .stApp { background-color: #2e2e2e !important; }
    [data-testid="stText"] {
        background-color: #8A9878; color: #101010;
        font-family: monospace; padding: 20px; border: 5px solid #000;
        line-height: 1.0; font-size: 20px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧱 GB-TETRIS")

# Render the board
display_board = [row[:] for row in st.session_state.board]
curr_r, curr_c = st.session_state.curr_pos
for r, row in enumerate(st.session_state.curr_shape):
    for c, val in enumerate(row):
        if val and curr_r + r < 20:
            display_board[curr_r + r][curr_c + c] = 1

board_str = ""
for row in display_board:
    board_str += "".join(["🟥" if cell else "⬛" for cell in row]) + "\n"

st.text(board_str)

# --- 5. THE AUTO-FALL ---
time.sleep(1)
move(1, 0)
st.rerun()