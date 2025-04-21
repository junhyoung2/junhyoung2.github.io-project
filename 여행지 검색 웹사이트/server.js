const express = require("express");
const fetch = require("node-fetch");
const app = express();

const CLIENT_ID = "dmlkmvsk54"; // 네이버 클라이언트 ID
const CLIENT_SECRET = "kiKoR8yH2izUZv3ui8Y4ucU8NGFUhR17uxrx3714"; // 네이버 클라이언트 Secret

app.get("/api/search", (req, res) => {
  const query = req.query.query;

  fetch(`https://openapi.naver.com/v1/search/local.json?query=${encodeURIComponent(query)}&display=5`, {
    headers: {
      "X-Naver-Client-Id": CLIENT_ID,
      "X-Naver-Client-Secret": CLIENT_SECRET,
    },
  })
    .then((response) => response.json())
    .then((data) => res.json(data))
    .catch((error) => {
      console.error("API 요청 중 오류:", error);
      res.status(500).json({ error: "API 호출 실패" });
    });
});
// 정적 파일 서빙
app.use(express.static(__dirname));
app.listen(3000, () => {
  console.log("서버가 http://localhost:3000 에서 실행 중입니다.");
});

