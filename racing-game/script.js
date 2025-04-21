document.addEventListener("DOMContentLoaded", () => {
    const player = document.querySelector(".player");
    const obstacle = document.querySelector(".obstacle");
    const scoreDisplay = document.getElementById("score");
    const levelDisplay = document.getElementById("level");

    let playerPosition = 125; // 플레이어 초기 위치
    let obstaclePosition = -100; // 장애물 초기 위치
    let score = 0;
    let level = 1; // 초기 레벨
    let gameSpeed = 10; // 장애물 이동 속도
    let gameInterval;

    // 키보드 이벤트로 차량 이동
    document.addEventListener("keydown", (event) => {
        if (event.key === "ArrowLeft" && playerPosition > 0) {
            playerPosition -= 25; // 왼쪽으로 이동
        } else if (event.key === "ArrowRight" && playerPosition < 250) {
            playerPosition += 25; // 오른쪽으로 이동
        }
        player.style.left = `${playerPosition}px`;
    });

    // 장애물 움직이기 및 충돌 감지
    function moveObstacle() {
        obstaclePosition += gameSpeed; // 장애물 이동 속도 적용
        obstacle.style.top = `${obstaclePosition}px`;

        // 장애물이 화면 아래로 나가면 초기화
        if (obstaclePosition > 500) {
            obstaclePosition = -100;

            // 장애물 위치와 크기 랜덤화
            const randomLeft = Math.floor(Math.random() * 250);
            const randomWidth = Math.floor(Math.random() * 50) + 50;
            obstacle.style.left = `${randomLeft}px`;
            obstacle.style.width = `${randomWidth}px`;

            score++; // 점수 증가
            scoreDisplay.textContent = `점수: ${score}`;

            // 레벨 증가
            if (score % 10 === 0) {
                level++;
                levelDisplay.textContent = `레벨: ${level}`;
                gameSpeed += 2; // 속도 증가
            }
        }

        // 충돌 감지
        const playerRect = player.getBoundingClientRect();
        const obstacleRect = obstacle.getBoundingClientRect();

        if (
            playerRect.left < obstacleRect.right &&
            playerRect.right > obstacleRect.left &&
            playerRect.top < obstacleRect.bottom &&
            playerRect.bottom > obstacleRect.top
        ) {
            clearInterval(gameInterval);
            alert(`게임 오버! 점수: ${score} | 레벨: ${level}`);
            location.reload(); // 게임 재시작
        }
    }

    // 게임 루프 시작
    gameInterval = setInterval(moveObstacle, 50);
});
