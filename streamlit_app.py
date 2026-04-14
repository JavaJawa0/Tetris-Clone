import streamlit as st
import random
import time
from streamlit_javascript import st_javascript

# --- 1. SETUP ---
st.set_page_config(page_title="Retro Tetris", layout="centered")

# Get width for mobile styling
width = st_javascript("window.innerWidth")
is_mobile = width < 768 if width is not None else False

# --- 2. INITIALIZE STATE ---
if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = [[1, 1, 1], [0, 1, 0]]
    st.session_state.game_over = False


# --- 3. GAME FUNCTIONS ---
def move(dr, dc):
    new_r = st.session_state.curr_pos[0] + dr
    new_c = st.session_state.curr_pos[1] + dc
    shape_h = len(st.session_state.curr_shape)
    shape_w = len(st.session_state.curr_shape[0])

    if 0 <= new_c <= 10 - shape_w and new_r <= 20 - shape_h:
        st.session_state.curr_pos = [new_r, new_c]
    elif dr > 0:
        st.session_state.curr_pos = [0, 3]
        st.session_state.score += 10
        st.session_state.curr_shape = random.choice([
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[1, 1, 0], [0, 1, 1]],
            [[1, 1, 1], [0, 1, 0]]
        ])


def rotate():
    shape = st.session_state.curr_shape
    rotated = [list(row) for row in zip(*shape[::-1])]
    if st.session_state.curr_pos[1] + len(rotated[0]) <= 10:
        st.session_state.curr_shape = rotated


# --- 4. CSS ---
st.markdown(f"""
<style>
    .stApp {{ background-color: {"#A0A09F" if is_mobile else "#2e2e2e"} !important; }}
    [data-testid="stText"] {{
        background-color: #8A9878; color: #101010;
        font-family: monospace; padding: 20px; border: 10px solid #333;
        line-height: 1.1; font-size: 18px; font-weight: bold;
    }}
    div.stButton > button {{
        background-color: #3B3B3B !important; color: white !important;
        border-radius: 50% !important; height: 60px; width: 60px;
    }}
</style>
""", unsafe_allow_html=True)


# --- 5. THE GAME ENGINE (FRAGMENT) ---
# This special decorator stops the "flashing" by only updating this function
@st.fragment(run_every=1.0)
def game_engine():
    move(1, 0)  # Auto-fall

    # Render Board
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


# --- 6. UI ---
st.title("🧱 GB-TETRIS")
st.sidebar.metric("SCORE", st.session_state.score)

# Run the engine
game_engine()

# --- 7. CONTROLS ---
st.write("---")
c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
if c1.button("⬅️"): move(0, -1);