import requests
import json

API_KEY = "AIzaSyAbmR9iixRZAy2Q78IvOluOsLYmD_1Oc60"
CX_ID = "331f511ab5e234261"

def search_google(query, display=3):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query + " 맛집",
        "key": API_KEY,
        "cx": CX_ID,
        "num": display
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        search_results = []
        for item in data.get("items", []):
            title = item.get("title", "제목 없음")
            link = item.get("link", "링크 없음")
            search_results.append({"title": title, "link": link})

        return search_results
    except requests.exceptions.RequestException as e:
        print(f"API 요청 오류: {e}")
        return []

def main():
    categories = input("검색할 음식 종류를 입력하세요 (예: 한식, 일식, 양식, 중식): ").split(',')
    
    results_dict = {}
    for category in categories:
        category = category.strip()
        results = search_google(category)
        results_dict[category] = results
        
        print(f"\n{category} 음식 추천:")
        for idx, food in enumerate(results, 1):
            print(f"{idx}. {food['title']}\n   링크: {food['link']}")
        print("-")
    
    # JSON 형태로 저장
    with open("food_results.json", "w", encoding="utf-8") as f:
        json.dump(results_dict, f, ensure_ascii=False, indent=4)
    print("\n결과가 'food_results.json' 파일에 저장되었습니다!")

if __name__ == "__main__":
    main()
