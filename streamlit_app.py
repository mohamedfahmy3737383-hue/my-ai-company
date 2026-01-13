import streamlit as st
import pandas as pd
import requests
import time

# إعدادات خفيفة جداً لمنع التهنيج
st.set_page_config(page_title="Ultra Fast Sniper", layout="wide")

# ذاكرة الشركة
if 'prev_v' not in st.session_state: st.session_state.prev_v = {}

st.title("🏹 رادار السيطرة الفوري (نسخة الطوارئ)")

# مدخلات المحفظة
buy_p = st.sidebar.number_input("سعر شراء عملتك ($):", value=0.000001, format="%.8f")

def get_data():
    try:
        # اتصال مباشر وسريع
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=3)
        return r.json()
    except: return None

placeholder = st.empty()

while True:
    data = get_data()
    if data:
        # القائمة الذهبية
        targets = ['BTCUSDT','ETHUSDT','SOLUSDT','PEPEUSDT','SHIBUSDT','BONKUSDT','FLOKIUSDT','LUNCUSDT','1000SATSUSDT','DOGEUSDT']
        rows = []
        
        for item in data:
            sym = item.get('symbol')
            if sym in targets:
                p = float(item['lastPrice'])
                c = float(item['priceChangePercent'])
                v = float(item['quoteVolume'])
                
                # حساب تدفق الحيتان
                old = st.session_state.prev_v.get(sym, v)
                flow = v - old
                st.session_state.prev_v[sym] = v
                
                # قرار الشركة
                if flow > 50000 or c > 5: action = "🔥 هجوم"
                elif flow > 10000: action = "🐳 حوت"
                else: action = "📡 رصد"
                
                rows.append({
                    "العملة": sym.replace("USDT",""),
                    "السعر": f"{p:.8f}" if p < 1 else f"{p:,.2f}",
                    "تغير%": c,
                    "فلوس دخلت": f"${flow:,.0f}",
                    "القرار": action
                })

        with placeholder.container():
            # حساب الـ 100 جنيه فوراً
            # بنستخدم سعر أول عملة في القائمة كمرجع (غالباً PEPE أو BTC)
            curr_ref = float(rows[3]['السعر'].replace(',','')) if len(rows)>3 else p
            val_egp = ((2.0 / buy_p) * curr_p) * 50 if buy_p > 0 else 100
            
            c1, c2 = st.columns(2)
            c1.metric("الـ 100 ج بقت كام؟", f"{val_egp:.2f} ج.م")
            c2.metric("نبض السوق", time.strftime('%H:%M:%S'))

            # الجدول السريع
            df = pd.DataFrame(rows).sort_values(by="تغير%", ascending=False)
            st.dataframe(df.style.highlight_max(axis=0, subset=['تغير%']), use_container_width=True)

    time.sleep(5) # تحديث كل 5 ثواني
