import requests
import json

def search_naver(query, client_id, client_secret, display=3):
    url = "https://openapi.naver.com/v1/search/local.json"

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {
        "query": query,
        "display": display
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()
        
        if 'items' in result:
            return [
                {
                    "title": item['title'],
                    "link": item['link'],
                    "address": item.get('address', '주소 정보 없음')
                } for item in result['items']
            ]
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"API 요청 오류: {e}")
        return []

def main():
    client_id = "70MvLdiXExYz9VkNYhJl"  # 네이버 API 클라이언트 ID
    client_secret = "7goPZ9GkUO"  # 네이버 API 클라이언트 시크릿
    
    categories = input("검색할 음식 종류를 입력하세요 (예: 한식, 일식, 양식, 중식): ").split(',')
    
    results_dict = {}
    for category in categories:
        category = category.strip()
        results = search_naver(category, client_id, client_secret)
        results_dict[category] = results
        
        print(f"\n{category} 음식 추천:")
        for idx, food in enumerate(results, 1):
            print(f"{idx}. {food['title']}\n   링크: {food['link']}\n   주소: {food['address']}")
        print("-")
    
    # JSON 형태로 저장 (캐싱 가능)
    with open("food_results.json", "w", encoding="utf-8") as f:
        json.dump(results_dict, f, ensure_ascii=False, indent=4)
    print("\n결과가 'food_results.json' 파일에 저장되었습니다!")

if __name__ == "__main__":
    main()
