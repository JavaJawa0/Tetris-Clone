import streamlit as st
import random
import time

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Classic GB Tetris", layout="centered")

# Ensure all game variables exist in memory
if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = [[1, 1], [1, 1]]


# --- 2. GAME LOGIC ---

def check_collision(r, c, shape):
    """Returns True if the piece hits boundaries or landed blocks."""
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
    """Bakes the current piece into the board and clears lines."""
    curr_r, curr_c = st.session_state.curr_pos
    for r, row in enumerate(st.session_state.curr_shape):
        for c, val in enumerate(row):
            if val and curr_r + r < 20:
                st.session_state.board[curr_r + r][curr_c + c] = 1

    # Identify full rows
    new_board = [row for row in st.session_state.board if sum(row) < 10]
    rows_cleared = 20 - len(new_board)

    if rows_cleared > 0:
        st.session_state.score += (rows_cleared * 100)
        # Drop everything down by adding empty rows at top
        for _ in range(rows_cleared):
            new_board.insert(0, [0 for _ in range(10)])
        st.session_state.board = new_board

    # Spawn new piece
    st.session_state.curr_pos = [0, 3]
    st.session_state.curr_shape = random.choice([
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[1, 1, 1], [0, 1, 0]],  # T
        [[1, 1, 0], [0, 1, 1]],  # Z
        [[0, 1, 1], [1, 1, 0]]  # S
    ])

    # Game Over Check
    if check_collision(0, 3, st.session_state.curr_shape):
        st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
        st.session_state.score = 0


def move(dr, dc):
    new_r = st.session_state.curr_pos[0] + dr
    new_c = st.session_state.curr_pos[1] + dc
    if not check_collision(new_r, new_c, st.session_state.curr_shape):
        st.session_state.curr_pos = [new_r, new_c]
    elif dr > 0:
        lock_and_clear()


def rotate():
    s = st.session_state.curr_shape
    rotated = [list(row) for row in zip(*s[::-1])]
    if not check_collision(st.session_state.curr_pos[0], st.session_state.curr_pos[1], rotated):
        st.session_state.curr_shape = rotated


# --- 3. STYLE (FORCED MOBILE CONTROLLER CSS) ---
st.markdown("""<style>
    .block-container { padding: 10px 5px !important; }
    .stApp { background-color: #2e2e2e !important; }

    /* Screen Area */
    [data-testid="stText"] {
        background-color: #8A9878; color: #101010;
        font-family: monospace; padding: 10px; border: 4px solid #000;
        line-height: 1.0; font-size: 14px; font-weight: bold;
        text-align: center;
    }

    /* Force horizontal alignment for arrows */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
    }

    div[data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0 !important;
        padding: 0 !important;
    }

    /* Big Controller Buttons */
    div.stButton > button {
        background-color: #3B3B3B !important; color: white !important;
        height: 75px !important; font-size: 30px !important; 
        border-radius: 12px !important; width: 100% !important;
        border: 2px solid #111 !important; padding: 0 !important;
    }
</style>""", unsafe_allow_html=True)

# --- 4. UI ---
st.title("🧱 GB-TETRIS")
st.write(f"### Score: {st.session_state.score}")

# Render board (landed blocks + active block)
display_board = [row[:] for row in st.session_state.board]
curr_r, curr_c = st.session_state.curr_pos
for r, row in enumerate(st.session_state.curr_shape):
    for c, val in enumerate(row):
        if val:
            if curr_r + r < 20:
                display_board[curr_r + r][curr_c + c] = 1

board_str = "".join(["".join(["🟥" if cell else "⬛" for cell in row]) + "\n" for row in display_board])
st.text(board_str)

# --- 5. THE CONTROLS ---
# Movement Row
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("⬅️", key="L"): move(0, -1); st.rerun()
with c2:
    if st.button("⬇️", key="D"): move(1, 0); st.rerun()
with c3:
    if st.button("➡️", key="R"): move(0, 1); st.rerun()

st.write("")  # Spacer

# Utility Row
cr1, cr2 = st.columns([2, 1])
with cr1:
    if st.button("🔄 ROTATE", key="Rot", use_container_width=True): rotate(); st.rerun()
with cr2:
    if st.button("♻️", key="Res", use_container_width=True): st.session_state.clear(); st.rerun()

# --- 6. GRAVITY ---
time.sleep(1)
move(1, 0)
st.rerun()