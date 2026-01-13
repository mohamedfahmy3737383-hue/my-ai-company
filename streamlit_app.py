import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Big Vision Radar 🚀", layout="wide")

# كود الصوت
def play_sound():
    sound_html = """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>"""
    st.components.v1.html(sound_html, height=0)

st.title("📈 شركة القنص الذكي - رادار العملات الواعدة")
st.write("رأس المال المستهدف: 100 جنيه مصري (حوالي $2.00)")

def get_mexc_data():
    url = "https://api.mexc.com/api/v3/ticker/bookTicker"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    raw_data = get_data = get_mexc_data()
    if raw_data:
        # إضافة عملات رخيصة جداً وحركتها سريعة
        targets = [
            'BTCUSDT', 'ETHUSDT', 'SOLUSDT', # الكبار
            'PEPEUSDT', 'SHIBUSDT', 'FLOKIUSDT', 'BONKUSDT', 'LUNCUSDT', # عملات رخيصة (تراب فلوس)
            'GALAUSDT', 'VETUSDT', 'CHZUSDT' # عملات مشاريع قوية ورخيصة
        ]
        
        final_list = []
        for item in raw_data:
            if item['symbol'] in targets:
                bid = float(item['bidPrice'])
                ask = float(item['askPrice'])
                spread = ((ask - bid) / bid) * 100
                net = spread - 0.2
                
                # حساب الكمية اللي تشتريها بـ 100 جنيه (بافتراض الدولار بـ 50 جنيه)
                capital_usd = 2.0 
                quantity = capital_usd / ask if ask > 0 else 0
                
                final_list.append({
                    "العملة": item['symbol'].replace("USDT", ""),
                    "السعر": f"${ask:.8f}", # عرض 8 أرقام بعد العلامة عشان العملات الرخيصة
                    "صافي الربح %": round(net, 3),
                    "كمية بـ 100 ج": f"{quantity:,.0f} قطعة",
                    "الحالة": "💎 صيد ثمين" if net > 0.01 else "⏳ مراقبة"
                })

        with placeholder.container():
            df = pd.DataFrame(final_list)
            
            # كروت الشركة
            c1, c2, c3 = st.columns(3)
            c1.metric("عدد العملات تحت المراقبة", len(final_list))
            c2.metric("قوة السوق", "متذبذب (ممتاز للمراجحة)" if any(df['صافي الربح %'] > 0) else "هادئ")
            c3.metric("رأس المال", "100 EGP")

            st.write("### 🔍 رادار العملات الرخيصة والفرص")
            
            def color_strategy(val):
                if "💎" in val: return 'background-color: #004d40; color: white'
                return ''

            st.table(df.style.applymap(color_strategy, subset=['الحالة']))
            
            if any("💎" in x for x in df['الحالة']):
                play_sound()

    time.sleep(5)
