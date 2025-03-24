window.addEventListener('load', function () {

    const imageCycles = [1, 2, 2, 1]; // Number of cycles for each background image

    // load level data dynamically, it is what differenciates levels from each other
    //const gameData = JSON.parse(document.getElementById("game-data").textContent);

    //console.log("Raw Game Data:", gameData);
    const speedMultiplier = Number(this.document.getElementById("speedMultiplier_").value);
    const enemySpawnRate = Number(this.document.getElementById("enemySpawnRate_").value);
    const level = Number(this.document.getElementById("level_").value);

    console.log("Speed Multiplier:", speedMultiplier);
    console.log("Enemy Spawn Rate:", enemySpawnRate);
    console.log("Level:", level);

    // Game Variables
    let enemys = [];
    let score = 0;
    let paused = false;
    let gameOver = false;
    let levelCompleted = false;

    // Canvas Setup
    const canvas = document.getElementById('canvas1');
    const ctx = canvas.getContext('2d');
    canvas.width = 1500;
    canvas.height = 800;

    class Player {
        constructor(gameWidth, gameHeight) {
            this.gameWidth = gameWidth;
            this.gameHeight = gameHeight;
            this.width = 286.5;
            this.height = 261.5;
            this.x = 50;
            this.y = this.gameHeight - this.height;
            this.image = document.getElementById('playerImage');
            this.frameX = 0;
            this.maxFrame = 8;
            this.fps = 60;
            this.frameTime = 0;
            this.frameInterval = 1000 / this.fps;
            this.frameY = 0;
            this.speed = 0;
            this.vy = 0;
            this.weight = 1;
            this.sitting = false;
            this.radius = this.width * 0.35;
            this.centerX = this.x + this.width / 2;
            this.centerY = this.y + this.height / 2;
        }

        draw(context) {
            context.drawImage(
                this.image,
                this.frameX * this.width, this.frameY * this.height,
                this.width, this.height,
                this.x, this.y,
                this.width, this.height
            );
        }

        update(input, deltaTime) {
            if (this.frameTime > this.frameInterval) {
                if (this.frameX >= this.maxFrame) this.frameX = 0;
                else this.frameX++;
                this.frameTime = 0;
            } else {
                this.frameTime += deltaTime;
            }

            if (input.keys.includes('ArrowRight') || input.keys.includes('d')) {
                this.speed = 5;
            } else if (input.keys.includes('ArrowLeft') || input.keys.includes('a')) {
                this.speed = -5;
            } else {
                this.speed = 0;
            }

            if ((input.keys.includes('ArrowUp') || input.keys.includes('w')) && this.onGround()) {
                this.vy -= 35;
            }

            if ((input.keys.includes('ArrowDown') || input.keys.includes('s')) && this.onGround()) {
                this.sitting = true;
                this.frameY = 6;
                this.maxFrame = 5;
                this.centerY = this.y + this.height / 2 + 100;
            } else {
                this.sitting = false;
                this.centerY = this.y + this.height / 2;
            }

            this.x += this.speed;
            if (this.x < 0) this.x = 0;
            else if (this.x > this.gameWidth - this.width) this.x = this.gameWidth - this.width;

            this.y += this.vy;
            if (!this.onGround()) {
                this.vy += this.weight;
                this.frameY = 1;
                this.maxFrame = 5;
            } else if (this.sitting) {
                this.frameY = 6;
                this.maxFrame = 5;
            } else {
                this.vy = 0;
                this.frameY = 3;
                this.maxFrame = 7;
            }

            if (this.y > this.gameHeight - this.height) this.y = this.gameHeight - this.height;

            this.centerX = this.x + this.width / 2;
        }

        onGround() {
            return this.y >= this.gameHeight - this.height;
        }
    }

    // Background Class
    class Background {
        constructor(gameWidth, gameHeight, imageCycles) {
            this.gameWidth = gameWidth;
            this.gameHeight = gameHeight;
            this.imageCycles = imageCycles;
            this.images = [
                document.getElementById('backgroundImage1'),
                document.getElementById('backgroundImage2'),
                document.getElementById('backgroundImage3'),
                document.getElementById('backgroundImage4')
            ];
            this.imageIndex = 0;
            this.imageCount = 0;
            this.currentImage = this.images[this.imageIndex];
            this.nextImage = null;
            this.transitionProgress = 0;
            this.isTransitioning = false;
            this.x = 0;
            this.y = 0;
            this.width = 2400;
            this.height = 800;
            this.speed = 7.9 * speedMultiplier; // A the constant is slightly < 8 for a subtle paralax effect
            this.isStageComplete = false;
        }

        draw(context) {
            context.drawImage(this.currentImage, this.x, this.y, this.width, this.height);
            context.drawImage(this.currentImage, this.x + this.width - this.speed, this.y, this.width, this.height);

            if (this.isTransitioning) {
                context.drawImage(this.nextImage, this.x + this.width, this.y, this.width, this.height);
                context.drawImage(this.nextImage, this.x + this.width * 2 - this.speed, this.y, this.width, this.height);
            }
        }

        update() {
            if (this.isStageComplete) return;

            this.x -= this.speed;

            if (this.x < 0 - this.width) {
                this.x = 0;
                this.imageCount++;

                if (this.imageCount >= this.imageCycles[this.imageIndex]) {
                    if (this.imageIndex === this.images.length - 1) {
                        this.isStageComplete = true;
                        levelCompleted = true; // Level is completed
                        setTimeout(() => {
                            window.location.href = "/games/";
                        }, 2000); // Redirect after 2 seconds
                    } else {
                        this.startTransition();
                    }
                }
            }

            if (this.isTransitioning) {
                this.transitionProgress += this.speed / this.width;

                if (this.transitionProgress >= 1) {
                    this.completeTransition();
                }
            }
        }

        startTransition() {
            this.isTransitioning = true;
            this.transitionProgress = 0;
            this.nextImage = this.images[(this.imageIndex + 1) % this.images.length];
        }

        completeTransition() {
            this.isTransitioning = false;
            this.imageIndex = (this.imageIndex + 1) % this.images.length;
            this.imageCount = 0;
            this.currentImage = this.images[this.imageIndex];
            this.nextImage = null;
        }

        reset() {
            this.imageIndex = 0;
            this.imageCount = 0;
            this.currentImage = this.images[this.imageIndex];
            this.isStageComplete = false;
            this.x = 0;
        }
    }

    // Enemy Class
    class Enemy {
        constructor(gameWidth, gameHeight, type = 'enemy1') {
            this.gameWidth = gameWidth;
            this.gameHeight = gameHeight;
            this.type = type;

            if (this.type === 'enemy1') {
                this.width = 181;
                this.height = 218;
                this.image = document.getElementById('enemyImage');
                this.speed = 8 * speedMultiplier; // Adjusted by speedMultiplier
                this.fps = 60;
                this.maxFrame = 0;
                this.y = this.gameHeight - this.height;
                this.hitbox = 0;
            } else {
                this.width = 337;
                this.height = 337;
                this.image = document.getElementById('enemyImage2');
                this.speed = 10 * speedMultiplier; // Adjusted by speedMultiplier
                this.fps = 60;
                this.maxFrame = 0;
                this.flyHeight = Math.random() * (300 - 200 + 1) + 100;
                this.y = this.gameHeight - this.height - this.flyHeight;
                this.hitbox = 0.2;
            }

            this.x = this.gameWidth;
            this.frameX = 0;
            this.frameTime = 0;
            this.frameInterval = 1000 / this.fps;
            this.radius = this.width * (0.4 - this.hitbox);
            this.centerX = this.x + this.width / 2;
            this.centerY = this.y + this.height / 2;
        }

        draw(context) {
            context.drawImage(
                this.image,
                this.frameX * this.width, 0,
                this.width, this.height,
                this.x, this.y,
                this.width, this.height
            );
        }

        update(deltaTime) {
            if (this.frameTime > this.frameInterval) {
                if (this.frameX >= this.maxFrame) this.frameX = 0;
                else this.frameX++;
                this.frameTime = 0;
            } else {
                this.frameTime += deltaTime;
            }

            this.x -= this.speed;
            this.centerX = this.x + this.width / 2;
            this.centerY = this.y + this.height / 2;
        }
    }

    // Input Handler Class
    class InputHandler {
        constructor() {
            this.keys = [];
            window.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    paused = !paused;
                    if (!paused) animate(0);
                }
                if ((e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'ArrowLeft' || e.key === 'ArrowRight' || e.key === 'a' || e.key === 'w' || e.key === 's' || e.key === 'd') && this.keys.indexOf(e.key) === -1) {
                    this.keys.push(e.key);
                }
                if (e.key === ' ' && (gameOver || levelCompleted)) {
                    restartGame(); // Restart the game when spacebar is pressed
                }
            });
            window.addEventListener('keyup', (e) => {
                if (e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'ArrowLeft' || e.key === 'ArrowRight' || e.key === 'a' || e.key === 'w' || e.key === 's' || e.key === 'd') {
                    this.keys.splice(this.keys.indexOf(e.key), 1);
                }
            });
            canvas.addEventListener('click', () => {
                if (gameOver || levelCompleted) {
                    restartGame(); // Restart the game when the canvas is clicked
                }
            });
        }
    }

    // Collision Detection
    function checkCollision(player, enemy) {
        const dx = player.centerX - enemy.centerX;
        const dy = player.centerY - enemy.centerY;
        const distance = Math.sqrt(dx * dx + dy * dy);
        return distance < (player.radius + enemy.radius);
    }

    function handleCollisions() {
        for (let enemy of enemys) {
            if (checkCollision(player, enemy)) {
                gameOver = true;
            }
        }
    }

    // Enemy Handling
    let enemyTimer = 0;
    let randomEnemyInterval = Math.random() * 1000 + 500;

    function handleEnemies(deltaTime) {
        if (enemyTimer > enemySpawnRate + randomEnemyInterval) {
            const enemyType = Math.random() < 0.5 ? 'enemy1' : 'enemy2';
            enemys.push(new Enemy(canvas.width, canvas.height, enemyType));
            randomEnemyInterval = Math.random() * 1000 + 200;
            enemyTimer = 0;
        } else {
            enemyTimer += deltaTime;
        }

        enemys.forEach((enemy, index) => {
            enemy.draw(ctx);
            enemy.update(deltaTime);

            if (enemy.x + enemy.width < 0) {
                enemys.splice(index, 1);
                score++;
            }
        });
    }

    // Status Display
    function displayStatusText(context) {
        context.font = '40px Helvetica';
        context.fillStyle = 'black';
        context.fillText('Score: ' + score, 20, 50);
        context.fillText('Level: ' + level, 20, 100);
        context.fillStyle = 'white';
        context.fillText('Score: ' + score, 22, 52);
        context.fillText('Level: ' + level, 22, 102);
    }

    // Restart Game
    function restartGame() {
        console.log('Restarting game...'); // Debugging
        gameOver = false;
        levelCompleted = false;
        score = 0;
        enemys = [];
        player.x = 50;
        player.y = player.gameHeight - player.height;
        player.vy = 0;
        player.frameX = 0;
        player.frameY = 0;
        player.sitting = false;
        enemyTimer = 0;
        background.reset();
        animate(0); // Restart the game loop
    }

    // Pause Menu
    function drawPauseMenu() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'white';
        ctx.font = '50px Helvetica';
        ctx.fillText('Game Paused', canvas.width / 2 - 130, canvas.height / 2 - 30);
        ctx.font = '30px Helvetica';
        ctx.fillText('Press ESC to Resume', canvas.width / 2 - 130, canvas.height / 2 + 20);
    }

    // Game Initialization
    const input = new InputHandler();
    const player = new Player(canvas.width, canvas.height);
    const background = new Background(canvas.width, canvas.height, imageCycles);

    let lastTime = 0;

    // Animation Loop
    function animate(timeStamp) {
        if (gameOver) {
            ctx.fillStyle = 'white';
            ctx.font = '50px Helvetica';
            ctx.fillText('Game Over', canvas.width / 2 - 120, canvas.height / 2 - 20);
            ctx.font = '30px Helvetica';
            ctx.fillText('Score: ' + score, canvas.width / 2 - 80, canvas.height / 2 + 40);
            ctx.fillText('Press SPACE or Click to Restart', canvas.width / 2 - 220, canvas.height / 2 + 100);
            return; // Stop the game loop
        }

        if (levelCompleted) {
            ctx.fillStyle = 'white';
            ctx.font = '50px Helvetica';
            ctx.fillText('Level Completed!', canvas.width / 2 - 150, canvas.height / 2 - 20);
            ctx.font = '30px Helvetica';
            ctx.fillText('Score: ' + score, canvas.width / 2 - 80, canvas.height / 2 + 40);

            // edge case for odd levels with no obstacles
            if (score < 1) {
                score = 1;
            }

            // Send completion data to backend
            fetch('/mark_jumping_game_complete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    task_id: level,
                    score: score
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);  // Show the message like "Level Complete. X reward points"
                }
            })
            .catch(error => {
                alert('Error marking game level complete');
            });
            return; // Stop the game loop
        }

        if (paused) {
            drawPauseMenu();
            return; // Stop the game loop
        }

        const deltaTime = timeStamp - lastTime;
        lastTime = timeStamp;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        background.draw(ctx);
        background.update();

        player.draw(ctx);
        player.update(input, deltaTime);

        handleEnemies(deltaTime);
        handleCollisions();

        displayStatusText(ctx);

        requestAnimationFrame(animate); // Continue the game loop
    }

    animate(0); // Start the game
});