import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Sniper Pro V3", layout="wide")

st.title("🏹 رادار القنص السريع (صيد السنتات)")
st.write("الهدف: تحويل الـ 100 جنيه لأرباح تراكمية سريعة")

def get_data():
    # استخدام API مختلف يعطي بيانات أكثر دقة للحركة اللحظية
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

# تخزين السعر القديم للمقارنة وحساب الانفجار اللحظي
if 'old_prices' not in st.session_state:
    st.session_state.old_prices = {}

while True:
    data = get_data()
    if data:
        # قائمة أوسع من العملات الرخيصة والمجنونة
        targets = ['PEPEUSDT', 'SHIBUSDT', 'FLOKIUSDT', 'BONKUSDT', 'LUNCUSDT', 'XECUSDT', 'BTTCUSDT', 'GASUSDT', 'ORDIUSDT']
        rows = []
        
        for item in data:
            symbol = item['symbol']
            if symbol in targets:
                price = float(item['lastPrice'])
                vol = float(item['quoteVolume'])
                change_24h = float(item['priceChangePercent'])
                
                # حساب الحركة "اللحظية" (Scalping Detection)
                old_price = st.session_state.old_prices.get(symbol, price)
                instant_move = ((price - old_price) / old_price) * 100 if old_price > 0 else 0
                st.session_state.old_prices[symbol] = price
                
                # إشارة الدخول (شروط أسهل للمكسب السريع)
                if instant_move > 0.02 or (change_24h > 2 and vol > 1000000):
                    signal = "✅ دخول سريع (سكالبينج)"
                    color = "#00ff00"
                elif instant_move < -0.02:
                    signal = "🔻 هبوط لحظي"
                    color = "#ff4b4b"
                else:
                    signal = "⌛ انتظار"
                    color = "#ffffff"

                rows.append({
                    "العملة": symbol.replace("USDT", ""),
                    "السعر": f"${price:.8f}",
                    "السيولة": f"${vol:,.0f}",
                    "حركة لحظية": f"{instant_move:+.4f}%",
                    "الإشارة": signal,
                    "color": color
                })

        with placeholder.container():
            # عرض "الفرصة الذهبية"
            st.subheader(f"📡 حالة الرادار: {time.strftime('%H:%M:%S')}")
            
            # تصميم كروت احترافية
            cols = st.columns(len(rows[:4])) # عرض أول 4 عملات ككروت
            for i, row in enumerate(rows[:4]):
                with cols[i]:
                    st.markdown(f"""
                    <div style="background-color:#1e1e1e; padding:10px; border-radius:10px; border-left: 5px solid {row['color']}">
                        <h4 style="margin:0">{row['العملة']}</h4>
                        <p style="color:{row['color']}; font-weight:bold; margin:0">{row['الإشارة']}</p>
                        <p style="font-size:12px; margin:0">حركة: {row['حركة لحظية']}</p>
                    </div>
                    """, unsafe_allow_html=True)

            st.write("---")
            # الجدول الكامل
            df = pd.DataFrame(rows).drop(columns=['color'])
            st.table(df)

    time.sleep(3) # تحديث كل 3 ثواني لقنص الحركة
