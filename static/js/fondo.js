const canvas = document.getElementById("stars");
const ctx = canvas.getContext("2d");

let stars = [];
let meteors = [];
let numStars = 150;

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

// Crear estrellas (solo se mueven lentamente)
function createStars() {
  stars = [];
  for (let i = 0; i < numStars; i++) {
    const radius = Math.random() * 2; // estrellas más variadas
    const depth = 0.5 + Math.random() * 1.5; // profundidad (0.5=lejanas, 2=cercanas)

    stars.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      radius: radius,
      speedX: (Math.random() - 0.5) * 0.2 * depth, 
      speedY: (Math.random() - 0.5) * 0.2 * depth
    });
  }
}

// Crear meteorito desde un borde
function createMeteor() {
  const edge = Math.floor(Math.random() * 3); // 0=arriba, 1=izquierda, 2=derecha
  let startX, startY, angle;

  if (edge === 0) { 
    startX = Math.random() * canvas.width;
    startY = -50;
    angle = Math.PI / 2 + (Math.random() - 0.5) * 0.3;
  } else if (edge === 1) {
    startX = -50;
    startY = Math.random() * (canvas.height / 2);
    angle = (Math.random() * Math.PI) / 4;
  } else {
    startX = canvas.width + 50;
    startY = Math.random() * (canvas.height / 2);
    angle = Math.PI - (Math.random() * Math.PI) / 4;
  }

  meteors.push({
    x: startX,
    y: startY,
    length: Math.random() * 120 + 80,
    speed: Math.random() * 8 + 6,
    angle: angle,
    opacity: 1
  });
}

// Dibujar estrellas
function drawStars() {
  ctx.fillStyle = "white";
  for (let star of stars) {
    ctx.beginPath();
    ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
    ctx.fill();
  }
}

// Dibujar meteoritos con cola difuminada
function drawMeteors() {
  for (let meteor of meteors) {
    let gradient = ctx.createLinearGradient(
      meteor.x,
      meteor.y,
      meteor.x - meteor.length * Math.cos(meteor.angle),
      meteor.y - meteor.length * Math.sin(meteor.angle)
    );
    gradient.addColorStop(0, `rgba(255,255,255,${meteor.opacity})`);
    gradient.addColorStop(1, "rgba(255,255,255,0)");

    ctx.strokeStyle = gradient;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(meteor.x, meteor.y);
    ctx.lineTo(
      meteor.x - meteor.length * Math.cos(meteor.angle),
      meteor.y - meteor.length * Math.sin(meteor.angle)
    );
    ctx.stroke();
  }
}

// Actualizar posiciones
function update() {
  // estrellas
  for (let star of stars) {
    star.x += star.speedX;
    star.y += star.speedY;

    // si salen del canvas, reaparecen
    if (star.x < 0) star.x = canvas.width;
    if (star.x > canvas.width) star.x = 0;
    if (star.y < 0) star.y = canvas.height;
    if (star.y > canvas.height) star.y = 0;
  }

  // meteoritos
  for (let meteor of meteors) {
    meteor.x += meteor.speed * Math.cos(meteor.angle);
    meteor.y += meteor.speed * Math.sin(meteor.angle);
    meteor.opacity -= 0.008;
  }
  meteors = meteors.filter(m => m.opacity > 0);
}

// Animación
function animate() {
  ctx.fillStyle = "rgba(0,0,15,0.6)"; // fondo oscuro con leve rastro
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  drawStars();
  drawMeteors();
  update();
  requestAnimationFrame(animate);
}

createStars();
animate();

// Meteoritos cada 8–18 segundos
setInterval(() => {
  if (Math.random() < 0.9) {
    createMeteor();
  }
}, Math.random() * 2000 + 8000);