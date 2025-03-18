import sys
import pyupbit
import pandas as pd
import matplotlib.pyplot as plt
import asyncio
import aiohttp
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QImage
import threading
import time

# 🔹 업비트 API 키 설정 (사용자 본인의 API 키 입력)
ACCESS_KEY = "nBD2XzRCOkUspRTFuMTeMdxM6xKNXWv4dqJUd75W"  # 발급받은 Access Key 입력
SECRET_KEY = "SLxfdPTb9nZ67LvGm0BI9Wmmq8fY7IxS1FSLNyQ3"  # 발급받은 Secret Key 입력

# 🔹 자동 매매 전략 및 기본 설정
TRADE_INTERVAL = 60  # 자동매매 주기 (초 단위)
TRADE_AMOUNT = 10000  # 매매 금액 (원)
MAX_TRADE_COUNT = 10  # 최대 매매 횟수
TARGET_VOLUME_RANK = 30  # 거래량 상위 종목 기준

# 🔹 거래량 상위 30개 종목 비동기 함수
async def fetch_market_data(session, market_code):
    url = f"https://api.upbit.com/v1/ticker?markets={market_code}"
    async with session.get(url) as response:
        data = await response.json()
        return market_code, data[0]['acc_trade_volume_24h'] if data else None

async def get_top_30_markets():
    markets = pyupbit.get_markets()  # 업비트의 마켓 정보 가져오기
    market_codes = [market['market'] for market in markets if 'BTC' in market['market']]  # BTC 거래소들만 필터링
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_market_data(session, code) for code in market_codes]
        volumes = await asyncio.gather(*tasks)

    # 거래량 기준으로 상위 30개 종목 정렬
    sorted_volumes = sorted(volumes, key=lambda x: x[1] if x[1] else 0, reverse=True)[:TARGET_VOLUME_RANK]
    
    # 거래량 상위 30개 종목 반환
    return [market[0] for market in sorted_volumes if market[1] is not None]

# 🔹 자동 매매 전략
def auto_trade():
    target_markets = asyncio.run(get_top_30_markets())  # 거래량 상위 30개 종목 리스트 가져오기
    print("자동 매매 시작. 거래량 상위 30개 종목:", target_markets)

    for market in target_markets:
        # 1. 현재 가격 가져오기
        price = pyupbit.get_current_price(market)
        if price is None:
            print(f"오류: {market} 가격을 불러올 수 없습니다.")
            continue

        # 2. 매수/매도 전략: 예시로 현재 가격보다 낮은 가격에 매수, 높은 가격에 매도 (단순 전략)
        balance = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY).get_balance(market)  # 종목별 잔고 확인
        if balance <= 0:
            print(f"{market}에 잔고가 없습니다. 매수 시작.")
            # 예시: 현재 가격의 1% 낮은 가격에 매수
            buy_price = price * 0.99
            pyupbit.Upbit(ACCESS_KEY, SECRET_KEY).buy_market_order(market, TRADE_AMOUNT)
            print(f"{market} 매수 주문 완료. 매수 가격: {buy_price}")
        else:
            print(f"{market}에 잔고가 있습니다. 매도 시작.")
            # 예시: 현재 가격보다 1% 높은 가격에 매도
            sell_price = price * 1.01
            pyupbit.Upbit(ACCESS_KEY, SECRET_KEY).sell_market_order(market, balance)
            print(f"{market} 매도 주문 완료. 매도 가격: {sell_price}")
        time.sleep(TRADE_INTERVAL)  # 매매 간의 대기 시간

# 🔹 GUI 클래스 정의
class TradingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("비트코인 자동매매")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        # 🔹 매매 시작 버튼
        self.start_button = QPushButton("자동 매매 시작")
        self.start_button.clicked.connect(self.start_auto_trade)
        layout.addWidget(self.start_button)

        # 🔹 매매 중지 버튼
        self.stop_button = QPushButton("자동 매매 중지")
        self.stop_button.clicked.connect(self.stop_auto_trade)
        layout.addWidget(self.stop_button)

        # 🔹 거래량 상위 30개 종목 출력
        self.top_markets_label = QLabel("거래량 상위 30개 종목:")
        layout.addWidget(self.top_markets_label)

        self.top_markets_list = QLabel("대기 중...")
        layout.addWidget(self.top_markets_list)

        self.setLayout(layout)

    def start_auto_trade(self):
        # 자동 매매 시작
        self.trade_thread = threading.Thread(target=self.auto_trade_with_gui, daemon=True)
        self.trade_thread.start()

    def auto_trade_with_gui(self):
        # 자동매매 실행 및 거래량 상위 30개 종목 업데이트
        target_markets = asyncio.run(get_top_30_markets())  # 거래량 상위 30개 종목 리스트 가져오기
        target_markets_str = '\n'.join(target_markets)  # 종목 목록 문자열로 변환
        
        # GUI 업데이트: 거래량 상위 30개 종목 표시
        self.top_markets_list.setText(target_markets_str)

        # 자동 매매 실행
        auto_trade()

    def stop_auto_trade(self):
        # 자동 매매 중지
        print("자동 매매를 중지합니다.")
        # 중지 구현 (현재는 실제 중지 기능을 구현하지 않음)

# 🔹 실행 코드
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TradingApp()
    ex.show()
    sys.exit(app.exec_())
