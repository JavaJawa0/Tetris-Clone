import streamlit as st
import random
import time

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Pro Tetris", layout="centered")

SHAPES = {
    'I': {'shape': [[1, 1, 1, 1]], 'color': '🟦'},
    'O': {'shape': [[1, 1], [1, 1]], 'color': '🟨'},
    'T': {'shape': [[1, 1, 1], [0, 1, 0]], 'color': '🟪'},
    'S': {'shape': [[0, 1, 1], [1, 1, 0]], 'color': '🟩'},
    'Z': {'shape': [[1, 1, 0], [0, 1, 1]], 'color': '🟥'},
    'J': {'shape': [[1, 0, 0], [1, 1, 1]], 'color': '🟦'},
    'L': {'shape': [[0, 0, 1], [1, 1, 1]], 'color': '🟧'}
}

if 'board' not in st.session_state:
    st.session_state.board = [["⬛" for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_type = random.choice(list(SHAPES.keys()))
    st.session_state.next_type = random.choice(list(SHAPES.keys()))
    st.session_state.curr_pos = [0, 3]


# --- 2. LOGIC ---
def check_collision(r, c, shape):
    for ri, row in enumerate(shape):
        for ci, val in enumerate(row):
            if val:
                new_r, new_c = r + ri, c + ci
                if new_c < 0 or new_c >= 10 or new_r >= 20: return True
                if new_r >= 0 and st.session_state.board[new_r][new_c] != "⬛": return True
    return False


def lock_and_clear():
    curr_r, curr_c = st.session_state.curr_pos
    shape_data = SHAPES[st.session_state.curr_type]
    for r, row in enumerate(shape_data['shape']):
        for c, val in enumerate(row):
            if val and curr_r + r < 20:
                st.session_state.board[curr_r + r][curr_c + c] = shape_data['color']

    new_board = [row for row in st.session_state.board if "⬛" in row]
    cleared = 20 - len(new_board)
    if cleared > 0:
        st.session_state.score += (cleared * 100)
        for _ in range(cleared): new_board.insert(0, ["⬛" for _ in range(10)])
        st.session_state.board = new_board

    st.session_state.curr_type = st.session_state.next_type
    st.session_state.next_type = random.choice(list(SHAPES.keys()))
    st.session_state.curr_pos = [0, 3]
    if check_collision(0, 3, SHAPES[st.session_state.curr_type]['shape']):
        st.session_state.board = [["⬛" for _ in range(10)] for _ in range(20)]
        st.session_state.score = 0


def move(dr, dc):
    shape = SHAPES[st.session_state.curr_type]['shape']
    nr, nc = st.session_state.curr_pos[0] + dr, st.session_state.curr_pos[1] + dc
    if not check_collision(nr, nc, shape):
        st.session_state.curr_pos = [nr, nc]
    elif dr > 0:
        lock_and_clear()


def rotate():
    shape = SHAPES[st.session_state.curr_type]['shape']
    rotated = [list(row) for row in zip(*shape[::-1])]
    if not check_collision(st.session_state.curr_pos[0], st.session_state.curr_pos[1], rotated):
        SHAPES[st.session_state.curr_type]['shape'] = rotated


# --- 3. CSS (THE FIX) ---
st.markdown("""<style>
    .block-container { max-width: 340px !important; padding: 5px !important; }
    .stApp { background-color: #2e2e2e !important; }

    /* PRE is the text box for the grid */
    pre {
        background-color: #1a1a1a !important; 
        color: white !important;
        padding: 4px !important; 
        border: 2px solid #444 !important;
        line-height: 1.0 !important; 
        font-size: 15px !important;
        white-space: nowrap !important; /* FORCES LINE TO STAY IN ONE PIECE */
        overflow: hidden !important;
        letter-spacing: -3px !important; /* PULLS EMOJIS CLOSER */
        font-family: 'Courier New', monospace !important;
    }

    div[data-testid="column"] { flex: 1 1 auto !important; width: auto !important; min-width: 0 !important; }
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; gap: 4px !important; }
    div.stButton > button { height: 60px !important; font-size: 25px !important; padding: 0 !important; }
</style>""", unsafe_allow_html=True)

# --- 4. DISPLAY ---
st.title("🧱 PRO TETRIS")

# Side-by-Side Dashboard
game_col, side_col = st.columns([2.5, 1])

with side_col:
    st.write("**NEXT**")
    n = SHAPES[st.session_state.next_type]
    n_p = "".join(["".join([n['color'] if v else "⬛" for v in r]) + "\n" for r in n['shape']])
    st.text(n_p)
    st.write(f"**SC**\n{st.session_state.score}")

with game_col:
    display_board = [row[:] for row in st.session_state.board]
    curr_r, curr_c = st.session_state.curr_pos
    curr_data = SHAPES[st.session_state.curr_type]
    for r, row in enumerate(curr_data['shape']):
        for c, val in enumerate(row):
            if val and curr_r + r < 20:
                display_board[curr_r + r][curr_c + c] = curr_data['color']

    board_str = "".join(["".join(row) + "\n" for row in display_board])
    st.text(board_str)

# --- 5. CONTROLS ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("⬅️", key="L"): move(0, -1); st.rerun()
with c2:
    if st.button("⬇️", key="D"): move(1, 0); st.rerun()
with c3:
    if st.button("➡️", key="R"): move(0, 1); st.rerun()
with c4:
    if st.button("🔄", key="Rot"): rotate(); st.rerun()

if st.button("♻️ RESET", use_container_width=True):
    st.session_state.clear();
    st.rerun()

# --- 6. GRAVITY ---
time.sleep(1)
move(1, 0)
st.rerun()