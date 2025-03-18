document.addEventListener("DOMContentLoaded", () => {
    let randomNumber = Math.floor(Math.random() * 100) + 1; // 1부터 100까지 랜덤 숫자 생성
    const userGuessInput = document.getElementById("userGuess");
    const guessButton = document.getElementById("guessButton");
    const resultMessage = document.getElementById("resultMessage");
    const restartButton = document.getElementById("restartButton");

    guessButton.addEventListener("click", () => {
        const userGuess = parseInt(userGuessInput.value);

        if (isNaN(userGuess) || userGuess < 1 || userGuess > 100) {
            resultMessage.textContent = "1부터 100 사이의 숫자를 입력하세요!";
            resultMessage.style.color = "red";
            return;
        }

        if (userGuess === randomNumber) {
            resultMessage.textContent = "축하합니다! 정답입니다!";
            resultMessage.style.color = "green";
            guessButton.style.display = "none";
            restartButton.style.display = "inline-block";
        } else if (userGuess < randomNumber) {
            resultMessage.textContent = "더 큰 숫자를 입력해보세요!";
            resultMessage.style.color = "orange";
        } else {
            resultMessage.textContent = "더 작은 숫자를 입력해보세요!";
            resultMessage.style.color = "orange";
        }
    });

    restartButton.addEventListener("click", () => {
        randomNumber = Math.floor(Math.random() * 100) + 1; // 새로운 숫자 생성
        userGuessInput.value = "";
        resultMessage.textContent = "";
        guessButton.style.display = "inline-block";
        restartButton.style.display = "none";
    });
});
