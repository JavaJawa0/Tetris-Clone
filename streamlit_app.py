import streamlit as st
import random
import time

# --- 1. SETUP ---
st.set_page_config(page_title="Stable Tetris", layout="centered")

# --- 2. INITIALIZE STATE ---
# We use st.session_state to store everything so it survives refreshes
if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = [[1, 1, 1], [0, 1, 0]]
    st.session_state.game_active = True


# --- 3. STABLE GAME FUNCTIONS ---
def move(dr, dc):
    # Calculate new position
    new_r = st.session_state.curr_pos[0] + dr
    new_c = st.session_state.curr_pos[1] + dc

    shape_h = len(st.session_state.curr_shape)
    shape_w = len(st.session_state.curr_shape[0])

    # Boundary check: If we can move, update position
    if 0 <= new_c <= 10 - shape_w and new_r <= 20 - shape_h:
        st.session_state.curr_pos = [new_r, new_c]
    elif dr > 0:
        # LANDING LOGIC: Reset to top and give a new shape
        st.session_state.curr_pos = [0, 3]
        st.session_state.score += 10
        st.session_state.curr_shape = random.choice([
            [[1, 1, 1, 1]],  # I
            [[1, 1], [1, 1]],  # O
            [[1, 1, 0], [0, 1, 1]],  # Z
            [[0, 1, 1], [1, 1, 0]],  # S
            [[1, 1, 1], [0, 1, 0]]  # T
        ])


def rotate():
    shape = st.session_state.curr_shape
    rotated = [list(row) for row in zip(*shape[::-1])]
    # Only rotate if it fits on the screen width-wise
    if st.session_state.curr_pos[1] + len(rotated[0]) <= 10:
        st.session_state.curr_shape = rotated


# --- 4. CSS STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #A0A09F !important; }
    [data-testid="stText"] {
        background-color: #8A9878; color: #101010;
        font-family: monospace; padding: 15px; border: 8px solid #333;
        line-height: 1.0; font-size: 18px; font-weight: bold;
    }
    div.stButton > button {
        background-color: #3B3B3B !important; color: white !important;
        border-radius: 10px !important; width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 5. PERMANENT UI (BUTTONS ALWAYS VISIBLE) ---
st.title("🧱 GB-TETRIS")
st.sidebar.metric("SCORE", st.session_state.score)

# CONTROLS (Placed at the top so they never vanish)
c1, c2, c3, c4 = st.columns(4)
if c1.button("⬅️"):
    move(0, -1)
    st.rerun()
if c2.button("⬇️"):
    move(1, 0)
    st.rerun()
if c3.button("➡️"):
    move(0, 1)
    st.rerun()
if c4.button("🔄"):
    rotate()
    st.rerun()


# --- 6. GAME ENGINE (RE-RENDERING AREA) ---
# We wrap only the screen in the fragment so it doesn't affect the buttons
@st.fragment(run_every=1.0)
def show_screen():
    # Only the block falling happens here
    move(1, 0)

    # Draw the board
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


# Launch the screen
show_screen()

if st.button("RESET GAME"):
    st.session_state.clear()
    st.rerun()