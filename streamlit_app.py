import streamlit as st
import random
import time

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Classic Tetris", layout="centered")

if 'board' not in st.session_state:
    # Initialize a 10x20 grid of zeros
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = [[1, 1], [1, 1]]  # Start with a Square


# --- 2. GAME LOGIC ---

def check_collision(r, c, shape):
    """ Checks if the shape at the given position hits anything """
    for ri, row in enumerate(shape):
        for ci, val in enumerate(row):
            if val:
                new_r, new_c = r + ri, c + ci
                # Check walls, floor, and existing blocks on the board
                if new_c < 0 or new_c >= 10 or new_r >= 20:
                    return True
                if new_r >= 0 and st.session_state.board[new_r][new_c] == 1:
                    return True
    return False


def lock_and_clear():
    """ Saves the piece to the board and clears full lines """
    curr_r, curr_c = st.session_state.curr_pos

    # 1. BAKE the piece into the board permanently
    for r, row in enumerate(st.session_state.curr_shape):
        for c, val in enumerate(row):
            if val:
                if curr_r + r < 20:
                    st.session_state.board[curr_r + r][curr_c + c] = 1

    # 2. CLEAR full rows and ADD 100 points
    # We only keep rows that are NOT full (sum < 10)
    new_board = [row for row in st.session_state.board if sum(row) < 10]
    rows_cleared = 20 - len(new_board)

    if rows_cleared > 0:
        st.session_state.score += (rows_cleared * 100)  # Give 100 points per line
        # Add the missing rows back to the TOP
        for _ in range(rows_cleared):
            new_board.insert(0, [0 for _ in range(10)])
        st.session_state.board = new_board

    # 3. SPAWN new piece
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = random.choice([
        [[1, 1, 1, 1]],  # I-piece
        [[1, 1], [1, 1]],  # O-piece
        [[1, 1, 1], [0, 1, 0]],  # T-piece
        [[1, 1, 0], [0, 1, 1]]  # Z-piece
    ])

    # Reset game if new piece hits immediately (Game Over)
    if check_collision(0, 3, st.session_state.curr_shape):
        st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
        st.session_state.score = 0


def move(dr, dc):
    new_r = st.session_state.curr_pos[0] + dr
    new_c = st.session_state.curr_pos[1] + dc

    if not check_collision(new_r, new_c, st.session_state.curr_shape):
        st.session_state.curr_pos = [new_r, new_c]
    elif dr > 0:
        # If we were trying to move DOWN and hit something, lock it!
        lock_and_clear()


def rotate():
    s = st.session_state.curr_shape
    rotated = [list(row) for row in zip(*s[::-1])]
    if not check_collision(st.session_state.curr_pos[0], st.session_state.curr_pos[1], rotated):
        st.session_state.curr_shape = rotated


# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("🕹️ CONTROLS")
    st.metric("SCORE", st.session_state.score)
    if st.button("⬅️ LEFT", use_container_width=True): move(0, -1); st.rerun()
    if st.button("➡️ RIGHT", use_container_width=True): move(0, 1); st.rerun()
    if st.button("🔄 ROTATE", use_container_width=True): rotate(); st.rerun()
    if st.button("⬇️ DROP", use_container_width=True): move(1, 0); st.rerun()
    st.divider()
    if st.button("RESET GAME", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- 4. STYLE & DISPLAY ---
st.markdown("""<style>
    .stApp { background-color: #2e2e2e !important; }
    [data-testid="stText"] {
        background-color: #8A9878; color: #101010;
        font-family: monospace; padding: 20px; border: 5px solid #000;
        line-height: 1.0; font-size: 18px; font-weight: bold;
    }
</style>""", unsafe_allow_html=True)

st.title("🧱 GB-TETRIS")

# Combine the board and the falling piece for drawing
display_board = [row[:] for row in st.session_state.board]
curr_r, curr_c = st.session_state.curr_pos

for r, row in enumerate(st.session_state.curr_shape):
    for c, val in enumerate(row):
        if val:
            if curr_r + r < 20:
                display_board[curr_r + r][curr_c + c] = 1

# Convert the grid to a string of emojis
board_str = ""
for row in display_board:
    board_str += "".join(["🟥" if cell else "⬛" for cell in row]) + "\n"

st.text(board_str)

# --- 5. AUTOMATIC GRAVITY ---
time.sleep(1)  # Wait 1 second
move(1, 0)  # Move down
st.rerun()  # Refresh