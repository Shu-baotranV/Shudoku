import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Artistic Sudoku Master",
    page_icon="🎨",
    layout="centered"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 0.5rem;
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
<title>Artistic Sudoku Master</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Quicksand:wght@600;700&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body {
    background: linear-gradient(135deg, #fce4ec, #e0f7fa, #fff9c4);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: 'Quicksand', sans-serif;
    color: #333;
  }
  .game-wrapper {
    background: rgba(255, 255, 255, 0.95);
    border: 4px solid #ff4081;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 15px 35px rgba(255, 64, 129, 0.25), 0 5px 15px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 440px;
    width: 100%;
    position: relative;
    overflow: hidden;
  }
  .game-wrapper::before {
    content: '🎨 ✨ 🧩 🌟';
    position: absolute;
    top: 10px; left: 15px;
    font-size: 16px;
    opacity: 0.6;
    letter-spacing: 5px;
  }
  .screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    text-align: center;
    position: relative;
    z-index: 1;
    margin-top: 10px;
  }
  h1 { 
    font-family: 'Fredoka One', cursive;
    font-size: 26px; 
    color: #d81b60; 
    margin-bottom: 12px; 
    text-shadow: 2px 2px 0px #ffe0b2;
  }
  p { 
    font-size: 14px; 
    color: #455a64; 
    margin-bottom: 18px; 
    line-height: 1.6; 
    text-align: left; 
    padding: 14px; 
    background: #fff3e0; 
    border-radius: 12px; 
    border-left: 5px solid #ffa726;
  }
  
  .header-info {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    font-size: 15px;
    font-weight: 700;
    color: #37474f;
  }
  .badge {
    background: linear-gradient(135deg, #ffb74d, #ffa726);
    padding: 6px 14px;
    border-radius: 20px;
    box-shadow: 0 3px 6px rgba(255, 152, 0, 0.3);
    color: #fff;
    font-size: 13px;
    font-family: 'Fredoka One', cursive;
  }
  
  .sudoku-grid {
    display: grid;
    gap: 4px;
    background: #ab47bc;
    padding: 6px;
    border-radius: 12px;
    margin-bottom: 14px;
    box-shadow: 0 8px 20px rgba(171, 71, 188, 0.3);
  }
  .cell {
    background: #fff;
    border: 2px solid #e1bee7;
    text-align: center;
    font-family: 'Fredoka One', cursive;
    font-weight: bold;
    color: #7b1fa2;
    border-radius: 8px;
    outline: none;
    transition: 0.2s;
  }
  .cell:focus {
    background: #f3e5f5;
    border-color: #ab47bc;
    transform: scale(1.05);
  }
  .cell.fixed {
    background: #fce4ec;
    color: #c2185b;
    border-color: #f8bbd0;
  }
  .cell.error {
    background: #ff5252 !important;
    color: #fff !important;
  }

  .controls {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 10px;
  }
  button {
    font-family: 'Fredoka One', cursive;
    background: linear-gradient(135deg, #26a69a, #00897b);
    color: #fff;
    border: none;
    padding: 10px 18px;
    font-size: 14px;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(38, 166, 154, 0.4);
    transition: 0.15s;
  }
  button:hover { filter: brightness(1.1); transform: translateY(-2px); }
  button:active { transform: translateY(1px); }
  button.hint-btn { background: linear-gradient(135deg, #ffa726, #fb8c00); box-shadow: 0 4px 10px rgba(255, 167, 38, 0.4); }
  button.next-btn { background: linear-gradient(135deg, #66bb6a, #43a047); box-shadow: 0 4px 10px rgba(102, 187, 106, 0.4); }
  button.start-btn { background: linear-gradient(135deg, #ec407a, #d81b60); font-size: 18px; padding: 12px 32px; margin-top: 10px; box-shadow: 0 6px 15px rgba(236, 64, 122, 0.5); }

  .status-msg {
    margin-top: 10px;
    font-size: 15px;
    font-weight: 700;
    height: 24px;
    text-align: center;
    color: #6a1b9a;
  }
</style>
</head>
<body>

<div class="game-wrapper">

  <!-- MÀN HÌNH HƯỚNG DẪN -->
  <div id="tutorial-screen" class="screen">
    <h1>🎨 ARTISTIC SUDOKU</h1>
    <p>
      🌟 <b>Mục tiêu:</b> Điền các con số nghệ thuật vào ô trống.<br>
      🌟 <b>Quy tắc:</b> Hàng ngang, cột dọc & khối vuông không trùng số.<br>
      🌟 <b>Trợ giúp:</b> Bạn có tối đa <b>3 lượt gợi ý (💡)</b> mỗi màn.<br>
      🌟 <b>Thử thách:</b> Trải nghiệm 5 cấp độ sinh động từ 5x5 đến 9x9!
    </p>
    <button class="btn start-btn" onclick="startTheGame()">🚀 BẮT ĐẦU KHÁM PHÁ</button>
  </div>

  <!-- MÀN HÌNH CHƠI GAME -->
  <div id="game-screen" class="screen" style="display: none;">
    <div class="header-info">
      <span id="levelTitle" style="color: #8e24aa; font-size: 16px; font-family: 'Fredoka One', cursive;">MÀN 1 (5x5)</span>
      <div class="badge" id="hintBadge">💡 Gợi ý: 3</div>
    </div>

    <div class="sudoku-grid" id="board"></div>

    <div class="status-msg" id="statusText">Hãy điền các con số thật khéo léo nhé!</div>

    <div class="controls">
      <button onclick="useHint()" class="hint-btn" id="hintBtn">💡 Gợi ý (3)</button>
      <button onclick="checkAnswer()">Kiểm tra</button>
      <button onclick="resetLevel()" style="background: linear-gradient(135deg, #ef5350, #e53935);">Làm lại</button>
      <button onclick="nextLevel()" class="next-btn" id="nextBtn" style="display:none;">Màn tiếp ➡</button>
    </div>
  </div>

</div>

<script>
let audioCtx = null;
let bgMusicInterval = null;

function initAudio() {
  try {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  } catch(e) {}
}

function startBgMusic() {
  if (bgMusicInterval) return;
  const cheerfulMelody = [329.63, 392.00, 440.00, 523.25, 392.00, 440.00, 523.25, 659.25];
  let step = 0;
  bgMusicInterval = setInterval(() => {
    try {
      if(!audioCtx || audioCtx.state !== 'running') return;
      let freq = cheerfulMelody[step % cheerfulMelody.length];
      
      let osc = audioCtx.createOscillator();
      let gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(0.03, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.3);
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.start(); osc.stop(audioCtx.currentTime + 0.3);
      
      step++;
    } catch(e){}
  }, 400);
}

function playSound(type) {
  try {
    initAudio();
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    
    if (type === 'correct') {
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(659.25, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(1046.50, audioCtx.currentTime + 0.15);
      gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2);
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.start(); osc.stop(audioCtx.currentTime + 0.2);
    } else if (type === 'wrong') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(180, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(90, audioCtx.currentTime + 0.25);
      gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.25);
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.start(); osc.stop(audioCtx.currentTime + 0.25);
    } else if (type === 'win') {
      const notes = [523.25, 659.25, 783.99, 1046.50, 1318.51];
      notes.forEach((f, i) => {
        setTimeout(() => {
          let o = audioCtx.createOscillator();
          let g = audioCtx.createGain();
          o.type = 'triangle'; o.frequency.setValueAtTime(f, audioCtx.currentTime);
          g.gain.setValueAtTime(0.15, audioCtx.currentTime);
          g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.4);
          o.connect(g); g.connect(audioCtx.destination);
          o.start(); o.stop(audioCtx.currentTime + 0.4);
        }, i * 90);
      });
    } else if (type === 'lose') {
      const notes = [330, 277, 220, 164];
      notes.forEach((f, i) => {
        setTimeout(() => {
          let o = audioCtx.createOscillator();
          let g = audioCtx.createGain();
          o.type = 'sawtooth'; o.frequency.setValueAtTime(f, audioCtx.currentTime);
          g.gain.setValueAtTime(0.1, audioCtx.currentTime);
          g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.3);
          o.connect(g); g.connect(audioCtx.destination);
          o.start(); o.stop(audioCtx.currentTime + 0.3);
        }, i * 110);
      });
    }
  } catch(e) {}
}

const levels = [
  {
    size: 5,
    solution: [1,2,3,4,5, 3,4,5,1,2, 5,1,2,3,4, 2,3,4,5,1, 4,5,1,2,3],
    puzzle: [1,0,3,0,5, 0,4,0,1,0, 5,0,2,0,4, 0,3,0,5,0, 4,0,1,0,3]
  },
  {
    size: 5,
    solution: [2,3,1,5,4, 4,5,2,3,1, 1,2,3,4,5, 5,1,4,2,3, 3,4,5,1,2],
    puzzle: [2,0,1,0,4, 0,5,0,3,0, 1,0,3,0,5, 0,1,0,2,0, 3,0,5,0,2]
  },
  {
    size: 9,
    solution: [
      5,3,4,6,7,8,9,1,2, 6,7,2,1,9,5,3,4,8, 1,9,8,3,4,2,5,6,7,
      8,5,9,7,6,1,4,2,3, 4,2,6,8,5,3,7,9,1, 7,1,3,9,2,4,8,5,6,
      9,6,1,5,3,7,2,8,4, 2,8,7,4,1,9,6,3,5, 3,4,5,2,8,6,1,7,9
    ],
    puzzle: [
      5,3,0,0,7,0,0,0,2, 6,0,0,1,9,5,0,0,0, 0,9,8,0,0,0,0,6,0,
      8,0,0,0,6,0,0,0,3, 4,0,0,8,0,3,0,0,1, 7,0,0,0,2,0,0,0,6,
      0,6,0,0,0,0,2,8,0, 0,0,0,4,1,9,0,0,5, 3,0,0,0,8,0,0,7,9
    ]
  },
  {
    size: 9,
    solution: [
      8,2,7,1,5,4,3,9,6, 9,6,5,3,2,7,1,4,8, 3,4,1,6,8,9,7,5,2,
      5,9,3,4,6,8,2,7,1, 4,7,2,5,1,3,6,8,9, 6,8,1,9,7,2,4,3,5,
      7,1,8,2,4,5,9,6,3, 2,3,9,7,6,1,8,5,4, 5,4,6,8,3,9,1,2,7
    ],
    puzzle: [
      8,0,0,1,0,0,0,0,6, 0,6,5,0,0,0,1,4,0, 0,4,0,0,8,0,0,5,0,
      5,0,3,0,0,0,2,0,1, 0,7,0,5,0,3,0,8,0, 6,0,1,0,0,0,4,0,5,
      0,1,0,0,4,0,0,6,0, 0,3,9,0,0,0,8,5,0, 5,0,0,0,0,9,0,0,7
    ]
  },
  {
    size: 9,
    solution: [
      1,2,3,4,5,6,7,8,9, 4,5,6,7,8,9,1,2,3, 7,8,9,1,2,3,4,5,6,
      2,1,4,3,6,5,8,9,7, 3,6,5,8,9,7,2,1,4, 8,9,7,2,1,4,3,6,5,
      5,3,1,6,4,2,9,7,8, 6,4,2,9,7,8,5,3,1, 9,7,8,5,3,1,6,4,2
    ],
    puzzle: [
      1,0,3,0,5,0,7,0,9, 0,5,0,7,0,9,0,2,0, 7,0,9,0,2,0,4,0,6,
      2,0,4,0,6,0,8,0,7, 0,6,0,8,0,7,0,1,0, 8,0,7,0,1,0,3,0,5,
      5,0,1,0,4,0,9,0,8, 0,4,0,9,0,8,0,3,0, 9,0,8,0,3,0,6,0,2
    ]
  }
];

let currentLevel = 0;
let hintsLeft = 3;
let isWon = false;

function startTheGame() {
  initAudio();
  startBgMusic();
  document.getElementById('tutorial-screen').style.display = 'none';
  document.getElementById('game-screen').style.display = 'flex';
  loadLevel(0);
}

function loadLevel(lvlIdx) {
  currentLevel = lvlIdx;
  hintsLeft = 3;
  isWon = false;
  
  let lvl = levels[currentLevel];
  document.getElementById('levelTitle').innerText = `MÀN ${currentLevel + 1} (${lvl.size}x${lvl.size})`;
  document.getElementById('hintBadge').innerText = `💡 Gợi ý: ${hintsLeft}`;
  document.getElementById('hintBtn').innerText = `💡 Gợi ý (${hintsLeft})`;
  document.getElementById('nextBtn').style.display = 'none';
  document.getElementById('statusText').style.color = '#7b1fa2';
  document.getElementById('statusText').innerText = 'Hãy điền các số thích hợp vào ô trống!';

  const board = document.getElementById('board');
  board.style.gridTemplateColumns = `repeat(${lvl.size}, ${lvl.size === 5 ? 58 : 38}px)`;
  board.style.gridTemplateRows = `repeat(${lvl.size}, ${lvl.size === 5 ? 58 : 38}px)`;
  board.innerHTML = '';

  let totalCells = lvl.size * lvl.size;
  for (let i = 0; i < totalCells; i++) {
    const input = document.createElement('input');
    input.type = 'number';
    input.min = 1;
    input.max = lvl.size;
    input.className = 'cell';
    input.style.width = lvl.size === 5 ? '58px' : '38px';
    input.style.height = lvl.size === 5 ? '58px' : '38px';
    input.style.fontSize = lvl.size === 5 ? '24px' : '16px';

    let val = lvl.puzzle[i];
    if (val !== 0) {
      input.value = val;
      input.disabled = true;
      input.classList.add('fixed');
    } else {
      input.oninput = (e) => {
        let v = parseInt(e.target.value);
        if (v >= 1 && v <= lvl.size) {
          if (v === lvl.solution[i]) {
            playSound('correct');
          } else {
            playSound('wrong');
          }
        }
      };
    }
    board.appendChild(input);
  }
}

function useHint() {
  if (isWon) return;
  if (hintsLeft <= 0) {
    document.getElementById('statusText').style.color = '#e65100';
    document.getElementById('statusText').innerText = '⚠️ Bạn đã dùng hết lượt gợi ý!';
    return;
  }

  let lvl = levels[currentLevel];
  let inputs = document.querySelectorAll('.cell');
  let emptyIndices = [];

  inputs.forEach((inp, idx) => {
    if (!inp.disabled && (inp.value == "" || parseInt(inp.value) !== lvl.solution[idx])) {
      emptyIndices.push(idx);
    }
  });

  if (emptyIndices.length > 0) {
    let randIdx = emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
    inputs[randIdx].value = lvl.solution[randIdx];
    inputs[randIdx].style.color = '#2e7d32';
    hintsLeft--;
    document.getElementById('hintBadge').innerText = `💡 Gợi ý: ${hintsLeft}`;
    document.getElementById('hintBtn').innerText = `💡 Gợi ý (${hintsLeft})`;
    playSound('correct');
    document.getElementById('statusText').style.color = '#00897b';
    document.getElementById('statusText').innerText = '💡 Đã điền giúp bạn 1 ô đúng!';
  } else {
    document.getElementById('statusText').innerText = '✨ Các ô trống hiện tại đều đã đúng!';
  }
}

function checkAnswer() {
  if (isWon) return;
  let lvl = levels[currentLevel];
  let inputs = document.querySelectorAll('.cell');
  let isAllCorrect = true;

  inputs.forEach((inp, idx) => {
    let val = parseInt(inp.value);
    if (val !== lvl.solution[idx]) {
      isAllCorrect = false;
      if (!inp.disabled) inp.classList.add('error');
    } else {
      inp.classList.remove('error');
    }
  });

  if (isAllCorrect) {
    isWon = true;
    playSound('win');
    document.getElementById('statusText').style.color = '#2e7d32';
    document.getElementById('statusText').innerText = '🎉 Chúc mừng! Bạn đã hoàn thành xuất sắc màn này!';
    
    if (currentLevel < levels.length - 1) {
      document.getElementById('nextBtn').style.display = 'inline-block';
    } else {
      document.getElementById('statusText').innerText = '🏆 TUYỆT VỜI! Bạn đã phá đảo toàn bộ 5 màn Sudoku!';
    }
  } else {
    playSound('lose');
    document.getElementById('statusText').style.color = '#d32f2f';
    document.getElementById('statusText').innerText = '❌ Có số điền chưa chính xác (ô màu đỏ)!';
  }
}

function resetLevel() {
  loadLevel(currentLevel);
}

function nextLevel() {
  if (currentLevel < levels.length - 1) {
    loadLevel(currentLevel + 1);
  }
}
</script>
</body>
</html>
"""

components.html(game_html, height=620)
