import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pipe Puzzle Realistic", layout="centered")

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
<title>Pipe Puzzle Realistic</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body {
    background: #121212;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #fff;
  }
  .game-wrapper {
    background: #1c1c1c;
    border: 3px solid #333;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.9);
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
    color: #cfd8dc;
  }
  .steps-badge {
    background: #263238;
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid #455a64;
    color: #80d8ff;
  }
  .game-board {
    display: grid;
    grid-template-columns: repeat(4, 80px);
    grid-template-rows: repeat(4, 80px);
    gap: 4px;
    background: #0d0d0d;
    padding: 8px;
    border-radius: 10px;
    border: 2px solid #282828;
    box-shadow: inset 0 0 10px #000;
  }
  canvas.tile-canvas {
    width: 80px;
    height: 80px;
    background: #222;
    border-radius: 6px;
    cursor: pointer;
    transition: transform 0.15s, filter 0.15s;
    box-shadow: 0 2px 5px rgba(0,0,0,0.5);
  }
  canvas.tile-canvas:hover {
    filter: brightness(1.2);
  }
  canvas.tile-canvas:active {
    transform: scale(0.94);
  }
  .controls {
    margin-top: 15px;
    display: flex;
    gap: 12px;
  }
  button {
    background: #00838f;
    color: #fff;
    border: none;
    padding: 10px 22px;
    font-size: 14px;
    font-weight: bold;
    border-radius: 6px;
    cursor: pointer;
    box-shadow: 0 4px #004d40;
    transition: 0.1s;
  }
  button:active {
    transform: translateY(3px);
    box-shadow: 0 1px #004d40;
  }
  .status-msg {
    margin-top: 12px;
    font-size: 15px;
    font-weight: bold;
    height: 24px;
    text-align: center;
  }
</style>
</head>
<body>

<div class="game-wrapper">
  <div class="header-info">
    <span>🚰 NỐI ỐNG NƯỚC THỰC TẾ</span>
    <div class="steps-badge" id="stepsText">Số bước: 12</div>
  </div>

  <div class="game-board" id="board"></div>

  <div class="status-msg" id="statusText">Bấm vào ống để xoay đúng đường dẫn!</div>

  <div class="controls">
    <button onclick="checkWin()">Mở van nước</button>
    <button onclick="resetGame()" style="background: #e65100; box-shadow: 0 4px #bf360c;">Chơi lại</button>
  </div>
</div>

<script>
let stepsLeft = 12;

// Lưới 4x4: type = source, target, straight, corner
let grid = [
  {type: 'source', rot: 0, connected: true}, {type: 'straight', rot: 1, connected: false}, {type: 'corner', rot: 2, connected: false}, {type: 'straight', rot: 0, connected: false},
  {type: 'corner', rot: 1, connected: false}, {type: 'corner', rot: 3, connected: false}, {type: 'straight', rot: 0, connected: false}, {type: 'corner', rot: 0, connected: false},
  {type: 'straight', rot: 0, connected: false}, {type: 'corner', rot: 2, connected: false}, {type: 'straight', rot: 1, connected: false}, {type: 'corner', rot: 3, connected: false},
  {type: 'corner', rot: 0, connected: false}, {type: 'straight', rot: 1, connected: false}, {type: 'corner', rot: 2, connected: false}, {type: 'target', rot: 0, connected: false}
];

// Hàm vẽ đường ống 3D kim loại lên Canvas
function drawPipeOnCanvas(canvas, type, rot, isConnected) {
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;
  const center = w / 2;
  const pipeR = 14; // Bán kính ống nước

  ctx.clearRect(0, 0, w, h);

  // Background ô đất gạch
  ctx.fillStyle = '#262626';
  ctx.fillRect(0, 0, w, h);
  ctx.strokeStyle = '#1a1a1a';
  ctx.lineWidth = 2;
  ctx.strokeRect(0, 0, w, h);

  ctx.save();
  ctx.translate(center, center);
  ctx.rotate(rot * Math.PI / 2);
  ctx.translate(-center, -center);

  // Tạo màu kim loại đúc (Metallic Gradient)
  function createPipeGradient(x1, y1, x2, y2) {
    let grad = ctx.createLinearGradient(x1, y1, x2, y2);
    if(isConnected) {
      grad.addColorStop(0, '#1b5e20');
      grad.addColorStop(0.3, '#66bb6a');
      grad.addColorStop(0.7, '#81c784');
      grad.addColorStop(1, '#1b5e20');
    } else {
      grad.addColorStop(0, '#37474f');
      grad.addColorStop(0.3, '#90a4ae');
      grad.addColorStop(0.7, '#cfd8dc');
      grad.addColorStop(1, '#263238');
    }
    return grad;
  }

  // Vẽ các loại ống cụ thể
  if (type === 'straight') {
    // Ống thẳng từ trái qua phải
    ctx.fillStyle = createPipeGradient(0, center - pipeR, 0, center + pipeR);
    ctx.fillRect(0, center - pipeR, w, pipeR * 2);

    // Đai đinh tán hai bên
    ctx.fillStyle = isConnected ? '#4caf50' : '#78909c';
    ctx.fillRect(8, center - pipeR - 3, 6, pipeR * 2 + 6);
    ctx.fillRect(w - 14, center - pipeR - 3, 6, pipeR * 2 + 6);
  } 
  else if (type === 'corner') {
    // Ống cong bo góc L (Từ trái xuống dưới)
    ctx.beginPath();
    ctx.arc(0, h, h - center + pipeR, -Math.PI/2, 0);
    ctx.arc(0, h, h - center - pipeR, 0, -Math.PI/2, true);
    ctx.closePath();
    ctx.fillStyle = createPipeGradient(0, center - pipeR, center + pipeR, h);
    ctx.fill();

    // Gờ nối đai
    ctx.fillStyle = isConnected ? '#4caf50' : '#78909c';
    ctx.fillRect(0, center - pipeR - 3, 6, pipeR * 2 + 6);
    ctx.fillRect(center - pipeR - 3, h - 6, pipeR * 2 + 6, 6);
  } 
  else if (type === 'source') {
    // Ô Nguồn nước kèm bồn/van dẫn
    ctx.fillStyle = createPipeGradient(0, center - pipeR, w, center + pipeR);
    ctx.fillRect(0, center - pipeR, center, pipeR * 2);

    ctx.fillStyle = '#2e7d32';
    ctx.beginPath();
    ctx.arc(center, center, 22, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#a5d6a7';
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.fillStyle = '#fff';
    ctx.font = '20px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('💧', center, center + 7);
  } 
  else if (type === 'target') {
    // Ô Đích đến có van xả đỏ
    ctx.fillStyle = createPipeGradient(0, center - pipeR, center, center + pipeR);
    ctx.fillRect(0, center - pipeR, center, pipeR * 2);

    ctx.fillStyle = '#c62828';
    ctx.beginPath();
    ctx.arc(center, center, 20, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#ef9a9a';
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.fillStyle = '#fff';
    ctx.font = '16px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('⚙️', center, center + 5);
  }

  ctx.restore();
}

function renderBoard() {
  const boardEl = document.getElementById('board');
  boardEl.innerHTML = '';

  grid.forEach((cell, index) => {
    const canvas = document.createElement('canvas');
    canvas.className = 'tile-canvas';
    canvas.width = 80;
    canvas.height = 80;
    
    drawPipeOnCanvas(canvas, cell.type, cell.rot, cell.connected);

    canvas.onclick = () => rotateTile(index);
    boardEl.appendChild(canvas);
  });

  document.getElementById('stepsText').innerText = `Số bước: ${stepsLeft}`;
}

function rotateTile(index) {
  if (grid[index].type !== 'source' && grid[index].type !== 'target' && stepsLeft > 0) {
    grid[index].rot = (grid[index].rot + 1) % 4;
    stepsLeft--;
    renderBoard();
    if(stepsLeft <= 0) {
      document.getElementById('statusText').style.color = '#ef5350';
      document.getElementById('statusText').innerText = '⚠️ Hết số bước! Bấm Chơi lại để làm lại.';
    }
  }
}

function checkWin() {
  const statusText = document.getElementById('statusText');
  let win = grid[1].rot === 0 && grid[5].rot === 2; // Ví dụ điều kiện ghép nối thành công

  if (win) {
    statusText.style.color = '#66bb6a';
    statusText.innerText = '🎉 Tuyệt vời! Nước đã chảy qua toàn bộ đường ống!';
    grid.forEach(c => c.connected = true);
    renderBoard();
  } else {
    statusText.style.color = '#ffa726';
    statusText.innerText = '❌ Đường ống chưa liền mạch, nước bị rò rỉ!';
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
  grid[0].connected = true;
  document.getElementById('statusText').style.color = '#fff';
  document.getElementById('statusText').innerText = 'Bấm vào ống để xoay đúng đường dẫn!';
  renderBoard();
}

renderBoard();
</script>
</body>
</html>
"""

components.html(game_html, height=540)
