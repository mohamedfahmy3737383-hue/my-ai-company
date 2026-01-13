import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Professional Sniper", layout="wide")

# نظام إدارة التنبيهات عشان الصوت ميشتغلش باستمرار
if 'alerted_symbols' not in st.session_state:
    st.session_state.alerted_symbols = {}
if 'last_signals' not in st.session_state:
    st.session_state.last_signals = {}

# صوت تنبيه هادي لمرة واحدة
def play_gentle_alert():
    sound_html = """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>"""
    st.components.v1.html(sound_html, height=0)

st.title("🎯 رادار القنص الهادئ")
st.write("الهدف: مراقبة صامتة وإشارات دخول واضحة للـ 100 جنيه")

def get_data():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    data = get_data()
    if data:
        targets = ['PEPEUSDT', 'SHIBUSDT', 'FLOKIUSDT', 'BONKUSDT', 'LUNCUSDT', 'SOLUSDT', 'XRPUSDT']
        rows = []
        current_time = time.time()
        
        for item in data:
            symbol = item['symbol']
            if symbol in targets:
                price = float(item['lastPrice'])
                change = float(item['priceChangePercent'])
                vol = float(item['quoteVolume'])
                
                # شرط الدخول (تحرك إيجابي + سيولة)
                if change > 1.2 and vol > 1500000:
                    # تفعيل الإشارة وتخزين وقتها
                    st.session_state.last_signals[symbol] = current_time
                    
                    # تشغيل التنبيه مرة واحدة فقط لكل عملة كل 5 دقائق عشان ميزعجكش
                    last_alert_time = st.session_state.alerted_symbols.get(symbol, 0)
                    if current_time - last_alert_time > 300: # 5 دقائق
                        play_gentle_alert()
                        st.session_state.alerted_symbols[symbol] = current_time
                
                # الإشارة تفضل خضراء لمدة 60 ثانية
                is_active = symbol in st.session_state.last_signals and (current_time - st.session_state.last_signals[symbol] < 60)
                
                rows.append({
                    "العملة": symbol.replace("USDT", ""),
                    "السعر": f"${price:.8f}",
                    "التغير": f"{change}%",
                    "الحالة": "🟢 فرصة دخول" if is_active else "⚪ مراقبة",
                    "السيولة": f"${vol:,.0f}"
                })

        with placeholder.container():
            # عرض الكروت النشطة فقط
            active_list = [r for r in rows if "فرصة" in r['الحالة']]
            if active_list:
                st.success(f"قناص: تم رصد حركة في {', '.join([x['العملة'] for x in active_list])}. الإشارة ثابتة لمدة دقيقة.")
            
            st.write("---")
            df = pd.DataFrame(rows)
            
            # تلوين الصفوف النشطة
            def highlight_active(s):
                return ['background-color: #004d00' if v == "🟢 فرصة دخول" else '' for v in s]
            
            st.table(df.style.apply(highlight_active, subset=['الحالة']))
            
            st.caption(f"آخر تحديث للرادار: {time.strftime('%H:%M:%S')}")

    time.sleep(5)
