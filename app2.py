import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Pipe Puzzle Deluxe",
    page_icon="🚰",
    layout="centered"
)

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
    width: 380px;
  }
  .header-info {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    font-size: 14px;
    font-weight: bold;
    color: #cfd8dc;
  }
  .badge {
    background: #263238;
    padding: 5px 10px;
    border-radius: 15px;
    border: 1px solid #455a64;
    color: #80d8ff;
    font-size: 12px;
  }
  .game-board {
    display: grid;
    gap: 4px;
    background: #0d0d0d;
    padding: 8px;
    border-radius: 10px;
    border: 2px solid #282828;
    box-shadow: inset 0 0 10px #000;
  }
  canvas.tile-canvas {
    background: #222;
    border-radius: 6px;
    cursor: pointer;
    transition: transform 0.15s, filter 0.15s;
    box-shadow: 0 2px 5px rgba(0,0,0,0.5);
  }
  canvas.tile-canvas:hover {
    filter: brightness(1.2);
  }
  .controls {
    margin-top: 12px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
  }
  button {
    background: #00838f;
    color: #fff;
    border: none;
    padding: 8px 14px;
    font-size: 13px;
    font-weight: bold;
    border-radius: 6px;
    cursor: pointer;
    box-shadow: 0 3px #004d40;
    transition: 0.1s;
  }
  button:active {
    transform: translateY(2px);
    box-shadow: 0 1px #004d40;
  }
  button.hint-btn { background: #f57c00; box-shadow: 0 3px #e65100; }
  button.next-btn { background: #2e7d32; box-shadow: 0 3px #1b5e20; }
  .status-msg {
    margin-top: 10px;
    font-size: 14px;
    font-weight: bold;
    height: 22px;
    text-align: center;
  }
</style>
</head>
<body>

<div class="game-wrapper">
  <div class="header-info">
    <span id="levelTitle">MÀN 1 / 5</span>
    <div class="badge" id="stepsText">Lượt: Không giới hạn</div>
  </div>

  <div class="game-board" id="board"></div>

  <div class="status-msg" id="statusText">Xoay ống để kết nối nguồn nước!</div>

  <div class="controls">
    <button onclick="useHint()" class="hint-btn">💡 Gợi ý</button>
    <button onclick="checkWin()">Kiểm tra</button>
    <button onclick="resetLevel()" style="background: #e65100; box-shadow: 0 3px #bf360c;">Chơi lại</button>
    <button onclick="nextLevel()" class="next-btn" id="nextBtn" style="display:none;">Màn tiếp ➡</button>
  </div>
</div>

<script>
let audioCtx = null;
function initAudio() {
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  if (audioCtx.state === 'suspended') audioCtx.resume();
}

function playRotateSound() {
  initAudio();
  try {
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(320, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(120, audioCtx.currentTime + 0.04);
    gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.04);
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.start(); osc.stop(audioCtx.currentTime + 0.04);
  } catch(e) {}
}

function playWinSound() {
  initAudio();
  const notes = [523.25, 659.25, 783.99, 1046.50];
  notes.forEach((freq, i) => {
    setTimeout(() => {
      try {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'sine'; osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.3);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + 0.3);
      } catch(e){}
    }, i * 120);
  });
}

function playLoseSound() {
  initAudio();
  const notes = [300, 260, 220, 180];
  notes.forEach((freq, i) => {
    setTimeout(() => {
      try {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'sawtooth'; osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.25);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + 0.25);
      } catch(e){}
    }, i * 150);
  });
}

const BASE_PORTS = {
  'straight': [1, 3],
  'corner': [2, 3],
  'source': [1],
  'target': [3]
};

function getTilePorts(type, rot) {
  let base = BASE_PORTS[type] || [];
  return base.map(p => (p + rot) % 4);
}

const levelsData = [
  // Màn 1: 3x3
  {
    size: 3, maxSteps: Infinity,
    grid: [
      {type: 'source', rot: 0, correctRot: 0}, {type: 'straight', rot: 1, correctRot: 0}, {type: 'corner', rot: 2, correctRot: 0},
      {type: 'corner', rot: 0, correctRot: 1}, {type: 'straight', rot: 2, correctRot: 1}, {type: 'corner', rot: 1, correctRot: 3},
      {type: 'straight', rot: 0, correctRot: 0}, {type: 'corner', rot: 2, correctRot: 2}, {type: 'target', rot: 0, correctRot: 0}
    ]
  },
  // Màn 2: 3x3
  {
    size: 3, maxSteps: Infinity,
    grid: [
      {type: 'source', rot: 0, correctRot: 0}, {type: 'corner', rot: 1, correctRot: 0}, {type: 'straight', rot: 0, correctRot: 1},
      {type: 'straight', rot: 2, correctRot: 1}, {type: 'corner', rot: 3, correctRot: 2}, {type: 'corner', rot: 0, correctRot: 3},
      {type: 'corner', rot: 2, correctRot: 1}, {type: 'straight', rot: 1, correctRot: 0}, {type: 'target', rot: 0, correctRot: 0}
    ]
  },
  // Màn 3: 4x4
  {
    size: 4, maxSteps: 15,
    grid: [
      {type: 'source', rot: 0, correctRot: 0}, {type: 'straight', rot: 2, correctRot: 0}, {type: 'corner', rot: 1, correctRot: 0}, {type: 'straight', rot: 0, correctRot: 1},
      {type: 'corner', rot: 3, correctRot: 1}, {type: 'straight', rot: 1, correctRot: 0}, {type: 'corner', rot: 2, correctRot: 2}, {type: 'corner', rot: 0, correctRot: 1},
      {type: 'straight', rot: 1, correctRot: 1}, {type: 'corner', rot: 0, correctRot: 0}, {type: 'straight', rot: 2, correctRot: 0}, {type: 'corner', rot: 3, correctRot: 3},
      {type: 'corner', rot: 1, correctRot: 1}, {type: 'straight', rot: 0, correctRot: 0}, {type: 'corner', rot: 2, correctRot: 1}, {type: 'target', rot: 0, correctRot: 0}
    ]
  },
  // Màn 4: 4x4
  {
    size: 4, maxSteps: 12,
    grid: [
      {type: 'source', rot: 0, correctRot: 0}, {type: 'corner', rot: 2, correctRot: 0}, {type: 'straight', rot: 1, correctRot: 1}, {type: 'corner', rot: 0, correctRot: 3},
      {type: 'straight', rot: 3, correctRot: 1}, {type: 'corner', rot: 1, correctRot: 1}, {type: 'corner', rot: 2, correctRot: 0}, {type: 'straight', rot: 0, correctRot: 1},
      {type: 'corner', rot: 0, correctRot: 1}, {type: 'straight', rot: 1, correctRot: 0}, {type: 'corner', rot: 3, correctRot: 2}, {type: 'corner', rot: 1, correctRot: 3},
      {type: 'straight', rot: 2, correctRot: 0}, {type: 'corner', rot: 0, correctRot: 1}, {type: 'straight', rot: 1, correctRot: 0}, {type: 'target', rot: 0, correctRot: 0}
    ]
  },
  // Màn 5: 4x4
  {
    size: 4, maxSteps: 10,
    grid: [
      {type: 'source', rot: 0, correctRot: 0}, {type: 'corner', rot: 3, correctRot: 0}, {type: 'corner', rot: 1, correctRot: 3}, {type: 'straight', rot: 2, correctRot: 1},
      {type: 'straight', rot: 0, correctRot: 1}, {type: 'corner', rot: 2, correctRot: 1}, {type: 'straight', rot: 1, correctRot: 0}, {type: 'corner', rot: 0, correctRot: 2},
      {type: 'corner', rot: 1, correctRot: 0}, {type: 'straight', rot: 3, correctRot: 1}, {type: 'corner', rot: 2, correctRot: 1}, {type: 'straight', rot: 0, correctRot: 1},
      {type: 'straight', rot: 2, correctRot: 0}, {type: 'corner', rot: 0, correctRot: 3}, {type: 'corner', rot: 1, correctRot: 2}, {type: 'target', rot: 0, correctRot: 0}
    ]
  }
];

let currentLevel = 0;
let stepsLeft = 0;
let isGameOver = false;
let isWon = false;
let connectedTiles = new Set();

function loadLevel(lvlIdx) {
  currentLevel = lvlIdx;
  let lvl = levelsData[currentLevel];
  stepsLeft = lvl.maxSteps;
  isGameOver = false;
  isWon = false;
  connectedTiles.clear();
  
  document.getElementById('nextBtn').style.display = 'none';
  document.getElementById('levelTitle').innerText = `MÀN ${currentLevel + 1} / 5`;
  document.getElementById('statusText').style.color = '#fff';
  document.getElementById('statusText').innerText = 'Xoay ống để kết nối nguồn nước!';
  
  if(stepsLeft === Infinity) {
    document.getElementById('stepsText').innerText = 'Lượt: Không giới hạn';
  } else {
    document.getElementById('stepsText').innerText = `Lượt còn lại: ${stepsLeft}`;
  }

  const board = document.getElementById('board');
  board.style.gridTemplateColumns = `repeat(${lvl.size}, ${lvl.size === 3 ? 90 : 75}px)`;
  board.style.gridTemplateRows = `repeat(${lvl.size}, ${lvl.size === 3 ? 90 : 75}px)`;
  
  renderBoard();
}

function renderBoard() {
  const board = document.getElementById('board');
  board.innerHTML = '';
  let lvl = levelsData[currentLevel];
  let tileSize = lvl.size === 3 ? 90 : 75;

  lvl.grid.forEach((cell, index) => {
    const canvas = document.createElement('canvas');
    canvas.className = 'tile-canvas';
    canvas.width = tileSize;
    canvas.height = tileSize;
    
    drawPipe(canvas, cell.type, cell.rot, connectedTiles.has(index));

    canvas.onclick = () => rotateTile(index);
    board.appendChild(canvas);
  });
}

function drawPipe(canvas, type, rot, isConnected) {
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const center = w / 2;
  const pipeR = w === 90 ? 16 : 14;

  ctx.clearRect(0, 0, w, w);

  ctx.fillStyle = '#262626';
  ctx.fillRect(0, 0, w, w);
  ctx.strokeStyle = '#1a1a1a';
  ctx.lineWidth = 2;
  ctx.strokeRect(0, 0, w, w);

  ctx.save();
  ctx.translate(center, center);
  ctx.rotate(rot * Math.PI / 2);
  ctx.translate(-center, -center);

  function getGrad() {
    let grad = ctx.createLinearGradient(0, center - pipeR, 0, center + pipeR);
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

  if (type === 'straight') {
    ctx.fillStyle = getGrad();
    ctx.fillRect(0, center - pipeR, w, pipeR * 2);
    ctx.fillStyle = isConnected ? '#4caf50' : '#78909c';
    ctx.fillRect(8, center - pipeR - 3, 6, pipeR * 2 + 6);
    ctx.fillRect(w - 14, center - pipeR - 3, 6, pipeR * 2 + 6);
  } 
  else if (type === 'corner') {
    ctx.beginPath();
    ctx.arc(0, w, w - center + pipeR, -Math.PI/2, 0);
    ctx.arc(0, w, w - center - pipeR, 0, -Math.PI/2, true);
    ctx.closePath();
    ctx.fillStyle = getGrad();
    ctx.fill();
    ctx.fillStyle = isConnected ? '#4caf50' : '#78909c';
    ctx.fillRect(0, center - pipeR - 3, 6, pipeR * 2 + 6);
    ctx.fillRect(center - pipeR - 3, w - 6, pipeR * 2 + 6, 6);
  } 
  else if (type === 'source') {
    ctx.fillStyle = getGrad();
    ctx.fillRect(0, center - pipeR, center, pipeR * 2);
    ctx.fillStyle = '#2e7d32';
    ctx.beginPath(); ctx.arc(center, center, 20, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#a5d6a7'; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.font = '16px Arial'; ctx.textAlign = 'center';
    ctx.fillText('💧', center, center + 6);
  } 
  else if (type === 'target') {
    ctx.fillStyle = getGrad();
    ctx.fillRect(0, center - pipeR, center, pipeR * 2);
    ctx.fillStyle = '#c62828';
    ctx.beginPath(); ctx.arc(center, center, 18, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#ef9a9a'; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.font = '14px Arial'; ctx.textAlign = 'center';
    ctx.fillText('⚙️', center, center + 5);
  }

  ctx.restore();
}

function rotateTile(index) {
  if (isGameOver || isWon) return;
  let lvl = levelsData[currentLevel];
  let cell = lvl.grid[index];

  if (cell.type !== 'source' && cell.type !== 'target') {
    cell.rot = (cell.rot + 1) % 4;
    playRotateSound();

    if (lvl.maxSteps !== Infinity) {
      stepsLeft--;
      document.getElementById('stepsText').innerText = `Lượt còn lại: ${stepsLeft}`;
      if (stepsLeft <= 0) {
        isGameOver = true;
        playLoseSound();
        document.getElementById('statusText').style.color = '#ef5350';
        document.getElementById('statusText').innerText = '❌ Hết lượt xoay! Bạn đã thua cuộc.';
        return;
      }
    }
    connectedTiles.clear();
    renderBoard();
  }
}

function useHint() {
  if (isGameOver || isWon) return;
  let lvl = levelsData[currentLevel];
  let wrongCells = [];
  
  lvl.grid.forEach((cell, idx) => {
    if (cell.type !== 'source' && cell.type !== 'target' && cell.rot !== cell.correctRot) {
      wrongCells.push(idx);
    }
  });

  if (wrongCells.length > 0) {
    let randIdx = wrongCells[Math.floor(Math.random() * wrongCells.length)];
    lvl.grid[randIdx].rot = lvl.grid[randIdx].correctRot;
    playRotateSound();
    connectedTiles.clear();
    renderBoard();
    document.getElementById('statusText').style.color = '#00bcd4';
    document.getElementById('statusText').innerText = '💡 Gợi ý: Đã chỉnh 1 đoạn ống đúng vị trí!';
  } else {
    document.getElementById('statusText').innerText = '✨ Tất cả các ống đã đúng vị trí rồi!';
  }
}

function checkWin() {
  if (isGameOver || isWon) return;
  let lvl = levelsData[currentLevel];
  let size = lvl.size;

  const oppositeDir = [2, 3, 0, 1];

  let visited = new Set();
  let queue = [0];
  visited.add(0);

  let reachesTarget = false;

  while (queue.length > 0) {
    let curr = queue.shift();
    let currType = lvl.grid[curr].type;
    let currRot = lvl.grid[curr].rot;
    let currPorts = getTilePorts(currType, currRot);

    if (currType === 'target') {
      reachesTarget = true;
    }

    let r = Math.floor(curr / size);
    let c = curr % size;

    currPorts.forEach(dir => {
      let nr = r;
      let nc = c;
      if (dir === 0) nr--;
      else if (dir === 1) nc++;
      else if (dir === 2) nr++;
      else if (dir === 3) nc--;

      if (nr >= 0 && nr < size && nc >= 0 && nc < size) {
        let nextIdx = nr * size + nc;
        if (!visited.has(nextIdx)) {
          let nextType = lvl.grid[nextIdx].type;
          let nextRot = lvl.grid[nextIdx].rot;
          let nextPorts = getTilePorts(nextType, nextRot);

          let reqPort = oppositeDir[dir];
          if (nextPorts.includes(reqPort)) {
            visited.add(nextIdx);
            queue.push(nextIdx);
          }
        }
      }
    });
  }

  connectedTiles = visited;

  if (reachesTarget) {
    isWon = true;
    playWinSound();
    document.getElementById('statusText').style.color = '#66bb6a';
    document.getElementById('statusText').innerText = '🎉 Hoan hô! Nước đã chảy liên tục tới đích!';
    renderBoard();
    if (currentLevel < levelsData.length - 1) {
      document.getElementById('nextBtn').style.display = 'inline-block';
    } else {
      document.getElementById('statusText').innerText = '🏆 Chúc mừng bạn đã phá đảo toàn bộ 5 màn!';
    }
  } else {
    playLoseSound();
    renderBoard();
    document.getElementById('statusText').style.color = '#ffa726';
    document.getElementById('statusText').innerText = '⚠️ Đường ống bị hở hoặc chưa nối liền tới đích!';
  }
}

function resetLevel() {
  loadLevel(currentLevel);
}

function nextLevel() {
  if (currentLevel < levelsData.length - 1) {
    loadLevel(currentLevel + 1);
  }
}

loadLevel(0);
</script>
</body>
</html>
"""

components.html(game_html, height=520)
