import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Liquidity Hunter Pro", layout="wide")

# مخزن لحفظ السيولة السابقة للمقارنة
if 'prev_vol' not in st.session_state:
    st.session_state.prev_vol = {}

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>""", height=0)

st.title("🌊 رادار تدفق السيولة (صيد الحيتان قبل الانطلاق)")
st.write("الرادار يراقب الآن: كم دولاراً دخل في كل عملة خلال الـ 60 ثانية الماضية؟")

def fetch_data():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    data = fetch_data()
    if data:
        targets = ['PEPEUSDT', 'SHIBUSDT', 'BONKUSDT', 'FLOKIUSDT', 'LUNCUSDT', '1000SATSUSDT', 'RATSUSDT', 'XRPUSDT', 'SOLUSDT']
        results = []
        
        for item in data:
            symbol = item['symbol']
            if symbol in targets:
                price = float(item['lastPrice'])
                current_vol = float(item['quoteVolume'])
                
                # حساب "السيولة الجديدة" (اللي دخلت في آخر 10 ثواني)
                prev_v = st.session_state.prev_vol.get(symbol, current_vol)
                new_money = current_vol - prev_v
                st.session_state.prev_vol[symbol] = current_vol
                
                # تقييم الفرصة بناءً على "دخول المال"
                if new_money > 5000: # لو دخل أكتر من 5000 دولار في ثواني
                    status = "🚨 دخول سيولة فوري!"
                    color = "#ff4b4b"
                    play_alert()
                elif new_money > 1000:
                    status = "💰 تجميع هادئ"
                    color = "#00ff00"
                else:
                    status = "💤 سكون"
                    color = "white"

                results.append({
                    "العملة": symbol.replace("USDT", ""),
                    "السعر": f"${price:.8f}",
                    "فلوس دخلت الآن": f"${new_money:,.2f}",
                    "حالة السيولة": status
                })

        with placeholder.container():
            # ترتيب حسب السيولة الجديدة
            df = pd.DataFrame(results).sort_values(by="فلوس دخلت الآن", ascending=False)
            
            # عرض كروت العملات اللي بيدخل فيها فلوس "حالا"
            hot_coins = df[df['فلوس دخلت الآن'].str.replace('$', '').str.replace(',', '').astype(float) > 1000]
            
            if not hot_coins.empty:
                cols = st.columns(len(hot_coins[:3]))
                for i, row in enumerate(hot_coins.iloc[:3].to_dict('records')):
                    cols[i].success(f"🔥 {row['العملة']} دخل فيها {row['فلوس دخلت الآن']}")

            st.write("---")
            st.table(df.drop(columns=[]))
            st.caption(f"مراقبة النبض اللحظي للسوق - تحديث كل 10 ثواني")

    time.sleep(10)
