document.addEventListener("DOMContentLoaded", () => {
    let randomNumber;
    let minRange = 1;
    let maxRange = 100;

    const minNumberInput = document.getElementById("minNumber");
    const maxNumberInput = document.getElementById("maxNumber");
    const setRangeButton = document.getElementById("setRangeButton");
    const rangeMessage = document.getElementById("rangeMessage");

    const userGuessInput = document.getElementById("userGuess");
    const guessButton = document.getElementById("guessButton");
    const resultMessage = document.getElementById("resultMessage");
    const revealAnswerButton = document.getElementById("revealAnswerButton");
    const restartButton = document.getElementById("restartButton");

    // 숫자 범위 설정
    setRangeButton.addEventListener("click", () => {
        const minValue = parseInt(minNumberInput.value);
        const maxValue = parseInt(maxNumberInput.value);

        if (isNaN(minValue) || isNaN(maxValue) || minValue >= maxValue) {
            rangeMessage.textContent = "유효한 범위를 입력하세요! (예: 최소 1, 최대 100)";
            rangeMessage.style.color = "red";
            return;
        }

        minRange = minValue;
        maxRange = maxValue;
        randomNumber = Math.floor(Math.random() * (maxRange - minRange + 1)) + minRange;

        rangeMessage.textContent = `숫자 범위가 ${minRange}부터 ${maxRange}까지 설정되었습니다!`;
        rangeMessage.style.color = "green";

        // 게임 활성화
        userGuessInput.disabled = false;
        guessButton.disabled = false;
        resultMessage.textContent = "";
    });

    // 숫자 맞추기 로직
    guessButton.addEventListener("click", () => {
        const userGuess = parseInt(userGuessInput.value);

        if (isNaN(userGuess) || userGuess < minRange || userGuess > maxRange) {
            resultMessage.textContent = `설정된 범위(${minRange}~${maxRange}) 내의 숫자를 입력하세요!`;
            resultMessage.style.color = "red";
            return;
        }

        if (userGuess === randomNumber) {
            resultMessage.textContent = "축하합니다! 정답입니다!";
            resultMessage.style.color = "green";
            guessButton.style.display = "none";
            revealAnswerButton.style.display = "none";
            restartButton.style.display = "inline-block";
        } else if (userGuess < randomNumber) {
            resultMessage.textContent = "더 큰 숫자를 입력해보세요!";
            resultMessage.style.color = "orange";
        } else {
            resultMessage.textContent = "더 작은 숫자를 입력해보세요!";
            resultMessage.style.color = "orange";
        }
    });

    // 정답 확인하기
    revealAnswerButton.addEventListener("click", () => {
        resultMessage.textContent = `정답은 ${randomNumber}입니다!`;
        resultMessage.style.color = "blue";
        guessButton.style.display = "none";
        revealAnswerButton.style.display = "none";
        restartButton.style.display = "inline-block";
    });

    // 다시 시작하기
    restartButton.addEventListener("click", () => {
        minNumberInput.value = "";
        maxNumberInput.value = "";
        userGuessInput.value = "";
        rangeMessage.textContent = "";
        resultMessage.textContent = "";

        guessButton.style.display = "inline-block";
        revealAnswerButton.style.display = "inline-block";
        restartButton.style.display = "none";

        userGuessInput.disabled = true;
        guessButton.disabled = true;
    });
});
