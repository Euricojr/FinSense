/**
 * Particle Animation for FinSense Hero Section
 * Creates a floating particle effect similar to "Antigravity" style.
 */

const canvas = document.getElementById('hero-particles');
const ctx = canvas.getContext('2d');

let particlesArray;

// Set canvas size to fill the hero section
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.addEventListener('resize', () => {
    resizeCanvas();
    init();
});

// Particle Class
class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 0.5; // Random size between 0.5 and 2.5
        this.speedX = Math.random() * 1 - 0.5; // Random speed between -0.5 and 0.5
        this.speedY = Math.random() * 1 - 0.5;
        this.color = 'rgba(77, 163, 255, 0.6)'; // Light blueish
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        // Wrap around screen
        if (this.x < 0) this.x = canvas.width;
        if (this.x > canvas.width) this.x = 0;
        if (this.y < 0) this.y = canvas.height;
        if (this.y > canvas.height) this.y = 0;
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function init() {
    particlesArray = [];
    // Number of particles based on screen area
    const numberOfParticles = (canvas.width * canvas.height) / 9000;
    for (let i = 0; i < numberOfParticles; i++) {
        particlesArray.push(new Particle());
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
        particlesArray[i].draw();
    }
    requestAnimationFrame(animate);
}

// Start
resizeCanvas();
init();
animate();
