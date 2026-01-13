import streamlit as st
import pandas as pd
import requests
import time

# 1. إعدادات السيطرة (ثبات وسرعة)
st.set_page_config(page_title="Global Crypto Command", layout="wide")

if 'prev_v' not in st.session_state: st.session_state.prev_v = {}

st.title("🌐 مركز قيادة الكريبتو العالمي")
st.write("يتم الآن مراقبة كافة العملات التي تمتلك سيولة نشطة في العالم")

# 2. محفظة الـ 100 جنيه (القائد)
st.sidebar.title("💰 إدارة الأرباح")
target_asset = st.sidebar.text_input("العملة التي تملكها (مثال: PEPE):", value="PEPE").upper()
buy_p = st.sidebar.number_input("سعر شرائك بالدولار ($):", value=0.000001, format="%.8f")

def get_fast_global_data():
    # استخدام بوابة بيانات مجمعة وسريعة جداً
    try:
        url = "https://api.coincap.io/v2/assets?limit=300" # ركزنا على أول 300 عملة (العمود الفقري للسوق)
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json().get('data', [])
    except:
        return None

placeholder = st.empty()

while True:
    data = get_fast_global_data()
    
    if data:
        results = []
        for item in data:
            try:
                sym = item.get('symbol')
                p = float(item.get('priceUsd', 0))
                c = float(item.get('changePercent24Hr', 0))
                v = float(item.get('volumeUsd24Hr', 0))
                
                # حساب تدفق الحيتان اللحظي
                old_v = st.session_state.prev_v.get(sym, v)
                flow = v - old_v
                st.session_state.prev_v[sym] = v
                
                results.append({
                    "العملة": sym,
                    "السعر ($)": p,
                    "تغير% (24س)": round(c, 2),
                    "تدفق السيولة": flow,
                    "نشاط الحيتان": "🐳 حوت ضخم" if flow > 50000 else "🐟 أفراد",
                    "القرار": "🚀 هجوم" if c > 10 or flow > 100000 else "📡 مراقبة"
                })
            except: continue

        df = pd.DataFrame(results)

        with placeholder.container():
            # حسابات الـ 100 جنيه
            my_coin_row = df[df['العملة'] == target_asset]
            if not my_coin_row.empty:
                curr_
