import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Ultimate Global Control", layout="wide")

# ذاكرة الشركة
if 'prev_v' not in st.session_state: st.session_state.prev_v = {}
if 'last_signals' not in st.session_state: st.session_state.last_signals = {}

st.title("🌐 رادار السيطرة العالمية (إصدار تخطي الحواجز)")

# إدارة المحفظة
st.sidebar.title("💰 شركة الـ 100 جنيه")
buy_p = st.sidebar.number_input("سعر شراء عملتك ($):", value=0.000001, format="%.8f")

def get_data_from_anywhere():
    # محاولة الطريق الأول: Binance
    try:
        r = requests.get("https://api1.binance.com/api/v3/ticker/24hr", timeout=3)
        if r.status_code == 200: return ("B", r.json())
    except: pass
    
    # محاولة الطريق الثاني: CoinCap (احتياطي)
    try:
        r = requests.get("https://api.coincap.io/v2/assets?limit=20", timeout=3)
        if r.status_code == 200: return ("C", r.json().get('data', []))
    except: pass
    
    return None

placeholder = st.empty()

while True:
    source_data = get_data_from_anywhere()
    
    if source_data:
        source, raw = source_data
        results = []
        current_time = time.time()
        
        # معالجة البيانات بناءً على المصدر اللي فتح معانا
        if source == "B": # لو Binance هي اللي اشتغلت
            targets = ['BTCUSDT', 'SOLUSDT', 'PEPEUSDT', 'SHIBUSDT', 'BONKUSDT', 'FLOKIUSDT', '1000SATSUSDT']
            for item in raw:
                if item.get('symbol') in targets:
                    sym = item['symbol'].replace("USDT","")
                    p, c, v = float(item['lastPrice']), float(item['priceChangePercent']), float(item['quoteVolume'])
                    results.append({"العملة": sym, "السعر": p, "تغير%": c, "سيولة": v})
        
        elif source == "C": # لو CoinCap هي اللي اشتغلت
            targets = ['bitcoin', 'solana', 'pepe', 'shiba-inu', 'bonk', 'dogecoin']
            for item in raw:
                if item.get('id') in targets:
                    results.append({
                        "العملة": item['symbol'],
                        "السعر": float(item['priceUsd']),
                        "تغير%": float(item['changePercent24Hr']),
                        "سيولة": float(item['volumeUsd24Hr'])
                    })

        if results:
            with placeholder.container():
                # حساب الـ 100 جنيه
                ref = results[0] # أول عملة في القائمة
                val_egp = ((2.0 / buy_p) * ref['السعر']) * 50 if buy_p > 0 else 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric("قيمة الـ 100 ج", f"{val_
