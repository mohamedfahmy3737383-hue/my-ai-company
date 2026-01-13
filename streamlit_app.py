import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Global Control Lite", layout="wide")

# محرك البحث عن البيانات (نسخة خفيفة ومستقرة)
def fetch_fast():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        res = requests.get(url, timeout=5)
        return res.json() if res.status_code == 200 else None
    except: return None

st.title("🌎 رادار السيطرة (النسخة المستقرة)")

# الذاكرة البسيطة
if 'prev' not in st.session_state: st.session_state.prev = {}

placeholder = st.empty()

while True:
    data = fetch_fast()
    if data:
        targets = ['BTCUSDT', 'SOLUSDT', 'PEPEUSDT', 'SHIBUSDT', 'BONKUSDT', 'FLOKIUSDT', '1000SATSUSDT', 'LUNCUSDT']
        results = []
        
        for item in data:
            if item.get('symbol') in targets:
                sym = item['symbol'].replace("USDT", "")
                price = float(item['lastPrice'])
                change = float(item['priceChangePercent'])
                vol = float(item['quoteVolume'])
                
                # حساب التدفق
                old_v = st.session_state.prev.get(sym, vol)
                flow = vol - old_v
                st.session_state.prev[sym] = vol
                
                results.append({
                    "العملة": sym,
                    "السعر": f"${price:.8f}" if price < 1 else f"${price:,.2f}",
                    "التغير": f"{change}%",
                    "تدفق حيتان ($)": f"{flow:,.0f}",
                    "الحالة": "🚀 هجوم" if change > 2 or flow > 10000 else "📡 رصد"
                })
        
        with placeholder.container():
            df = pd.DataFrame(results).sort_values(by="تغير", ascending=False)
            st.dataframe(df, use_container_width=True) # استخدام dataframe أخف من table
            st.caption(f"تحديث مستقر: {time.strftime('%H:%M:%S')}")
            
    time.sleep(10) # زودنا الوقت لـ 10 ثواني عشان السيرفر ميهنجش
