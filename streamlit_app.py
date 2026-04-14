import streamlit as st
import random
import time

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Tetris-Clone", layout="centered")

if 'SHAPE_DEFS' not in st.session_state:
    st.session_state.SHAPE_DEFS = {
        'I': {'matrix': [[1, 1, 1, 1]], 'color': '🟦'},
        'O': {'matrix': [[1, 1], [1, 1]], 'color': '🟨'},
        'T': {'matrix': [[1, 1, 1], [0, 1, 0]], 'color': '🟪'},
        'S': {'matrix': [[0, 1, 1], [1, 1, 0]], 'color': '🟩'},
        'Z': {'matrix': [[1, 1, 0], [0, 1, 1]], 'color': '🟥'},
        'J': {'matrix': [[1, 0, 0], [1, 1, 1]], 'color': '🟦'},
        'L': {'matrix': [[0, 0, 1], [1, 1, 1]], 'color': '🟧'}
    }

if 'board' not in st.session_state:
    st.session_state.board = [["⬛" for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.curr_type = random.choice(list(st.session_state.SHAPE_DEFS.keys()))
    st.session_state.next_type = random.choice(list(st.session_state.SHAPE_DEFS.keys()))
    st.session_state.curr_pos = [0, 3]
    st.session_state.live_matrix = st.session_state.SHAPE_DEFS[st.session_state.curr_type]['matrix']


# --- 2. LOGIC ---
def check_collision(r, c, matrix):
    for ri, row in enumerate(matrix):
        for ci, val in enumerate(row):
            if val:
                new_r, new_c = r + ri, c + ci
                if new_c < 0 or new_c >= 10 or new_r >= 20: return True
                if new_r >= 0 and st.session_state.board[new_r][new_c] != "⬛": return True
    return False


def lock_and_clear():
    curr_r, curr_c = st.session_state.curr_pos
    color = st.session_state.SHAPE_DEFS[st.session_state.curr_type]['color']
    for r, row in enumerate(st.session_state.live_matrix):
        for c, val in enumerate(row):
            if val:
                tr, tc = curr_r + r, curr_c + c
                if 0 <= tr < 20: st.session_state.board[tr][tc] = color

    new_board = [row for row in st.session_state.board if "⬛" in row]
    cleared = 20 - len(new_board)
    if cleared > 0:
        st.session_state.score += (cleared * 100)
        for _ in range(cleared): new_board.insert(0, ["⬛" for _ in range(10)])
        st.session_state.board = new_board

    st.session_state.curr_type = st.session_state.next_type
    st.session_state.next_type = random.choice(list(st.session_state.SHAPE_DEFS.keys()))
    st.session_state.live_matrix = st.session_state.SHAPE_DEFS[st.session_state.curr_type]['matrix']
    st.session_state.curr_pos = [0, 3]
    if check_collision(0, 3, st.session_state.live_matrix):
        st.session_state.board = [["⬛" for _ in range(10)] for _ in range(20)]
        st.session_state.score = 0


def move(dr, dc, is_hard_drop=False):
    if is_hard_drop:
        # Slam it to the bottom
        while not check_collision(st.session_state.curr_pos[0] + 1, st.session_state.curr_pos[1],
                                  st.session_state.live_matrix):
            st.session_state.curr_pos[0] += 1
        lock_and_clear()
    else:
        # Normal single step (Gravity)
        nr, nc = st.session_state.curr_pos[0] + dr, st.session_state.curr_pos[1] + dc
        if not check_collision(nr, nc, st.session_state.live_matrix):
            st.session_state.curr_pos = [nr, nc]
        elif dr > 0:
            lock_and_clear()


def rotate_logic():
    rotated = [list(row) for row in zip(*st.session_state.live_matrix[::-1])]
    r, c = st.session_state.curr_pos
    for kick in [0, -1, 1, -2, 2]:
        if not check_collision(r, c + kick, rotated):
            st.session_state.live_matrix = rotated
            st.session_state.curr_pos = [r, c + kick]
            return


# --- 3. CSS ---
st.markdown("""<style>
    .block-container { max-width: 320px !important; padding: 0 !important; margin: auto !important; }
    .stApp { background-color: #2e2e2e !important; }
    .game-table { border-collapse: collapse; margin: 0 auto; background-color: #1a1a1a; border: 4px solid #444; }
    .game-table td { padding: 0 !important; font-size: 20px !important; width: 22px; height: 22px; text-align: center; line-height: 0; }
    .dashboard { display: flex; justify-content: space-between; align-items: center; width: 100%; padding: 10px 5px; color: white; font-family: monospace; }
    .next-box { background: #1a1a1a; border: 2px solid #444; padding: 5px; min-width: 80px; }
    div[data-testid="stHorizontalBlock"] { display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 2px !important; }
    div.stButton > button { height: 60px !important; font-size: 25px !important; background-color: #3b3b3b !important; color: white !important; padding: 0 !important; }
</style>""", unsafe_allow_html=True)

# --- 4. RENDER DASHBOARD ---
n_def = st.session_state.SHAPE_DEFS[st.session_state.next_type]
next_grid = [["⬛" for _ in range(4)] for _ in range(2)]
for r, row in enumerate(n_def['matrix']):
    for c, val in enumerate(row):
        if val and r < 2 and c < 4: next_grid[r][c] = n_def['color']
next_html = "".join(["".join(r) + "<br>" for r in next_grid])

st.markdown(f"""<div class="dashboard"><div class="next-box"><small>NEXT:</small><br>{next_html}</div>
<div style="text-align: right;"><small>SCORE:</small><br><span style="font-size: 20px;">{st.session_state.score}</span></div></div>""",
            unsafe_allow_html=True)

# --- 5. RENDER BOARD ---
display_board = [row[:] for row in st.session_state.board]
curr_r, curr_c = st.session_state.curr_pos
color = st.session_state.SHAPE_DEFS[st.session_state.curr_type]['color']
for r, row in enumerate(st.session_state.live_matrix):
    for c, val in enumerate(row):
        if val:
            dr, dc = curr_r + r, curr_c + c
            if 0 <= dr < 20: display_board[dr][dc] = color

board_html = "<table class='game-table'>" + "".join(
    ["<tr>" + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>" for row in display_board]) + "</table>"
st.markdown(board_html, unsafe_allow_html=True)

# --- 6. CONTROLS ---
st.write("")
ctrl = st.columns(4)
if ctrl[0].button("⬅️", key="L"): move(0, -1); st.rerun()
if ctrl[1].button("⬇️", key="D"): move(1, 0, is_hard_drop=True); st.rerun()
if ctrl[2].button("➡️", key="R"): move(0, 1); st.rerun()
if ctrl[3].button("🔄", key="Rot"): rotate_logic(); st.rerun()

if st.button("♻️ RESET GAME", use_container_width=True): st.session_state.clear(); st.rerun()

# --- 7. AUTO-GRAVITY (Timer) ---
time.sleep(1)
move(1, 0, is_hard_drop=False)  # Gravity is always slow
st.rerun()