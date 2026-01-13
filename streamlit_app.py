import streamlit as st
import pandas as pd
import requests
import time

# 1. إعدادات الصفحة والجماليات
st.set_page_config(page_title="AI Mega Radar 🚀", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { border: 1px solid #4b5563; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. المحفظة الشخصية (الـ 100 جنيه)
st.sidebar.title("💰 محفظة الـ 100 جنيه")
buy_price = st.sidebar.number_input("سعر شراء عملتك (بالدولار):", value=0.000001, format="%.8f")
target_profit = st.sidebar.slider("هدفك الربحي (بالجنيه):", 1, 100, 20)

st.title("🎯 رادار القنص الموحد - نسخة الاستعادة")
st.write("تم استعادة نظام مراقبة الحيتان وإدارة الـ 100 جنيه")

def get_data():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    data = get_data()
    if data:
        targets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'PEPEUSDT', 'SHIBUSDT', 'FLOKIUSDT', 'BONKUSDT']
        rows = []
        my_coin_price = 0
        
        for item in data:
            symbol = item['symbol'].replace("USDT", "")
            if item['symbol'] in targets:
                price = float(item['lastPrice'])
                vol = float(item['quoteVolume'])
                change = float(item['priceChangePercent'])
                
                if symbol == "PEPE": my_coin_price = price
                
                rows.append({
                    "العملة": symbol,
                    "السعر": f"${price:.8f}",
                    "الحجم": f"${vol:,.0f}",
                    "قوة الحيتان": "🐳 ضخمة" if vol > 10000000 else "🐟 أفراد",
                    "التوقع": "🚀 صعود" if change > 2 else "➡️ استقرار"
                })

        with placeholder.container():
            # حسابات الـ 100 جنيه
            val_egp = ((2.0 / buy_price) * my_coin_price) * 50 if buy_price > 0 else 100
            diff = val_egp - 100
            
            # عرض النتائج
            c1, c2, c3 = st.columns(3)
            c1.metric("قيمة الـ 100 ج الآن", f"{val_egp:.2f} ج.م", f"{diff:.2f}")
            c2.metric("أعلى حجم تداول", rows[0]['العملة'])
            c3.metric("الساعة الآن", time.strftime('%H:%M:%S'))
            
            st.progress(min(max(diff/target_profit, 0.0), 1.0) if diff > 0 else 0.0)
            
            st.write("### 📊 رادار السوق الشامل")
            st.table(pd.DataFrame(rows))
            
    time.sleep(5)
