import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pipe Puzzle Game", layout="centered")

st.title("🚰 Thử Thách Nối Ống Nước")
st.write("Xoay các đoạn ống để kết nối nguồn nước (màu xanh lá) dẫn đến đích (màu đỏ) trước khi hết giờ!")

# Nhúng mã nguồn HTML/JS của game vào Streamlit
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body {
    background: #1e1e1e;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: 'Arial', sans-serif;
    color: #fff;
    padding: 10px;
  }
  .game-board {
    display: grid;
    grid-template-columns: repeat(3, 80px);
    grid-template-rows: repeat(3, 80px);
    gap: 5px;
    background: #333;
    padding: 5px;
    border-radius: 8px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.5);
  }
  .tile {
    width: 80px;
    height: 80px;
    background: #444;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    border-radius: 4px;
    font-size: 28px;
    transition: background 0.2s;
  }
  .tile:hover {
    background: #555;
  }
  .tile.source { background: #2e7d32; }
  .tile.target { background: #c62828; }
  .controls {
    margin-top: 15px;
    display: flex;
    gap: 10px;
  }
  button {
    background: #00bcd4;
    color: #000;
    border: none;
    padding: 10px 20px;
    font-size: 15px;
    font-weight: bold;
    border-radius: 5px;
    cursor: pointer;
  }
  button:hover {
    background: #26c6da;
  }
  .status {
    margin-top: 10px;
    font-size: 16px;
    font-weight: bold;
  }
</style>
</head>
<body>

<div class="game-board" id="board"></div>

<div class="status" id="statusText">Hãy xoay các ống để nối nguồn nước!</div>

<div class="controls">
  <button onclick="checkConnection()">Kiểm tra kết nối</button>
  <button onclick="resetGame()">Chơi lại</button>
</div>

<script>
let grid = [
  {type: 'source', rotation: 0}, {type: 'straight', rotation: 1}, {type: 'corner', rotation: 2},
  {type: 'corner', rotation: 0}, {type: 'straight', rotation: 0}, {type: 'corner', rotation: 3},
  {type: 'straight', rotation: 1}, {type: 'corner', rotation: 1}, {type: 'target', rotation: 0}
];

const symbols = {
  'source': '🚰',
  'target': '🏁',
  'straight': '➖',
  'corner': '🔄'
};

function renderBoard() {
  const boardEl = document.getElementById('board');
  boardEl.innerHTML = '';
  grid.forEach((cell, index) => {
    const tile = document.createElement('div');
    tile.className = `tile ${cell.type}`;
    tile.innerHTML = symbols[cell.type];
    tile.style.transform = `rotate(${cell.rotation * 90}deg)`;
    tile.onclick = () => rotateTile(index);
    boardEl.appendChild(tile);
  });
}

function rotateTile(index) {
  if (grid[index].type !== 'source' && grid[index].type !== 'target') {
    grid[index].rotation = (grid[index].rotation + 1) % 4;
    renderBoard();
  }
}

function checkConnection() {
  const statusText = document.getElementById('statusText');
  let win = grid[2].rotation === 1 && grid[3].rotation === 0;
  if (win) {
    statusText.style.color = '#4caf50';
    statusText.innerText = '🎉 Chúc mừng! Bạn đã dẫn nước thành công!';
  } else {
    statusText.style.color = '#ff9800';
    statusText.innerText = '⚠️ Chưa chính xác, hãy tiếp tục xoay ống nhé!';
  }
}

function resetGame() {
  grid.forEach(cell => {
    if(cell.type !== 'source' && cell.type !== 'target') {
      cell.rotation = Math.floor(Math.random() * 4);
    }
  });
  const statusText = document.getElementById('statusText');
  statusText.style.color = '#fff';
  statusText.innerText = 'Hãy xoay các ống để nối nguồn nước!';
  renderBoard();
}

renderBoard();
</script>
</body>
</html>
"""

components.html(game_html, height=380)
