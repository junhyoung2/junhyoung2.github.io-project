import sys
import pyupbit
import pandas as pd
import asyncio
import aiohttp
import threading
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

# 🔹 업비트 API 키 설정 (사용자 본인의 API 키 입력)
ACCESS_KEY = "nBD2XzRCOkUspRTFuMTeMdxM6xKNXWv4dqJUd75W"  # 발급받은 Access Key 입력
SECRET_KEY = "SLxfdPTb9nZ67LvGm0BI9Wmmq8fY7IxS1FSLNyQ3"  # 발급받은 Secret Key 입력

# 🔹 자동 매매 전략 및 기본 설정
TRADE_INTERVAL = 60  # 자동매매 주기 (초 단위)
TRADE_AMOUNT = 10000  # 매매 금액 (원)
MAX_TRADE_COUNT = 10  # 최대 매매 횟수

# 🔹 Upbit API 초기화
upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)

# 🔹 거래량 상위 30개 종목 추출 함수
async def get_top_30_markets():
    url = "https://api.upbit.com/v1/market/all"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            markets = await response.json()
    # 거래량 상위 30개 종목 필터링
    market_ids = [market['market'] for market in markets if market['market'].startswith('KRW')]
    market_data = []
    for market_id in market_ids:
        ticker = market_id.replace("KRW-", "")
        df = pyupbit.get_ohlcv(market_id, interval="day", count=1)
        
        # 데이터가 없을 경우 0 처리
        if df is None or df.empty:
            volume = 0
        else:
            volume = df.iloc[0]['volume']  # 첫 번째 데이터의 거래량 사용
        
        market_data.append((ticker, volume))
    
    # 거래량을 기준으로 상위 30개 종목 필터링
    top_30_markets = sorted(market_data, key=lambda x: x[1], reverse=True)[:30]
    return [market[0] for market in top_30_markets]

# 🔹 자동 매매 시작 함수
def start_auto_trade():
    while True:
        try:
            # 거래량 상위 30개 종목 가져오기
            top_30_markets = asyncio.run(get_top_30_markets())
            print(f"거래량 상위 30개 종목: {top_30_markets}")
            
            for market in top_30_markets:
                # 각 종목에 대해 매수/매도 전략 실행
                balance = upbit.get_balance("KRW")
                if balance >= TRADE_AMOUNT:
                    # 매수 예시: 매수 조건 설정 (예: 시장가 매수)
                    upbit.buy_market_order("KRW-" + market, TRADE_AMOUNT / len(top_30_markets))
                    print(f"{market} 매수 주문 실행")
                else:
                    print(f"{market} 잔액 부족으로 매수 불가")

            time.sleep(TRADE_INTERVAL)  # 자동매매 주기마다 대기
        except Exception as e:
            print(f"자동매매 오류 발생: {e}")
            time.sleep(TRADE_INTERVAL)

# 🔹 GUI 클래스 정의
class CryptoTradeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("비트코인 자동매매")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # 🔹 자동매매 시작/중지 버튼
        self.start_button = QPushButton("자동 매매 시작")
        self.start_button.clicked.connect(self.start_auto_trade)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("자동 매매 중지")
        self.stop_button.clicked.connect(self.stop_auto_trade)
        layout.addWidget(self.stop_button)

        # 🔹 상태 라벨
        self.status_label = QLabel("거래량 상위 30개 종목: (GUI에는 표시하지 않음)")
        layout.addWidget(self.status_label)

        # 🔹 GUI 설정
        self.setLayout(layout)

    # 🔹 자동 매매 시작 버튼 클릭 시 처리 함수
    def start_auto_trade(self):
        self.status_label.setText("대기 중...")
        self.auto_trade_thread = threading.Thread(target=start_auto_trade)
        self.auto_trade_thread.start()

    # 🔹 자동 매매 중지 버튼 클릭 시 처리 함수
    def stop_auto_trade(self):
        self.status_label.setText("자동 매매 중지됨.")
        # 중지 로직을 추가하고 싶으면 여기에서 처리

# 🔹 실행 코드
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CryptoTradeApp()
    ex.show()
    sys.exit(app.exec_())
