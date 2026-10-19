import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Sudoku Master Deluxe",
    page_icon="🔢",
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
<title>Sudoku Master Deluxe</title>
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
    background: #1e1e1e;
    border: 3px solid #333;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.9);
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 420px;
    width: 100%;
  }
  .screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    text-align: center;
  }
  h1 { font-size: 24px; color: #4fc3f7; margin-bottom: 10px; }
  p { font-size: 14px; color: #b0bec5; margin-bottom: 15px; line-height: 1.5; text-align: left; padding: 0 10px; }
  
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
    padding: 4px 10px;
    border-radius: 12px;
    border: 1px solid #455a64;
    color: #80d8ff;
    font-size: 12px;
  }
  
  /* Bảng lưới Sudoku */
  .sudoku-grid {
    display: grid;
    gap: 2px;
    background: #444;
    padding: 3px;
    border-radius: 6px;
    margin-bottom: 12px;
  }
  .cell {
    background: #282828;
    border: none;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    color: #4fc3f7;
    border-radius: 3px;
    outline: none;
    transition: 0.1s;
  }
  .cell:focus {
    background: #37474f;
    color: #fff;
  }
  .cell.fixed {
    background: #1f1f1f;
    color: #e0e0e0;
  }
  .cell.error {
    background: #c62828 !important;
    color: #fff;
  }

  .controls {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 8px;
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
  button.start-btn { background: #0288d1; box-shadow: 0 3px #01579b; font-size: 16px; padding: 10px 25px; margin-top: 10px;}

  .status-msg {
    margin-top: 8px;
    font-size: 13px;
    font-weight: bold;
    height: 20px;
    text-align: center;
  }
</style>
</head>
<body>

<div class="game-wrapper">

  <!-- MÀN HÌNH HƯỚNG DẪN -->
  <div id="tutorial-screen" class="screen">
    <h1>🔢 HƯỚNG DẪN CHƠI SUDOKU</h1>
    <p>
      <b>1. Mục tiêu:</b> Điền các con số vào ô trống sao cho hợp lệ.<br>
      <b>2. Quy tắc 5x5 / 9x9:</b> Mỗi hàng ngang, cột dọc và vùng lưới nhỏ không được chứa các số trùng lặp.<br>
      <b>3. Lượt gợi ý:</b> Mỗi màn chơi bạn có tối đa <b>3 lượt gợi ý (💡)</b> nếu gặp khó khăn.<br>
      <b>4. Thử thách:</b> Vượt qua đủ 5 màn chơi với độ khó tăng dần từ 5x5 lên 9x9!
    </p>
    <button class="btn start-btn" onclick="startTheGame()">BẮT ĐẦU CHƠI</button>
  </div>

  <!-- MÀN HÌNH CHƠI GAME -->
  <div id="game-screen" class="screen" style="display: none;">
    <div class="header-info">
      <span id="levelTitle">MÀN 1 (5x5)</span>
      <div class="badge" id="hintBadge">Gợi ý còn: 3</div>
    </div>

    <div class="sudoku-grid" id="board"></div>

    <div class="status-msg" id="statusText">Hãy điền các số thích hợp vào ô trống!</div>

    <div class="controls">
      <button onclick="useHint()" class="hint-btn" id="hintBtn">💡 Gợi ý (3)</button>
      <button onclick="checkAnswer()">Kiểm tra</button>
      <button onclick="resetLevel()" style="background: #d32f2f; box-shadow: 0 3px #b71c1c;">Làm lại</button>
      <button onclick="nextLevel()" class="next-btn" id="nextBtn" style="display:none;">Màn tiếp ➡</button>
    </div>
  </div>

</div>

<script>
// Quản lý Âm thanh Web Audio API
let audioCtx = null;
let bgMusicInterval = null;

function initAudio() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
}

// Nhạc nền nhẹ nhàng lặp lại
function startBgMusic() {
  if (bgMusicInterval) return;
  const melody = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63]; // C4, E4, G4, C5...
  let index = 0;
  bgMusicInterval = setInterval(() => {
    try {
      if(!audioCtx) return;
      let osc = audioCtx.createOscillator();
      let gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(melody[index], audioCtx.currentTime);
      gain.gain.setValueAtTime(0.02, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.4);
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.start(); osc.stop(audioCtx.currentTime + 0.4);
      index = (index + 1) % melody.length;
    } catch(e){}
  }, 1200);
}

function playSound(type) {
  initAudio();
  try {
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    if (type === 'correct') {
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(440, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.1);
      gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.start(); osc.stop(audioCtx.currentTime + 0.1);
    } else if (type === 'wrong') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(180, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.2);
      gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2);
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.start(); osc.stop(audioCtx.currentTime + 0.2);
    } else if (type === 'win') {
      const notes = [523.25, 659.25, 783.99, 1046.50];
      notes.forEach((f, i) => {
        setTimeout(() => {
          let o = audioCtx.createOscillator();
          let g = audioCtx.createGain();
          o.type = 'sine'; o.frequency.setValueAtTime(f, audioCtx.currentTime);
          g.gain.setValueAtTime(0.1, audioCtx.currentTime);
          g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.3);
          o.connect(g); g.connect(audioCtx.destination);
          o.start(); o.stop(audioCtx.currentTime + 0.3);
        }, i * 100);
      });
    } else if (type === 'lose') {
      const notes = [300, 250, 200];
      notes.forEach((f, i) => {
        setTimeout(() => {
          let o = audioCtx.createOscillator();
          let g = audioCtx.createGain();
          o.type = 'sawtooth'; o.frequency.setValueAtTime(f, audioCtx.currentTime);
          g.gain.setValueAtTime(0.08, audioCtx.currentTime);
          g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.25);
          o.connect(g); g.connect(audioCtx.destination);
          o.start(); o.stop(audioCtx.currentTime + 0.25);
        }, i * 120);
      });
    }
  } catch(e) {}
}

// Định nghĩa 5 màn chơi (0: ô trống cần điền)
// Màn 1 & 2: 5x5. Màn 3, 4, 5: 9x9.
const levels = [
  // Màn 1 (5x5) - Rất dễ
  {
    size: 5,
    solution: [
      1,2,3,4,5,
      3,4,5,1,2,
      5,1,2,3,4,
      2,3,4,5,1,
      4,5,1,2,3
    ],
    puzzle: [
      1,0,3,0,5,
      0,4,0,1,0,
      5,0,2,0,4,
      0,3,0,5,0,
      4,0,1,0,3
    ]
  },
  // Màn 2 (5x5) - Dễ
  {
    size: 5,
    solution: [
      2,3,1,5,4,
      4,5,2,3,1,
      1,2,3,4,5,
      5,1,4,2,3,
      3,4,5,1,2
    ],
    puzzle: [
      2,0,1,0,4,
      0,5,0,3,0,
      1,0,3,0,5,
      0,1,0,2,0,
      3,0,5,0,2
    ]
  },
  // Màn 3 (9x9) - Trung bình
  {
    size: 9,
    solution: [
      5,3,4,6,7,8,9,1,2,
      6,7,2,1,9,5,3,4,8,
      1,9,8,3,4,2,5,6,7,
      8,5,9,7,6,1,4,2,3,
      4,2,6,8,5,3,7,9,1,
      7,1,3,9,2,4,8,5,6,
      9,6,1,5,3,7,2,8,4,
      2,8,7,4,1,9,6,3,5,
      3,4,5,2,8,6,1,7,9
    ],
    puzzle: [
      5,3,0,0,7,0,0,0,2,
      6,0,0,1,9,5,0,0,0,
      0,9,8,0,0,0,0,6,0,
      8,0,0,0,6,0,0,0,3,
      4,0,0,8,0,3,0,0,1,
      7,0,0,0,2,0,0,0,6,
      0,6,0,0,0,0,2,8,0,
      0,0,0,4,1,9,0,0,5,
      3,0,0,0,8,0,0,7,9
    ]
  },
  // Màn 4 (9x9) - Khó
  {
    size: 9,
    solution: [
      8,2,7,1,5,4,3,9,6,
      9,6,5,3,2,7,1,4,8,
      3,4,1,6,8,9,7,5,2,
      5,9,3,4,6,8,2,7,1,
      4,7,2,5,1,3,6,8,9,
      6,8,1,9,7,2,4,3,5,
      7,1,8,2,4,5,9,6,3,
      2,3,9,7,6,1,8,5,4,
      5,4,6,8,3,9,1,2,7
    ],
    puzzle: [
      8,0,0,1,0,0,0,0,6,
      0,6,5,0,0,0,1,4,0,
      0,4,0,0,8,0,0,5,0,
      5,0,3,0,0,0,2,0,1,
      0,7,0,5,0,3,0,8,0,
      6,0,1,0,0,0,4,0,5,
      0,1,0,0,4,0,0,6,0,
      0,3,9,0,0,0,8,5,0,
      5,0,0,0,0,9,0,0,7
    ]
  },
  // Màn 5 (9x9) - Siêu khó
  {
    size: 5, // Sẽ override thành 9x9 ở logic dưới
    size: 9,
    solution: [
      1,2,3,4,5,6,7,8,9,
      4,5,6,7,8,9,1,2,3,
      7,8,9,1,2,3,4,5,6,
      2,1,4,3,6,5,8,9,7,
      3,6,5,8,9,7,2,1,4,
      8,9,7,2,1,4,3,6,5,
      5,3,1,6,4,2,9,7,8,
      6,4,2,9,7,8,5,3,1,
      9,7,8,5,3,1,6,4,2
    ],
    puzzle: [
      1,0,3,0,5,0,7,0,9,
      0,5,0,7,0,9,0,2,0,
      7,0,9,0,2,0,4,0,6,
      2,0,4,0,6,0,8,0,7,
      0,6,0,8,0,7,0,1,0,
      8,0,7,0,1,0,3,0,5,
      5,0,1,0,4,0,9,0,8,
      0,4,0,9,0,8,0,3,0,
      9,0,8,0,3,0,6,0,2
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
  document.getElementById('hintBadge').innerText = `Gợi ý còn: ${hintsLeft}`;
  document.getElementById('hintBtn').innerText = `💡 Gợi ý (${hintsLeft})`;
  document.getElementById('nextBtn').style.display = 'none';
  document.getElementById('statusText').style.color = '#fff';
  document.getElementById('statusText').innerText = 'Hãy điền các số thích hợp vào ô trống!';

  const board = document.getElementById('board');
  board.style.gridTemplateColumns = `repeat(${lvl.size}, ${lvl.size === 5 ? 50 : 35}px)`;
  board.style.gridTemplateRows = `repeat(${lvl.size}, ${lvl.size === 5 ? 50 : 35}px)`;
  board.innerHTML = '';

  let totalCells = lvl.size * lvl.size;
  for (let i = 0; i < totalCells; i++) {
    const input = document.createElement('input');
    input.type = 'number';
    input.min = 1;
    input.max = lvl.size;
    input.className = 'cell';
    input.style.width = lvl.size === 5 ? '50px' : '35px';
    input.style.height = lvl.size === 5 ? '50px' : '35px';
    input.style.fontSize = lvl.size === 5 ? '20px' : '16px';

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
    document.getElementById('statusText').style.color = '#ff9800';
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
    inputs[randIdx].style.color = '#00e676';
    hintsLeft--;
    document.getElementById('hintBadge').innerText = `Gợi ý còn: ${hintsLeft}`;
    document.getElementById('hintBtn').innerText = `💡 Gợi ý (${hintsLeft})`;
    playSound('correct');
    document.getElementById('statusText').style.color = '#00bcd4';
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
    document.getElementById('statusText').style.color = '#66bb6a';
    document.getElementById('statusText').innerText = '🎉 Chúc mừng! Bạn đã hoàn thành xuất sắc màn này!';
    
    if (currentLevel < levels.length - 1) {
      document.getElementById('nextBtn').style.display = 'inline-block';
    } else {
      document.getElementById('statusText').innerText = '🏆 TUYỆT VỜI! Bạn đã phá đảo toàn bộ 5 màn Sudoku!';
    }
  } else {
    playSound('lose');
    document.getElementById('statusText').style.color = '#ef5350';
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

components.html(game_html, height=580)
