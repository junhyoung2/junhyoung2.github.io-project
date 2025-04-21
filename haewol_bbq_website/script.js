// DOMContentLoaded 이벤트로 모든 요소가 로드된 후 실행
document.addEventListener("DOMContentLoaded", function() {
    // 모바일용 햄버거 메뉴 토글 기능
    const navToggle = document.getElementById("nav-toggle");
    const navMenu = document.querySelector("#nav-menu ul");
  
    if (navToggle && navMenu) {
      navToggle.addEventListener("click", () => {
        navMenu.classList.toggle("active"); // active 클래스 토글
      });
    }
  
    // 주문 문의 버튼 클릭 시 팝업 생성 및 하이라이트 효과 적용
    const orderInquiryBtn = document.getElementById("order-inquiry");
    if (orderInquiryBtn) {
      orderInquiryBtn.addEventListener("click", () => {
        // 팝업 요소 생성
        const popup = document.createElement("div");
        popup.classList.add("popup");
        popup.innerHTML = `
          <p>주문 문의는 아래 '연락처' 영역을 확인해주세요.</p>
          <button id="highlight-button">확인</button>
        `;
        document.body.appendChild(popup);
  
        const highlightButton = document.getElementById("highlight-button");
        highlightButton.addEventListener("click", () => {
          const contactSection = document.getElementById("contact");
          if (contactSection) {
            contactSection.scrollIntoView({ behavior: "smooth" });
            contactSection.style.transition = "background-color 0.5s";
            contactSection.style.backgroundColor = "#ffffcc";
            setTimeout(() => {
              contactSection.style.backgroundColor = "white";
            }, 1000);
          }
          document.body.removeChild(popup);
        });
      });
    }
  });
  