import streamlit as st
import pandas as pd
import requests
import time
import hmac
import hashlib

# إعدادات الصفحة
st.set_page_config(page_title="MEXC AI Hunter", layout="wide")

# جلب المفاتيح من الـ Secrets بأمان
try:
    access_key = st.secrets["MEXC_ACCESS_KEY"]
    secret_key = st.secrets["MEXC_SECRET_KEY"]
except:
    st.error("⚠️ خطأ: المفاتيح غير موجودة في Secrets!")
    st.stop()

def get_mexc_ticker():
    # جلب أسعار المنصة اللحظية (عمومي)
    url = "https://api.mexc.com/api/v3/ticker/bookTicker"
    return requests.get(url).json()

st.title("🏹 رادار قنص MEXC المطور")
st.markdown("---")

placeholder = st.empty()

while True:
    tickers = get_mexc_ticker()
    
    if tickers:
        data = []
        # أهم عملات بنراقبها
        targets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'LTCUSDT']
        
        for t in tickers:
            if t['symbol'] in targets:
                bid = float(t['bidPrice'])
                ask = float(t['askPrice'])
                # حساب الفارق الربحي (Spread)
                spread = ((ask - bid) / bid) * 100
                
                data.append({
                    "العملة": t['symbol'],
                    "أفضل شراء (Bid)": f"${bid:,.4f}",
                    "أفضل بيع (Ask)": f"${ask:,.4f}",
                    "الفارق الربحي %": round(spread, 4),
                    "صافي الربح (بعد العمولة)": f"{round(spread - 0.2, 4)}%"
                })
        
        with placeholder.container():
            # عرض كروت إحصائية
            c1, c2, c3 = st.columns(3)
            c1.metric("حالة الـ API", "✅ متصل")
            c2.metric("تحديث", time.strftime('%H:%M:%S'))
            c3.metric("المنصة", "MEXC Global")
            
            # عرض الجدول
            df = pd.DataFrame(data)
            st.dataframe(df.style.highlight_max(axis=0, subset=['الفارق الربحي %'], color='#1b4d3e'), use_container_width=True)
            
            # تنبيه لو فيه فرصة قوية
            if any(float(row['الفارق الربحي %']) > 0.05 for row in data):
                st.success("🔥 اكتشاف فجوة سعرية! راقب الجدول")
    
    time.sleep(3) # تحديث سريع جداً كل 3 ثواني
