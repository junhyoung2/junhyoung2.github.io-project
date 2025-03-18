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
BUY_THRESHOLD_PERCENT = 5  # 매수 기준: 가격이 현재가 대비 5% 하락시 매수
SELL_THRESHOLD_PERCENT = 5  # 매도 기준: 가격이 매수가 대비 5% 상승시 매도

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
    loop = asyncio.new_event_loop()  # 새 이벤트 루프 생성
    asyncio.set_event_loop(loop)  # 생성한 루프를 현재 스레드의 루프에 설정
    
    while True:
        try:
            # 거래량 상위 30개 종목 가져오기
            top_30_markets = loop.run_until_complete(get_top_30_markets())
            print(f"거래량 상위 30개 종목: {top_30_markets}")
            
            for market in top_30_markets:
                # 현재 가격을 가져오는 코드 수정
                ticker = "KRW-" + market
                current_price = pyupbit.get_current_price(ticker)  # 현재 가격 추출
                balance = upbit.get_balance("KRW")
                
                if current_price is None:
                    continue

                # 매수 기준: 현재 가격이 매수 기준 대비 n% 하락한 경우
                buy_price = current_price * (1 - (BUY_THRESHOLD_PERCENT / 100))
                if balance >= TRADE_AMOUNT and current_price <= buy_price:
                    # 매수 예시: 매수 조건 설정 (예: 시장가 매수)
                    upbit.buy_market_order(ticker, TRADE_AMOUNT / len(top_30_markets))
                    print(f"{market} 매수 주문 실행")

                # 매도 기준: 구매 가격에서 n% 상승한 경우
                sell_price = current_price * (1 + (SELL_THRESHOLD_PERCENT / 100))
                current_position = upbit.get_balance(ticker)
                if current_position > 0 and current_price >= sell_price:
                    # 매도 예시: 매도 조건 설정 (예: 시장가 매도)
                    upbit.sell_market_order(ticker, current_position)
                    print(f"{market} 매도 주문 실행")

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
