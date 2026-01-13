import streamlit as st
import pandas as pd
import requests
import time

# 1. إعدادات المنصة الاحترافية الشاملة
st.set_page_config(page_title="الرادار العملاق - مجمع العملات", layout="wide")

if 'prev_vol' not in st.session_state:
    st.session_state.prev_vol = {}
if 'last_signals' not in st.session_state:
    st.session_state.last_signals = {}

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>""", height=0)

# 2. إدارة المحفظة والـ 100 جنيه
st.sidebar.title("💰 محفظة الـ 100 جنيه")
buy_price = st.sidebar.number_input("سعر شراء عملتك (بالدولار):", value=0.000001, format="%.8f")
target_profit = st.sidebar.slider("هدف الربح فوق الـ 100 (بالجنيه):", 1, 100, 20)

st.title("🐋 رادار الشركة المتكامل (النسخة الكاملة)")

def fetch_data():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    data = fetch_data()
    if data:
        # قائمة "كل" العملات اللي اتكلمنا عنها (كبير وصغير ورخيص)
        targets = [
            'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT', 'PEPEUSDT', 
            'SHIBUSDT', 'BONKUSDT', 'FLOKIUSDT', 'LUNCUSDT', '1000SATSUSDT', 
            'RATSUSDT', 'TURBOUSDT', 'BOMEUSDT', 'MEMEUSDT', 'XECUSDT'
        ]
        rows = []
        current_time = time.time()
        
        for item in data:
            if item['symbol'] in targets:
                symbol = item['symbol']
                price = float(item['lastPrice'])
                change = float(item['priceChangePercent'])
                current_vol = float(item['quoteVolume'])
                
                # حساب السيولة اللحظية
                prev_v = st.session_state.prev_vol.get(symbol, current_vol)
                new_money = current_vol - prev_v
                st.session_state.prev_vol[symbol] = current_vol
                
                # حساب قوة الفرصة وتوقعات الذكاء
                power_score = (change * 5) + (new_money / 1000)
                
                if power_score > 35 or new_money > 5000:
                    st.session_state.last_signals[symbol] = current_time
                    play_alert()
                
                is_active = symbol in st.session_state.last_signals and (current_time - st.session_state.last_signals[symbol] < 60)
                
                # ذكاء التوقعات
                prediction = "🚀 انفجار" if change > 5 else "↗️ صعود" if change > 1 else "📉 هبوط" if change < -3 else "➡️ استقرار"

                rows.append({
                    "العملة": symbol.replace("USDT", ""),
                    "السعر": f"${price:.8f}",
                    "التغير": f"{change}%",
                    "سيولة لحظية": f"${new_money:,.0f}",
                    "القوة": round(power_score, 1),
                    "التوقع": prediction,
                    "القرار": "🔥 هجوم" if is_active else "⏳ مراقبة"
                })

        with placeholder.container():
            # حسابات الـ 100 جنيه الفورية
            # بنحسب الربح بناءً على سعر العملة اللي انت متابعها (أو PEPE كافتراضي)
            target_p = [r for r in rows if r['العملة'] == "PEPE"][0]['السعر'] if any(r['العملة'] == "PEPE" for r in rows) else rows[0]['السعر']
            curr_p_float = float(target_p.replace('$', ''))
            val_egp = ((2.0 / buy_price) * curr_p_float) * 50 if buy_price > 0 else 100
            
            c1, c2, c3 = st.columns(3)
            c1.metric("قيمة الـ 100 ج الآن", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
            c2.metric("حالة الرادار", "فرص نشطة" if any("🔥" in r['القرار'] for r in rows) else "مراقب")
            c3.metric("الوقت اللحظي", time.strftime('%H:%M:%S'))

            st.progress(min(max((val_egp-100)/target_profit, 0.0), 1.0) if val_egp > 100 else 0.0)

            st.write("---")
            # الجدول الشامل المرتب حسب الأقوى
            df = pd.DataFrame(rows).sort_values(by="القوة", ascending=False)
            
            def style_rows(s):
                return ['background-color: #4c0000' if v == "🔥 هجوم" else '' for v in s]
            
            st.table(df.style.apply(style_rows, subset=['القرار']))

    time.sleep(5)
