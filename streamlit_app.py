import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Max Opportunity Hunter", layout="wide")

# مخزن ذكي للشركة
if 'last_action' not in st.session_state:
    st.session_state.last_action = "انتظار"

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>""", height=0)

st.title("🏹 مركز قنص الأرباح - شركة الـ 100 جنيه")

def fetch_market():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    data = fetch_market()
    if data:
        # العملات الرخيصة (بتاعة الـ 100 جنيه)
        targets = ['PEPEUSDT', 'SHIBUSDT', 'FLOKIUSDT', 'BONKUSDT', 'LUNCUSDT', 'BOMEUSDT']
        results = []
        
        for item in data:
            if item['symbol'] in targets:
                symbol = item['symbol'].replace("USDT", "")
                price = float(item['lastPrice'])
                change = float(item['priceChangePercent'])
                vol = float(item['quoteVolume'])
                
                # حساب قوة الفرصة (كل ما الرقم زاد، كل ما كان المكسب أقرب)
                score = (change * 5) + (vol / 2000000)
                
                # تحديد "أمر العمل"
                if score > 40:
                    action = "🚀 هجوم (شراء فوري)"
                    color = "red" # لون ينبهك
                elif score > 15:
                    action = "🎯 تجهيز (راقب السعر)"
                    color = "green"
                elif change < -3:
                    action = "⚠️ هروب (بيع لو معاك)"
                    color = "orange"
                else:
                    action = "⏳ سكون"
                    color = "white"

                results.append({
                    "العملة": symbol,
                    "السعر": f"${price:.8f}",
                    "حركة 24س": f"{change}%",
                    "قوة الفرصة": round(score, 2),
                    "أمر الشركة": action
                })

        with placeholder.container():
            # كارت "أقوى فرصة الآن"
            top_opportunity = max(results, key=lambda x: x['قوة الفرصة'])
            
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"""
                <div style="background-color:#1e1e1e; padding:25px; border-radius:15px; border: 2px solid gold; text-align:center">
                    <h2 style="color:white; margin:0">أفضل صيد للـ 100 جنيه الآن: {top_opportunity['العملة']}</h2>
                    <h1 style="color:gold; font-size:50px; margin:10px">{top_opportunity['قوة الفرصة']}</h1>
                    <h3 style="color:#00ff00">{top_opportunity['أمر الشركة']}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                st.metric("حالة السوق", "فرص مشتعلة" if top_opportunity['قوة الفرصة'] > 30 else "سوق هادئ")
                st.write("🔍 **نصيحة المدير:**")
                st.info("لو القوة وصلت 50، الـ 100 جنيه لازم تدخل فوراً في العملة دي.")

            st.write("---")
            st.subheader("📊 جدول البيانات التفصيلي")
            st.table(pd.DataFrame(results))
            
            if top_opportunity['قوة الفرصة'] > 40:
                play_alert()

    time.sleep(4)
