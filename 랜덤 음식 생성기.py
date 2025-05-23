import random

# 음식 데이터 (음식 이름)
menu = {
    "한식": [
        "비빔밥", "불고기", "김치찌개", "갈비탕", "된장찌개", "잡채", "불닭", "삼겹살", "김밥", "떡볶이",
        "김치볶음밥", "순두부찌개", "소불고기", "제육볶음", "오징어볶음", "된장국", "닭갈비", "동태찌개", "육회", "콩나물국",
        "설렁탕", "부대찌개", "전", "수육", "황태국", "어묵탕", "치즈불닭", "홍합탕", "냉면", "오리불고기",
        "갈비찜", "삼계탕", "닭도리탕", "김치전", "감자탕", "순대국", "칼국수", "떡국", "부침개", "두부김치",
        "열무냉면", "부추전", "쭈꾸미볶음", "백숙", "비지찌개", "고등어조림", "고추장찌개", "조개탕", "삼겹살구이", "볶음밥",
        "간장게장", "갈비구이", "족발", "낙지볶음", "장어구이", "메밀국수", "매갈비찜", "무생채", "치킨", "유린기",
        "곰탕", "청국장찌개", "훈제오리", "고추장불고기", "계란찜", "오징어볶음", "고등어구이", "버섯전골", "전복죽", "간장닭볶음",
        "도토리묵", "사골국", "문어숙회", "육개장", "우엉조림", "곱창", "버섯볶음", "짬뽕", "양념게장", "육전",
        "떡국떡", "양배추찜", "양송이죽", "계란후라이", "메추리알장조림", "새우젓국", "버섯전", "순대", "두부전골",
        "라면", "된장찌개", "포장김밥", "해물파전", "파김치", "돼지갈비", "육두구전골", "배추김치", "미역국", "두부조림"
    ],
    "중식": [
        "짜장면", "짬뽕", "마파두부", "탕수육", "유린기", "볶음밥", "팔보채", "깐풍기", "양장피", "공갈면",
        "라조기", "고추잡채", "군만두", "해물짬뽕", "기스면", "라면", "사천탕면", "대만식볶음면", "춘권", "북경오리",
        "치킨까스", "소롱포", "양장피", "춘장면", "매운탕", "쏘세지탕", "중화비빔면", "홍콩식 해산물", "동파육", "청경채볶음",
        "춘장볶음밥", "베이징덕", "깐풍기", "우육탕면", "소룡포", "베트남쌀국수", "마라탕", "중화죽", "떡볶이",
        "카스텔라", "두반장", "청경채", "꼬치튀김", "도마뱀", "양자강", "중화비빔면", "쌀국수", "마라샹궈", "마파소스",
        "새우볶음밥", "고추기름면", "차오면", "게장", "중화식물냉면", "춘권", "고추짬뽕", "두부조림", "채소볶음밥", "오리요리",
        "상하이식볶음밥", "청경채볶음", "탕수육소스", "돼지고기볶음", "된장탕", "고추장소스", "돼지갈비", "양고기", "떡국", "연어볶음",
        "두부소스", "양고기탕", "양장식볶음밥", "고기두루치기", "조선족두부", "왕만두", "샥스핀", "고기짬뽕", "샤브샤브", "뽕나무두부"
    ],
    "일식": [
        "스시", "라멘", "돈까스", "오코노미야끼", "타코야끼", "우동", "소바", "규동", "카츠동", "텐푸라",
        "야키소바", "돈부리", "교자", "햄버그스테이크", "모츠나베", "초밥", "이나리초밥", "유부초밥", "스키야키", "우메보시",
        "벚꽃초밥", "산도", "가츠동", "참치회", "연어회", "스시롤", "규카츠", "보리차", "미소시루", "아나고",
        "연어덮밥", "장어덮밥", "미소라멘", "치킨카츠", "일본식카레", "사시미", "가리비", "문어덮밥", "파르페",
        "히야시추카", "카라아게", "산치카레", "마끼초밥", "타마고", "초밥세트", "덴푸라우동", "이부리", "스키야키돈", "베이징오리",
        "코로케", "소바", "벤토", "포장마차", "냉모밀", "고로케", "회덮밥", "치킨카레", "간장게장", "햄버거스테이크",
        "치즈돈까스", "파나소", "탕솥", "두부전골", "쇼쿠도", "규카츠", "생선회", "타이완식우육면", "하카타라멘", "차슈라멘",
        "카레라이스", "오므라이스", "온천가", "산슈", "구운어묵", "연어찜", "조개구이", "후리카케", "타코피자", "연어샐러드"
    ],
    "양식": [
        "스파게티", "피자", "스테이크", "리조또", "라자냐", "파스타", "미트볼", "치즈버거", "핫도그", "프렌치프라이",
        "샐러드", "파니니", "퀘사디아", "브리오슈", "치킨파르메잔", "버팔로윙", "카프레제", "시저샐러드", "베이컨롤",
        "프렌치토스트", "부리토", "크림파스타", "클램차우더", "그라탱", "토마토수프", "부에나비스타", "코코넛새우", "볼로네제",
        "칠리콘카르네", "시금치그라탕", "버터치킨", "비프웰던", "연어구이", "팔라펠", "스파게티볼로네즈", "에그베네딕트",
        "쉬림프스크램블", "미트로프", "하와이안피자", "프리타타", "크로아상", "토마토브루스케타", "블랙빈버거", "햄버거",
        "치킨샐러드", "프렌치오믈렛", "맥앤치즈", "쉬림프파스타", "소시지그릴", "라따뚜이", "제트로프리타", "카넬로니",
        "로스트비프", "치킨롤", "카프레제샐러드", "베이컨래프", "라따뚜이", "프랑스식오믈렛", "해산물파스타", "가리비스테이크", "버섯리조또",
        "스파게티볼로네즈", "비스킷", "콩수프", "샌드위치", "스테이크프라이즈", "채소그라탱", "피시앤칩스", "라면", "피자마르게리타", "브루셀스프라우트"
    ]
}

def recommend_food():
    # 각 음식 종류에서 하나씩 무작위로 추천
    recommended_menu = {}
    
    for food_type in menu:
        food = random.choice(menu[food_type])  # 해당 음식 종류에서 무작위 음식 선택
        recommended_menu[food_type] = food
    
    # 추천 결과 출력
    for food_type, food in recommended_menu.items():
        print(f"{food_type} 추천 음식: {food}")

# 추천 함수 호출
recommend_food()
