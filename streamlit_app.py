import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Real Profit Sniper 💰", layout="wide")

st.title("💰 رادار المكسب الحقيقي (إصدار القناص)")
st.write("الهدف: تحويل الـ 100 جنيه لأرباح حقيقية من خلال قنص السيولة")

def get_data():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    data = get_data()
    if data:
        # العملات الأكثر ربحية للرأس المال الصغير
        targets = ['PEPEUSDT', 'SHIBUSDT', 'FLOKIUSDT', 'BONKUSDT', 'LUNCUSDT', 'XRPUSDT', 'SOLUSDT']
        rows = []
        
        for item in data:
            if item['symbol'] in targets:
                price = float(item['lastPrice'])
                vol = float(item['quoteVolume'])
                change = float(item['priceChangePercent'])
                
                # معادلة المكسب الحقيقي
                if change > 1 and vol > 5000000:
                    signal = "🔥 اشتري الآن (فرصة مكسب)"
                elif change < -2:
                    signal = "⚠️ خطر (هروب السيولة)"
                else:
                    signal = "⏳ انتظر إشارة"

                rows.append({
                    "العملة": item['symbol'].replace("USDT", ""),
                    "السعر الحالي": f"${price:.8f}",
                    "حركة 24س": f"{change}%",
                    "السيولة ($)": f"{vol:,.0f}",
                    "الإشارة": signal
                })

        with placeholder.container():
            # عرض أقوى فرصة في كارت كبير
            best_opportunity = max(rows, key=lambda x: float(x['حركة 24س'].replace('%','')))
            
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"""
                <div style="background-color:#1b4d3e; padding:20px; border-radius:15px; text-align:center">
                    <h2 style="color:white">أقوى فرصة للمكسب الآن: {best_opportunity['العملة']}</h2>
                    <h1 style="color:#00ff00">{best_opportunity['الإشارة']}</h1>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                st.metric("تحديث الرادار", time.strftime('%H:%M:%S'))
                st.write("نصيحة: لا تدخل الصفقة إلا لو الإشارة 'اشتري الآن' والسيولة فوق 5 مليون.")

            st.write("---")
            df = pd.DataFrame(rows)
            st.table(df)

    time.sleep(5)
