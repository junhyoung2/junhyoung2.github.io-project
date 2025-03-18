import os
import sys
import pyupbit
import pandas as pd
import asyncio
import aiohttp
import threading
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

# 🔹 업비트 API 키 설정 (직접 할당)
ACCESS_KEY = "nBD2XzRCOkUspRTFuMTeMdxM6xKNXWv4dqJUd75W"
SECRET_KEY = "SLxfdPTb9nZ67LvGm0BI9Wmmq8fY7IxS1FSLNyQ3"

print(f"ACCESS_KEY: {ACCESS_KEY}")
print(f"SECRET_KEY: {SECRET_KEY}")

# 🔹 자동 매매 전략 및 기본 설정
TRADE_INTERVAL = 60  # 자동매매 주기 (초 단위)
TRADE_AMOUNT = 10000  # 매매 금액 (원)
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
    market_ids = [market['market'] for market in markets if market['market'].startswith('KRW')]
    market_data = []
    for market_id in market_ids:
        ticker = market_id.replace("KRW-", "")
        df = pyupbit.get_ohlcv(market_id, interval="day", count=1)
        volume = 0 if df is None or df.empty else df.iloc[0]['volume']
        market_data.append((ticker, volume))
    return [market[0] for market in sorted(market_data, key=lambda x: x[1], reverse=True)[:30]]

# 🔹 자동 매매 시작 함수
async def start_auto_trade():
    while True:
        try:
            top_30_markets = await get_top_30_markets()
            for market in top_30_markets:
                ticker = "KRW-" + market
                current_price = pyupbit.get_current_price(ticker)
                try:
                    balance = upbit.get_balance("KRW")
                    if balance is None:
                        raise ValueError("Balance is None")
                except Exception as e:
                    print(f"Error retrieving balance: {e}")
                    balance = 0
                
                if current_price is None:
                    print(f"Skipping {ticker} due to None value. current_price: {current_price}, balance: {balance}")
                    continue
                buy_price = current_price * (1 - (BUY_THRESHOLD_PERCENT / 100))
                if balance >= TRADE_AMOUNT and current_price <= buy_price:
                    upbit.buy_market_order(ticker, TRADE_AMOUNT / len(top_30_markets))
                sell_price = current_price * (1 + (SELL_THRESHOLD_PERCENT / 100))
                current_position = upbit.get_balance(ticker)
                if current_position > 0 and current_price >= sell_price:
                    upbit.sell_market_order(ticker, current_position)
            await asyncio.sleep(TRADE_INTERVAL)
        except Exception as e:
            print(f"자동매매 오류 발생: {e}")
            await asyncio.sleep(TRADE_INTERVAL)

# 🔹 GUI 클래스 정의
class CryptoTradeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("비트코인 자동매매")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        self.start_button = QPushButton("자동 매매 시작")
        self.start_button.clicked.connect(self.start_auto_trade)
        layout.addWidget(self.start_button)
        self.stop_button = QPushButton("자동 매매 중지")
        self.stop_button.clicked.connect(self.stop_auto_trade)
        layout.addWidget(self.stop_button)
        self.status_label = QLabel("거래량 상위 30개 종목: (GUI에는 표시하지 않음)")
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def start_auto_trade(self):
        self.status_label.setText("대기 중...")
        self.auto_trade_thread = threading.Thread(target=self.run_async_auto_trade)
        self.auto_trade_thread.start()

    def run_async_auto_trade(self):
        asyncio.run(start_auto_trade())

    def stop_auto_trade(self):
        self.status_label.setText("자동 매매 중지됨.")
        # 중지 로직 추가 필요

# 🔹 실행 코드
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CryptoTradeApp()
    ex.show()
    sys.exit(app.exec_())
