const API_KEY = "AIzaSyAbmR9iixRZAy2Q78IvOluOsLYmD_1Oc60"; // Google API 키
const CX_ID = "331f511ab5e234261"; // Custom Search 엔진 ID

async function searchFood() {
    let query = document.getElementById("query").value;
    let category = document.getElementById("category").value;
    
    if (!query) {
        alert("검색어를 입력하세요.");
        return;
    }
    
    if (category) {
        query += ` ${category}`;
    }

    saveSearchHistory(query); // 검색어 저장

    const url = `https://www.googleapis.com/customsearch/v1?q=${encodeURIComponent(query)}&key=${API_KEY}&cx=${CX_ID}&num=10&searchType=image`;
    console.log("API 요청 URL:", url); 

    try {
        const response = await fetch(url);
        const data = await response.json();

        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";

        let uniqueUrls = new Set(); // 중복 체크용 Set

        if (data.items) {
            data.items.forEach(item => {
                if (!uniqueUrls.has(item.link)) { // 중복 URL 제외
                    uniqueUrls.add(item.link);

                    const div = document.createElement("div");
                    div.className = "result-item shadow-lg rounded-lg p-4 bg-white";

                    div.innerHTML = `
                        <h3 class="text-lg font-semibold"><a href="${item.image.contextLink}" target="_blank" class="text-blue-600">${item.title}</a></h3>
                        <img src="${item.link}" alt="${item.title}" class="rounded-lg w-full mt-2">
                        <p class="text-gray-600 mt-2">${item.snippet}</p>
                    `;

                    resultsDiv.appendChild(div);
                }
            });
        } else {
            resultsDiv.innerHTML = "<p class='text-gray-600'>검색 결과가 없습니다.</p>";
        }
    } catch (error) {
        console.error("API 요청 오류:", error);
        alert("검색 중 오류가 발생했습니다.");
    }
}

