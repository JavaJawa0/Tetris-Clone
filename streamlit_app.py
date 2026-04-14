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
        [[[1, 1, 1, 1]], [[1, 1], [1, 1]], [[1, 1, 1], [0, 1, 0]], [[1, 1, 0], [0, 1, 1]], [[0, 1, 1], [1, 1, 0]]])
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


# --- 3. STYLE (FORCED TIGHT LAYOUT) ---
st.markdown("""<style>
    .stApp { background-color: #2e2e2e !important; }
    [data-testid="stText"] {
        background-color: #8A9878; color: #101010;
        font-family: monospace; padding: 10px; border: 5px solid #000;
        line-height: 1.0; font-size: 14px; font-weight: bold;
    }

    /* REMOVE GAPS BETWEEN COLUMNS */
    [data-testid="column"] {
        width: 33% !important;
        flex: 1 1 33% !important;
        min-width: 33% !important;
        padding: 0px 2px !important; /* Tiny gap */
    }

    /* MAKE BUTTONS SQUISH TOGETHER */
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
    }

    div.stButton > button {
        background-color: #3B3B3B !important; color: white !important;
        height: 55px; width: 100% !important; border-radius: 5px;
        font-size: 22px; padding: 0px; margin: 0px;
    }
</style>""", unsafe_allow_html=True)

st.title("🧱 GB-TETRIS")
st.write(f"**Score: {st.session_state.score}**")

# --- 4. THE GAME SCREEN ---
display_board = [row[:] for row in st.session_state.board]
curr_r, curr_c = st.session_state.curr_pos
for r, row in enumerate(st.session_state.curr_shape):
    for c, val in enumerate(row):
        if val and curr_r + r < 20:
            display_board[curr_r + r][curr_c + c] = 1

board_str = "".join(["".join(["🟥" if cell else "⬛" for cell in row]) + "\n" for row in display_board])
st.text(board_str)

# --- 5. THE BUTTONS ---
# Row 1: Left, Down, Right
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("⬅️"): move(0, -1); st.rerun()
with c2:
    if st.button("⬇️"): move(1, 0); st.rerun()
with c3:
    if st.button("➡️"): move(0, 1); st.rerun()

st.write("")  # Tiny spacer

# Row 2: Rotate and Reset (Wider buttons)
cr1, cr2 = st.columns([3, 1])
with cr1:
    if st.button("🔄 ROTATE", use_container_width=True): rotate(); st.rerun()
with cr2:
    if st.button("♻️", use_container_width=True): st.session_state.clear(); st.rerun()

# --- 6. GRAVITY ---
time.sleep(1)
move(1, 0)
st.rerun()