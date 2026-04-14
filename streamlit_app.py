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
    if not check_collision(nr, nc, shape): st.session_state.curr_pos = [nr, nc]
    elif dr > 0: lock_and_clear()

def rotate():
    shape = SHAPES[st.session_state.curr_type]['shape']
    rotated = [list(row) for row in zip(*shape[::-1])]
    if not check_collision(st.session_state.curr_pos[0], st.session_state.curr_pos[1], rotated):
        SHAPES[st.session_state.curr_type]['shape'] = rotated

# --- 3. CSS (DASHBOARD FIX) ---
st.markdown("""<style>
    .block-container { max-width: 320px !important; padding: 0 !important; margin: auto !important; }
    .stApp { background-color: #2e2e2e !important; }

    /* The Main Game Grid */
    .game-table { 
        border-collapse: collapse; margin: 0 auto; line-height: 0; 
        background-color: #1a1a1a; border: 4px solid #444; 
    }
    .game-table td { padding: 0 !important; font-size: 20px !important; width: 22px; height: 22px; text-align: center; }

    /* SIDE-BY-SIDE DASHBOARD */
    .dashboard {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; padding: 10px 5px; color: white; font-family: monospace;
    }
    .next-box { background: #1a1a1a; border: 2px solid #444; padding: 5px; line-height: 1; }
    .next-grid { font-size: 14px; letter-spacing: -2px; }

    /* Controller */
    div[data-testid="stHorizontalBlock"] { display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 2px !important; }
    div.stButton > button { height: 60px !important; font-size: 22px !important; padding: 0 !important; }
</style>""", unsafe_allow_html=True)

# --- 4. RENDER DASHBOARD (SCORE & NEXT) ---
n = SHAPES[st.session_state.next_type]
# Create a 4x2 Next Piece Grid
next_display = [["⬛" for _ in range(4)] for _ in range(2)]
for r, row in enumerate(n['shape']):
    for c, val in enumerate(row):
        if val and r < 2 and c < 4:
            next_display[r][c] = n['color']

next_html = "".join(["".join(row) + "<br>" for row in next_display])

st.markdown(f"""
<div class="dashboard">
    <div class="next-box">
        <small>NEXT:</small><br>
        <div class="next-grid">{next_html}</div>
    </div>
    <div style="text-align: right;">
        <small>SCORE:</small><br>
        <span style="font-size: 20px; font-weight: bold;">{st.session_state.score}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5. RENDER GAME BOARD ---
display_board = [row[:] for row in st.session_state.board]
curr_r, curr_c = st.session_state.curr_pos
curr_data = SHAPES[st.session_state.curr_type]
for r, row in enumerate(curr_data['shape']):
    for c, val in enumerate(row):
        if val and curr_r + r < 20:
            display_board[curr_r + r][curr_c + c] = curr_data['color']

table_html = "<table class='game-table'>"
for row in display_board:
    table_html += "<tr>" + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
table_html += "</table>"
st.markdown(table_html, unsafe_allow_html=True)

# --- 6. CONTROLS ---
st.write("") # Spacer
ctrl_cols = st.columns(4)
with ctrl_cols[0]:
    if st.button("⬅️", key="L"): move(0, -1); st.rerun()
with ctrl_cols[1]:
    if st.button("⬇️", key="D"): move(1, 0); st.rerun()
with ctrl_cols[2]:
    if st.button("➡️", key="R"): move(0, 1); st.rerun()
with ctrl_cols[3]:
    if st.button("🔄", key="Rot"): rotate(); st.rerun()

if st.button("♻️ RESET", use_container_width=True):
    st.session_state.clear(); st.rerun()

# --- 7. GRAVITY ---
time.sleep(1)
move(1, 0)
st.rerun()