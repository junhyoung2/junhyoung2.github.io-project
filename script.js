// script.js
const searchBtn = document.getElementById("search-btn");
const searchInput = document.getElementById("search");
const filterSelect = document.getElementById("filter");
const resultsDiv = document.getElementById("results");

searchBtn.addEventListener("click", () => {
  const query = searchInput.value;
  const filter = filterSelect.value;

  if (!query) {
    alert("검색어를 입력하세요!");
    return;
  }

  fetch(`https://openapi.naver.com/v1/search/local.json?query=${query}&display=5`, {
    headers: {
      "X-Naver-Client-Id": "70MvLdiXExYz9VkNYhJl",
      "X-Naver-Client-Secret": "7goPZ9GkUO",
    },
  })
    .then(response => response.json())
    .then(data => {
      let items = data.items;

      // 필터링 처리
      if (filter === "distance") {
        items = items.sort((a, b) => a.distance - b.distance); // 'distance' 필드 존재 가정
      } else if (filter === "rating") {
        items = items.sort((a, b) => b.rating - a.rating); // 'rating' 필드 존재 가정
      }

      resultsDiv.innerHTML = items
        .map(item => `
          <div class="result-item">
            <img src="https://via.placeholder.com/100" alt="아이콘" style="border-radius: 50%; margin-bottom: 10px;">
            <h3>${item.title}</h3>
            <p><i class="fas fa-map-marker-alt"></i> ${item.address}</p>
            <p>거리: ${item.distance || "알 수 없음"} km</p>
            <p>평점: ${item.rating || "없음"}</p>
            <a href="${item.link}" target="_blank">자세히 보기</a>
          </div>
        `)
        .join('');
    })
    .catch(error => {
      console.error("Error:", error);
      alert("데이터를 불러오는 데 문제가 발생했습니다.");
    });
});
