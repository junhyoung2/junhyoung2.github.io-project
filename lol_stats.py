import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtGui import QPixmap, QImage
from io import BytesIO

# 🔹 라이엇 API 정보 설정
API_KEY = "RGAPI-9bb997ee-91cc-478c-b016-9bc4fb75b044"  # 여기에 본인의 API 키 입력
SUMMONER_NAME = "싹다 장인"  # 여기에 본인의 소환사명 입력
REGION = "kr"

# 🔹 API 요청 함수
def get_summoner_data():
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{SUMMONER_NAME}?api_key={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_match_history(puuid, count=10):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_match_details(match_id):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
    response = requests.get(url)
    return response.json()

# 🔹 GUI 클래스 정의
class LolDataApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("롤 플레이 데이터 분석")
        self.setGeometry(100, 100, 1000, 800)

        layout = QVBoxLayout()

        # 🔹 API 데이터 가져오기
        summoner_data = get_summoner_data()
        puuid = summoner_data['puuid']
        match_ids = get_match_history(puuid)

        # 🔹 플레이한 챔피언 정보 저장
        champion_play_data = {}
        total_games = len(match_ids)
        win_data = []
        kda_data = []
        game_times = []

        for match_id in match_ids:
            match_data = get_match_details(match_id)
            for participant in match_data['info']['participants']:
                if participant['puuid'] == puuid:
                    champion = participant['championName']
                    champion_play_data[champion] = champion_play_data.get(champion, 0) + 1
                    win_data.append(1 if participant['win'] else 0)
                    kda = (participant['kills'] + participant['assists']) / max(1, participant['deaths'])
                    kda_data.append(kda)
                    game_times.append(pd.to_datetime(match_data['info']['gameStartTimestamp'], unit='ms').hour)

        # 🔹 챔피언별 플레이 횟수 시각화 (파이 차트)
        df_champ = pd.DataFrame(list(champion_play_data.items()), columns=["챔피언", "플레이 횟수"])
        plt.figure(figsize=(6, 6))
        plt.pie(df_champ["플레이 횟수"], labels=df_champ["챔피언"], autopct="%1.1f%%", startangle=140)
        plt.title("챔피언별 플레이 비율")
        plt.savefig("champion_play.png")

        # 🔹 승률 그래프 추가
        plt.figure(figsize=(6, 4))
        plt.plot(range(1, len(win_data) + 1), win_data, marker='o', linestyle='-', color='b')
        plt.title("최근 10경기 승률")
        plt.xlabel("게임 번호")
        plt.ylabel("승리 여부 (1=승, 0=패)")
        plt.savefig("win_rate.png")

        # 🔹 KDA 분석 그래프
        plt.figure(figsize=(6, 4))
        plt.plot(range(1, len(kda_data) + 1), kda_data, marker='s', linestyle='-', color='r')
        plt.title("KDA 변화")
        plt.xlabel("게임 번호")
        plt.ylabel("KDA")
        plt.savefig("kda_graph.png")

        # 🔹 게임 시간대 분석 (히트맵)
        plt.figure(figsize=(6, 4))
        sns.histplot(game_times, bins=24, kde=True, color='g')
        plt.title("플레이 시간대 분석")
        plt.xlabel("시간 (24h 기준)")
        plt.ylabel("게임 수")
        plt.savefig("game_time.png")

        # 🔹 GUI 요소 추가
        title_label = QLabel(f"소환사: {summoner_data['name']}")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        # 🔹 이미지 표시
        for img_name in ["champion_play.png", "win_rate.png", "kda_graph.png", "game_time.png"]:
            img_label = QLabel()
            image = QImage(img_name)
            pixmap = QPixmap.fromImage(image)
            img_label.setPixmap(pixmap.scaled(400, 300))
            layout.addWidget(img_label)

        self.setLayout(layout)

# 🔹 실행 코드
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LolDataApp()
    ex.show()
    sys.exit(app.exec_())
