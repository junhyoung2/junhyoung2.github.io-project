document.addEventListener("DOMContentLoaded", () => {
    const choices = ["가위", "바위", "보"];
    const resultMessage = document.getElementById("resultMessage");
    const userChoiceSpan = document.getElementById("userChoice");
    const computerChoiceSpan = document.getElementById("computerChoice");
    const restartButton = document.getElementById("restartButton");

    // 사용자 선택
    document.querySelectorAll(".choice").forEach(button => {
        button.addEventListener("click", () => {
            const userChoice = button.textContent;
            const computerChoice = choices[Math.floor(Math.random() * choices.length)];
            
            userChoiceSpan.textContent = userChoice;
            computerChoiceSpan.textContent = computerChoice;

            // 결과 판단
            if (userChoice === computerChoice) {
                resultMessage.textContent = "무승부!";
                resultMessage.style.color = "gray";
            } else if (
                (userChoice === "가위" && computerChoice === "보") ||
                (userChoice === "바위" && computerChoice === "가위") ||
                (userChoice === "보" && computerChoice === "바위")
            ) {
                resultMessage.textContent = "사용자가 승리했습니다!";
                resultMessage.style.color = "green";
            } else {
                resultMessage.textContent = "컴퓨터가 승리했습니다!";
                resultMessage.style.color = "red";
            }

            // 다시 시작 버튼 표시
            restartButton.style.display = "block";
        });
    });

    // 다시 시작하기
    restartButton.addEventListener("click", () => {
        userChoiceSpan.textContent = "-";
        computerChoiceSpan.textContent = "-";
        resultMessage.textContent = "";
        restartButton.style.display = "none";
    });
});
