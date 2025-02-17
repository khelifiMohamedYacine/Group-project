window.addEventListener('load', function () {
    const canvas = document.getElementById('canvas1');
    const ctx = canvas.getContext('2d');
    canvas.width = 1500;
    canvas.height = 800;
    let enemys = [];
    let score = 0;

      this.sound = new Audio();
      this.sound.src = 'backgrorund.wav';
      this.sound.play();


    class InputHandler {
        constructor() {
            this.keys = [];
            window.addEventListener('keydown', function (e) {
                if (e.key === 'Escape') {
                    paused = !paused; // Toggle Pause
                    if (!paused) {
                        animate(0); // Keep playing.
                    }
                }
            });

            // Listen to the “keydown” event (triggered when a key is pressed)
            window.addEventListener('keydown', e => {
                // Check if the arrow keys (ArrowDown, ArrowUp, ArrowLeft, ArrowRight) are pressed
                // And make sure the key is not in the keys array to prevent duplicate additions.
                if ((e.key === 'ArrowDown' ||
                        e.key === 'ArrowUp' ||
                        e.key === 'ArrowLeft' ||
                        e.key === 'ArrowRight' ||
                        e.key === 'a' ||
                        e.key === 'w' ||
                        e.key === 's' ||
                        e.key === 'd') &&
                    this.keys.indexOf(e.key) === -1) {
                    // If the key is not in the array, add it to the keys array
                    this.keys.push(e.key);
                }
            });

            // Listen for the “keyup” event (triggered when the key is released)
            window.addEventListener('keyup', e => {
                // Check to see if it is the arrow keys that are released
                if (
                    e.key === 'ArrowDown' ||
                    e.key === 'ArrowUp' ||
                    e.key === 'ArrowLeft' ||
                    e.key === 'ArrowRight' ||
                    e.key === 'a' ||
                    e.key === 'w' ||
                    e.key === 's' ||
                    e.key === 'd'
                ) {
                    // Finds the index of the key in the keys array.
                    let index = this.keys.indexOf(e.key);
                    // Deletion is performed only if the index is greater than -1 (i.e., the key exists in the array)
                    if (index > -1) {
                        this.keys.splice(index, 1); // Remove the key from the array
                    }
                }
            });

            window.addEventListener('keydown', function (e) {
                if (e.key === ' ' && gameOver) { // Press spacebar to restart the game
                    restartGame();
                }
            });


        }
    }

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

            // **initialize hitbox**
            this.radius = this.width * 0.35; // Character's hitbox radius
            this.centerX = this.x + this.width / 2;
            this.centerY = this.y + this.height / 2;
        }

        draw(context) {
            // characterization
            context.drawImage(
                this.image,
                this.frameX * this.width, this.frameY * this.height,
                this.width, this.height,
                this.x, this.y,
                this.width, this.height
            );


            // context.strokeStyle = 'red';
            // context.beginPath();
            // context.arc(this.centerX, this.centerY, this.radius, 0, Math.PI * 2);
            // context.stroke();
        }

        update(input, deltaTime) {
            if (this.frameTime > this.frameInterval) {
                if (this.frameX >= this.maxFrame) this.frameX = 0;
                else this.frameX++;
                this.frameTime = 0;
            } else {
                this.frameTime += deltaTime;
            }

            // **Controls left and right movement**
            if (input.keys.includes('ArrowRight') || input.keys.includes('d')) {
                this.speed = 5;
            } else if (input.keys.includes('ArrowLeft') || input.keys.includes('a')) {
                this.speed = -5;
            } else {
                this.speed = 0;
            }

            // **jump**
            if ((input.keys.includes('ArrowUp') || input.keys.includes('w')) && this.onGround()) {
                this.vy -= 35;
            }

            // **sit down**
            if ((input.keys.includes('ArrowDown') || input.keys.includes('s')) && this.onGround()) {
                this.sitting = true;
                this.frameY = 6;
                this.maxFrame = 5;

                // **The hitbox moves down 10 pixels when you crouch **
                this.centerY = this.y + this.height / 2 + 100;
            } else {
                this.sitting = false;

                // **Restore hitbox position when released***
                this.centerY = this.y + this.height / 2;
            }

            // **Horizontal movement**
            this.x += this.speed;
            if (this.x < 0) this.x = 0;
            else if (this.x > this.gameWidth - this.width) this.x = this.gameWidth - this.width;

            // **Vertical movement**
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

            // **Update the X-coordinate of the hitbox
            this.centerX = this.x + this.width / 2;
        }

        onGround() {
            return this.y >= this.gameHeight - this.height;
        }
    }


    class Background {
        constructor(gameWidth, gameHeight) {
            this.gameWidth = gameWidth;
            this.gameHeight = gameHeight;
            this.image = document.getElementById('backgroundImage');
            this.x = 0;
            this.y = 0;
            this.width = 2400;
            this.height = 800;
            this.speed = 8;

        }

        draw(context) {

            context.drawImage(this.image, this.x, this.y, this.width, this.height);
            context.drawImage(this.image, this.x + this.width - this.speed, this.y, this.width, this.height);
        }

        update() {
            this.x -= this.speed;
            if (this.x < 0 - this.width) this.x = 0;//Reset the scroll when the first image goes beyond the left side.
        }
    }

    class Enemy {
        constructor(gameWidth, gameHeight, type = 'enemy1') {
            this.gameWidth = gameWidth;
            this.gameHeight = gameHeight;
            this.type = type;

            if (this.type === 'enemy1') {
                this.width = 181;
                this.height = 218;
                this.image = document.getElementById('enemyImage');
                this.speed = 8;
                this.fps = 60;
                this.maxFrame = 0;
                this.y = this.gameHeight - this.height;
                this.hitbox = 0;
            } else {
                this.width = 337;
                this.height = 337;
                this.image = document.getElementById('enemyImage2');
                this.speed = 10 ;
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

            // **initialize hitbox**
            this.radius = this.width * (0.4 - this.hitbox); // 35% of the enemy's size as a radius
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

            // // **Optional: draw hitbox circle (for debugging purposes)**
            // context.beginPath();
            // context.arc(this.centerX, this.centerY, this.radius, 0, Math.PI * 2);
            // context.stroke();
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

            // **更新 hitbox**
            this.centerX = this.x + this.width / 2;
            this.centerY = this.y + this.height / 2;
        }
    }


    function checkCollision(player, enemy) {
        const dx = player.centerX - enemy.centerX;
        const dy = player.centerY - enemy.centerY;
        const distance = Math.sqrt(dx * dx + dy * dy);

        return distance < (player.radius + enemy.radius); // If the distance is less than the sum of the two radii, the collision
    }


    function handleCollisions() {
        for (let enemy of enemys) {
            if (checkCollision(player, enemy)) {
                gameOver = true;
            }
        }
    }


    function handleEnemies(deltaTime) {
        // Controls the time interval between enemy spawns
        if (enemyTimer > enemyInterval + randomEnemyInterval) {
            // 50% Probability of generating different enemy types
            const enemyType = Math.random() < 0.5 ? 'enemy1' : 'enemy2';
            enemys.push(new Enemy(canvas.width, canvas.height, enemyType));

            // Reset the random generation interval
            randomEnemyInterval = Math.random() * 1000 + 200;
            enemyTimer = 0;
        } else {
            enemyTimer += deltaTime;
        }

        // Updated and mapped all enemies
        enemys.forEach((enemy, index) => {
            enemy.draw(ctx);
            enemy.update(deltaTime);

            // Removes enemies that extend beyond the screen, preventing the array from growing indefinitely
            if (enemy.x + enemy.width < 0) {
                enemys.splice(index, 1);
                score++;
            }
        });
    }


    function displayStatusText(context) {
        context.font = '40px Helvetica';
        context.fillStyle = 'black';
        context.fillText('Score: ' + score, 20, 50);
        context.fillStyle = 'white';
        context.fillText('Score: ' + score, 22, 52);
    }

    function restartGame() {
        gameOver = false;
        score = 0;
        enemys = []; // Clear all enemies
        player.x = 50; // Reset player position
        player.y = player.gameHeight - player.height;
        player.vy = 0; // Reset jump state
        enemyTimer = 0;
        animate(0); // Restart the game loop
    }

    function drawPauseMenu() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)'; // Semi-transparent background
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = 'white';
        ctx.font = '50px Helvetica';
        ctx.fillText('Game Paused', canvas.width / 2 - 130, canvas.height / 2 - 30);
        ctx.font = '30px Helvetica';
        ctx.fillText('Press ESC to Resume', canvas.width / 2 - 130, canvas.height / 2 + 20);
    }


    const input = new InputHandler();
    const player = new Player(canvas.width, canvas.height);
    const background = new Background(canvas.width, canvas.height);

    let lastTime = 0;
    let enemyTimer = 0;
    let enemyInterval = 1000;
    let randomEnemyInterval = Math.random() * 1000 + 500;//Random monsters appear.


    let paused = false; // Whether the game is paused
    let gameOver = false;

    function animate(timeStamp) {
        if (gameOver) {
            // Show Game Over text
            ctx.fillStyle = 'white';
            ctx.font = '50px Helvetica';
            ctx.fillText('Game Over', canvas.width / 2 - 120, canvas.height / 2 - 20);
            ctx.font = '30px Helvetica';
            ctx.fillText('Press SPACE or Click to Restart', canvas.width / 2 - 180, canvas.height / 2 + 40);
            return;
        }

        if (paused) {
            drawPauseMenu(); // **Drawing the pause menu**
            return;
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
        requestAnimationFrame(animate);
    }


    animate(0);
});