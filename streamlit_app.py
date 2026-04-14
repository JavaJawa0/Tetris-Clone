import streamlit as st
import random
import time

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Pro Tetris", layout="centered")

if 'board' not in st.session_state:
    # 0 = empty, 1 = landed block
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = [[1, 1], [1, 1]]


# --- 2. GAME LOGIC ---

def check_collision(r, c, shape):
    """Returns True if the shape at (r, c) hits a boundary or a landed block"""
    for ri, row in enumerate(shape):
        for ci, val in enumerate(row):
            if val:
                new_r, new_c = r + ri, c + ci
                # Check walls and floor
                if new_c < 0 or new_c >= 10 or new_r >= 20:
                    return True
                # Check landed blocks on the board
                if new_r >= 0 and st.session_state.board[new_r][new_c] == 1:
                    return True
    return False


def lock_piece():
    """Permanentally writes the current piece into the board"""
    curr_r, curr_c = st.session_state.curr_pos
    for r, row in enumerate(st.session_state.curr_shape):
        for c, val in enumerate(row):
            if val:
                st.session_state.board[curr_r + r][curr_c + c] = 1

    # Clear lines after locking
    clear_rows()

    # Spawn new piece
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = random.choice([
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[1, 1, 1], [0, 1, 0]],  # T
        [[1, 1, 0], [0, 1, 1]]  # Z
    ])

    # Game Over Check
    if check_collision(0, 3, st.session_state.curr_shape):
        st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
        st.session_state.score = 0


def clear_rows():
    new_board = [row for row in st.session_state.board if sum(row) < 10]
    rows_cleared = 20 - len(new_board)
    if rows_cleared > 0:
        st.session_state.score += (rows_cleared * 100)
        # Add empty rows back to the top
        for _ in range(rows_cleared):
            new_board.insert(0, [0 for _ in range(10)])
        st.session_state.board = new_board


def move(dr, dc):
    new_r = st.session_state.curr_pos[0] + dr
    new_c = st.session_state.curr_pos[1] + dc

    if not check_collision(new_r, new_c, st.session_state.curr_shape):
        st.session_state.curr_pos = [new_r, new_c]
    elif dr > 0:
        # If moving down failed, lock it
        lock_piece()


def rotate():
    s = st.session_state.curr_shape
    rotated = [list(row) for row in zip(*s[::-1])]
    if not check_collision(st.session_state.curr_pos[0], st.session_state.curr_pos[1], rotated):
        st.session_state.curr_shape = rotated


# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🕹️ CONTROLS")
    st.metric("SCORE", st.session_state.score)
    if st.button("⬅️ LEFT", use_container_width=True): move(0, -1); st.rerun()
    if st.button("➡️ RIGHT", use_container_width=True): move(0, 1); st.rerun()
    if st.button("🔄 ROTATE", use_container_width=True): rotate(); st.rerun()
    if st.button("⬇️ DROP", use_container_width=True): move(1, 0); st.rerun()
    if st.button("RESET", use_container_width=True): st.session_state.clear(); st.rerun()

# --- 4. RENDER ---
st.markdown("""<style>
    .stApp { background-color: #2e2e2e !important; }
    [data-testid="stText"] {
        background-color: #8A9878; color: #101010;
        font-family: monospace; padding: 15px; border: 5px solid #000;
        line-height: 1.0; font-size: 18px; font-weight: bold;
    }
</style>""", unsafe_allow_html=True)

st.title("🧱 PRO-TETRIS")

# Merge landed blocks and falling block for display
display_board = [row[:] for row in st.session_state.board]
curr_r, curr_c = st.session_state.curr_pos
for r, row in enumerate(st.session_state.curr_shape):
    for c, val in enumerate(row):
        if val:
            display_board[curr_r + r][curr_c + c] = 1

board_str = ""
for row in display_board:
    board_str += "".join(["🟥" if cell else "⬛" for cell in row]) + "\n"
st.text(board_str)

# --- 5. FALL ENGINE ---
time.sleep(1)
move(1, 0)
st.rerun()