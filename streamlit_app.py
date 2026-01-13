import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Mega Opp Hunter 🚀", layout="wide")

# مخزن البيانات للحفاظ على سجل الفرص
if 'opportunity_history' not in st.session_state:
    st.session_state.opportunity_history = []

def play_ping():
    # صوت تنبيه قصير وذكي
    st.components.v1.html("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>""", height=0)

st.title("🚀 مركز عمليات القنص (نسخة استغلال الفرص)")
st.write("الهدف: تحويل الـ 100 جنيه لأرباح متراكمة عن طريق ملاحقة الانفجارات السعرية")

def fetch_data():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    data = fetch_data()
    if data:
        # العملات اللي بتعمل "انفجارات" حالياً
        targets = ['PEPEUSDT', 'SHIBUSDT', 'FLOKIUSDT', 'BONKUSDT', 'LUNCUSDT', '1000SATSUSDT', 'BOMEUSDT', 'MEMEUSDT']
        current_opportunities = []
        
        for item in data:
            if item['symbol'] in targets:
                symbol = item['symbol'].replace("USDT", "")
                price = float(item['lastPrice'])
                change = float(item['priceChangePercent'])
                vol = float(item['quoteVolume'])
                
                # حساب "درجة القوة" (معادلة خاصة بالشركة)
                # بتجمع بين التغير السعري والسيولة
                power_score = (change * 10) + (vol / 1000000)
                
                status = "⚪ هدوء"
                if power_score > 50:
                    status = "🔥 انفجار سعري!"
                    if symbol not in [x['العملة'] for x in st.session_state.opportunity_history[-5:]]:
                        play_ping()
                        st.session_state.opportunity_history.append({"العملة": symbol, "الوقت": time.strftime('%H:%M:%S'), "القوة": round(power_score, 1)})
                elif power_score > 20:
                    status = "💹 بداية حركة"

                current_opportunities.append({
                    "العملة": symbol,
                    "السعر": f"${price:.8f}",
                    "التغير %": f"{change}%",
                    "قوة الفرصة": round(power_score, 1),
                    "القرار": status
                })

        with placeholder.container():
            # الجزء العلوي: سجل آخر 3 فرص تم رصدهم
            if st.session_state.opportunity_history:
                st.subheader("📝 سجل القنص (آخر الفرص)")
                cols = st.columns(3)
                recent = st.session_state.opportunity_history[-3:][::-1]
                for i, op in enumerate(recent):
                    with cols[i]:
                        st.info(f"📍 {op['العملة']} | قوة: {op['القوة']} | الساعة: {op['الوقت']}")

            st.write("---")
            # الجدول الرئيسي
            df = pd.DataFrame(current_opportunities)
            
            def color_decision(val):
                if "🔥" in val: return 'background-color: #7a0000; color: white'
                if "💹" in val: return 'background-color: #004d40; color: white'
                return ''

            st.subheader("📊 رادار الفرص اللحظي")
            st.table(df.style.applymap(color_decision, subset=['القرار']))

    time.sleep(4)
