import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pipe Puzzle Deluxe", layout="centered")

# Tùy chỉnh CSS ẩn bớt lề mặc định của Streamlit để khung game hiển thị đẹp nhất
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
</style>
""", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pipe Puzzle Deluxe</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body {
    background: #141414;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #fff;
  }
  .game-wrapper {
    background: #222;
    border: 4px solid #3a3a3a;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.8);
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .header-info {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    font-size: 15px;
    font-weight: bold;
    color: #b0bec5;
  }
  .steps-badge {
    background: #37474f;
    padding: 5px 12px;
    border-radius: 6px;
    border: 1px solid #546e7a;
  }
  .game-board {
    display: grid;
    grid-template-columns: repeat(4, 75px);
    grid-template-rows: repeat(4, 75px);
    gap: 4px;
    background: #1a1a1a;
    padding: 6px;
    border-radius: 8px;
    border: 2px solid #2c2c2c;
  }
  .tile {
    width: 75px;
    height: 75px;
    background: #2b2b2b;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    border-radius: 6px;
    font-size: 32px;
    transition: background 0.15s, transform 0.15s;
    box-shadow: inset 0 2px 4px rgba(255,255,255,0.05);
  }
  .tile:hover {
    background: #383838;
  }
  .tile:active {
    transform: scale(0.95);
  }
  /* Kiểu dáng các loại ống */
  .tile.source { background: #1b5e20; border: 2px solid #4caf50; }
  .tile.target { background: #b71c1c; border: 2px solid #f44336; }
  .tile.connected { background: #004d40; border: 2px solid #00bcd4; }
  
  .controls {
    margin-top: 15px;
    display: flex;
    gap: 12px;
  }
  button {
    background: #00acc1;
    color: #000;
    border: none;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
    border-radius: 6px;
    cursor: pointer;
    box-shadow: 0 4px #007c91;
    transition: 0.1s;
  }
  button:active {
    transform: translateY(3px);
    box-shadow: 0 1px #007c91;
  }
  .status-msg {
    margin-top: 10px;
    font-size: 15px;
    font-weight: bold;
    height: 22px;
    text-align: center;
  }
</style>
</head>
<body>

<div class="game-wrapper">
  <div class="header-info">
    <span>🚰 PIPE PUZZLE DELUXE</span>
    <div class="steps-badge" id="stepsText">Số bước còn lại: 12</div>
  </div>

  <div class="game-board" id="board"></div>

  <div class="status-msg" id="statusText">Hãy xoay các ống để kết nối dòng nước!</div>

  <div class="controls">
    <button onclick="checkWin()">Kiểm tra dòng chảy</button>
    <button onclick="resetGame()" style="background: #ffa726; box-shadow: 0 4px #f57c00;">Chơi lại</button>
  </div>
</div>

<script>
// Lưới 4x4 mô phỏng trò chơi dẫn nước
// 0: Nguồn nước, 1: Đích đến, 2: Ống thẳng, 3: Ống góc (L), 4: Ống chữ T
let grid = [
  {type: 'source', rot: 0}, {type: 'straight', rot: 1}, {type: 'corner', rot: 2}, {type: 'straight', rot: 0},
  {type: 'corner', rot: 1}, {type: 'corner', rot: 3}, {type: 'straight', rot: 0}, {type: 'corner', rot: 0},
  {type: 'straight', rot: 0}, {type: 'corner', rot: 2}, {type: 'straight', rot: 1}, {type: 'corner', rot: 3},
  {type: 'corner', rot: 0}, {type: 'straight', rot: 1}, {type: 'corner', rot: 2}, {type: 'target', rot: 0}
];

const symbols = {
  'source': '🚰',
  'target': '🛑',
  'straight': '🪡',
  'corner': '🔄'
};

let stepsLeft = 12;

function renderBoard() {
  const boardEl = document.getElementById('board');
  boardEl.innerHTML = '';
  grid.forEach((cell, index) => {
    const tile = document.createElement('div');
    tile.className = `tile ${cell.type}`;
    if(cell.connected) tile.classList.add('connected');
    tile.innerHTML = symbols[cell.type];
    tile.style.transform = `rotate(${cell.rot * 90}deg)`;
    tile.onclick = () => rotateTile(index);
    boardEl.appendChild(tile);
  });
  document.getElementById('stepsText').innerText = `Số bước còn lại: ${stepsLeft}`;
}

function rotateTile(index) {
  if (grid[index].type !== 'source' && grid[index].type !== 'target' && stepsLeft > 0) {
    grid[index].rot = (grid[index].rot + 1) % 4;
    stepsLeft--;
    renderBoard();
    if(stepsLeft <= 0) {
      document.getElementById('statusText').style.color = '#ef5350';
      document.getElementById('statusText').innerText = '⚠️ Đã hết số bước! Hãy kiểm tra hoặc chơi lại.';
    }
  }
}

function checkWin() {
  const statusText = document.getElementById('statusText');
  // Điều kiện kiểm tra thắng mô phỏng trực quan
  let win = grid[1].rot === 0 && grid[5].rot === 2;
  if (win) {
    statusText.style.color = '#66bb6a';
    statusText.innerText = '🎉 Hoàn thành xuất sắc! Nước đã chảy thông suốt!';
    grid.forEach(c => c.connected = true);
    renderBoard();
  } else {
    statusText.style.color = '#ffa726';
    statusText.innerText = '❌ Đường ống chưa khớp, nước chưa thể chảy qua!';
  }
}

function resetGame() {
  stepsLeft = 12;
  grid.forEach(cell => {
    cell.connected = false;
    if(cell.type !== 'source' && cell.type !== 'target') {
      cell.rot = Math.floor(Math.random() * 4);
    }
  });
  document.getElementById('statusText').style.color = '#fff';
  document.getElementById('statusText').innerText = 'Hãy xoay các ống để kết nối dòng nước!';
  renderBoard();
}

renderBoard();
</script>
</body>
</html>
"""

components.html(game_html, height=520)
