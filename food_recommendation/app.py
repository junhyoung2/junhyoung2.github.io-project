import requests
from flask import Flask, request, render_template
from geopy.geocoders import Nominatim

# 네이버 API 인증 정보 (네이버 개발자 센터에서 발급)
CLIENT_ID = "70MvLdiXExYz9VkNYhJl"
CLIENT_SECRET = "7goPZ9GkUO"

# 네이버 지역 검색 API URL
NAVER_SEARCH_API_URL = "https://openapi.naver.com/v1/search/local.json"

app = Flask(__name__)

def get_current_location():
    """
    사용자의 현재 위치(위도, 경도)를 가져와서 주소로 변환
    """
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        
        lat = data.get("lat")
        lon = data.get("lon")

        if lat and lon:
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.reverse((lat, lon), language='ko')
            return location.address
        else:
            return None
    except Exception:
        return None

def recommend_food(category, location, display=5):
    """
    네이버 API를 이용한 음식점 추천
    """
    query = f"{location} {category} 맛집"

    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    
    params = {
        "query": query,
        "display": display,
        "sort": "random"
    }

    response = requests.get(NAVER_SEARCH_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        result = response.json()
        items = result.get("items", [])

        if not items:
            return []

        recommendations = []
        for item in items:
            name = item["title"].replace("<b>", "").replace("</b>", "")  
            address = item["roadAddress"]
            link = item["link"]
            recommendations.append({"name": name, "address": address, "link": link})

        return recommendations
    else:
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    category = ""

    if request.method == "POST":
        category = request.form["category"]
        location = get_current_location()

        if not location:
            location = "서울"

        recommendations = recommend_food(category, location)

    return render_template("index.html", recommendations=recommendations, category=category)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
