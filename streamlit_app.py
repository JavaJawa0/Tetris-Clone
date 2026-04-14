import streamlit as st
import random
import time
from streamlit_javascript import st_javascript

# --- 1. SETUP & DETECTION ---
width = st_javascript("window.innerWidth")
is_mobile = width < 768 if width is not None else False
st.set_page_config(page_title="GB Tetris", layout="centered")

# --- 2. INITIALIZE STATE ---
if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_pos = [0, 3]
    # Shapes are matrices: 1 is a block, 0 is empty
    st.session_state.curr_shape = [[1, 1, 1], [0, 1, 0]]
    st.session_state.last_fall = time.time()


# --- 3. CORE FUNCTIONS ---
def move(dr, dc):
    new_r = st.session_state.curr_pos[0] + dr
    new_c = st.session_state.curr_pos[1] + dc

    # Simple collision/boundary check
    if 0 <= new_c <= 10 - len(st.session_state.curr_shape[0]) and new_r <= 20 - len(st.session_state.curr_shape):
        st.session_state.curr_pos = [new_r, new_c]
    elif dr > 0:  # If moving down fails, "lock" it
        # (Simplified: just reset to top for now)
        st.session_state.curr_pos = [0, 3]
        st.session_state.score += 10


def rotate():
    # Matrix rotation: Transpose then reverse rows
    shape = st.session_state.curr_shape
    rotated = [list(row) for row in zip(*shape[::-1])]

    # Check if rotation is possible within boundaries
    if st.session_state.curr_pos[1] + len(rotated[0]) <= 10:
        st.session_state.curr_shape = rotated


# --- 4. CSS ---
st.markdown(f"""
<style>
    .stApp {{ background-color: {"#A0A09F" if is_mobile else "#2e2e2e"} !important; }}
    [data-testid="stText"] {{
        background-color: #8A9878; color: #101010;
        font-family: monospace; padding: 20px; border: 10px solid #333;
        line-height: 1.1; font-size: 18px;
    }}
    div.stButton > button {{
        background-color: #3B3B3B !important; color: white !important;
        border-radius: 50% !important; height: 60px; width: 60px;
    }}
</style>
""", unsafe_allow_html=True)

# --- 5. UI & RENDERING ---
st.title("🧱 GB-Tetris")
st.sidebar.metric("SCORE", st.session_state.get('score', 0))

# The Screen
placeholder = st.empty()


def render_board():
    display_board = [row[:] for row in st.session_state.board]
    curr_r, curr_c = st.session_state.curr_pos
    for r, row in enumerate(st.session_state.curr_shape):
        for c, val in enumerate(row):
            if val: display_board[curr_r + r][curr_c + c] = 1

    board_output = ""
    for row in display_board:
        board_output += "".join(["🟥" if cell else "⬛" for cell in row]) + "\n"
    return board_output


# --- 6. CONTROLS ---
c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
if c1.button("⬅️"): move(0, -1)
if c2.button("⬇️"): move(1, 0)
if c3.button("➡️"): move(0, 1)
if c4.button("🔄 ROTATE"): rotate()

# --- 7. AUTO-FALL LOOP ---
# This tells Streamlit to rerun every 1 second
time.sleep(2)
move(1, 0)
placeholder.text(render_board())
st.rerun()