import streamlit as st
import random
import time
from streamlit_javascript import st_javascript

# --- 1. SETUP & DEVICE DETECTION ---
# We fetch width to style the Gameboy background properly
width = st_javascript("window.innerWidth")
is_mobile = width < 768 if width is not None else False

st.set_page_config(page_title="Retro Tetris", layout="centered")

# --- 2. INITIALIZE STATE (The Fix for AttributeError) ---
# We define everything here so the rest of the script always has data to read
if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = [[1, 1, 1], [0, 1, 0]]  # Starting T-shape
    st.session_state.game_over = False


# --- 3. GAME FUNCTIONS ---
def move(dr, dc):
    if st.session_state.game_over:
        return

    new_r = st.session_state.curr_pos[0] + dr
    new_c = st.session_state.curr_pos[1] + dc

    # Boundary Check
    shape_h = len(st.session_state.curr_shape)
    shape_w = len(st.session_state.curr_shape[0])

    if 0 <= new_c <= 10 - shape_w and new_r <= 20 - shape_h:
        st.session_state.curr_pos = [new_r, new_c]
    elif dr > 0:
        # If we hit bottom, reset to top (Basic logic for now)
        st.session_state.curr_pos = [0, 3]
        st.session_state.score += 10
        if st.session_state.score > 500:  # Simple win condition or speed up
            pass


def rotate():
    if st.session_state.game_over:
        return
    # Matrix rotation logic
    shape = st.session_state.curr_shape
    rotated = [list(row) for row in zip(*shape[::-1])]

    # Check if rotation stays in bounds
    if st.session_state.curr_pos[1] + len(rotated[0]) <= 10:
        st.session_state.curr_shape = rotated


# --- 4. RETRO GAMEBOY CSS ---
st.markdown(f"""
<style>
    .stApp {{
        background-color: {"#A0A09F" if is_mobile else "#2e2e2e"} !important;
    }}
    /* The Screen Area */
    [data-testid="stText"] {{
        background-color: #8A9878;
        color: #101010;
        font-family: 'Courier New', monospace;
        padding: 20px;
        border: 10px solid #333;
        line-height: 1.1;
        font-size: 18px;
        font-weight: bold;
    }}
    /* Gameboy Buttons */
    div.stButton > button {{
        background-color: #3B3B3B !important;
        color: white !important;
        border-radius: 50% !important;
        height: 70px !important;
        width: 70px !important;
        border: 3px solid #101010 !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- 5. UI ELEMENTS ---
st.title("🧱 GB-TETRIS")

# Display Score safely
st.sidebar.metric("SCORE", st.session_state.score)

# Create a placeholder for the board so it doesn't "jitter"
board_placeholder = st.empty()

# --- 6. RENDER LOGIC ---
display_board = [row[:] for row in st.session