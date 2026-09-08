const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const tileSize = 40;
const maze = [
  [1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,1,0,0,0,0,1],
  [1,0,1,1,1,0,1,0,1,1,0,1],
  [1,0,1,0,0,0,0,0,0,1,0,1],
  [1,0,1,0,1,1,1,1,0,1,0,1],
  [1,0,0,0,0,0,0,1,0,1,0,1],
  [1,1,1,1,1,1,0,1,0,1,0,1],
  [1,0,0,0,0,1,0,1,0,1,0,1],
  [1,0,1,1,0,1,0,0,0,1,0,1],
  [1,0,0,1,0,0,0,1,0,0,0,1],
  [1,0,0,0,0,1,0,0,0,1,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1]
];

let playerX = 1;
let playerY = 1;

function drawMaze() {
  for (let y = 0; y < maze.length; y++) {
    for (let x = 0; x < maze[y].length; x++) {
      if (maze[y][x] === 1) {
        ctx.fillStyle = "#444";
      } else {
        ctx.fillStyle = "#222";
      }
      ctx.fillRect(x * tileSize, y * tileSize, tileSize, tileSize);
    }
  }
}

function drawPlayer() {
  ctx.fillStyle = "yellow";
  ctx.fillRect(playerX * tileSize, playerY * tileSize, tileSize, tileSize);
}

function drawGoal() {
  ctx.fillStyle = "lime";
  ctx.fillRect(10 * tileSize, 10 * tileSize, tileSize, tileSize);
}

function update() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawMaze();
  drawGoal();
  drawPlayer();

  if (playerX === 10 && playerY === 10) {
    alert("クリア！");
  }
}

document.addEventListener("keydown", (e) => {
  let newX = playerX;
  let newY = playerY;

  if (e.key === "ArrowUp") newY--;
  if (e.key === "ArrowDown") newY++;
  if (e.key === "ArrowLeft") newX--;
  if (e.key === "ArrowRight") newX++;

  if (maze[newY][newX] === 0) {
    playerX = newX;
    playerY = newY;
  }

  update();
});

update();
