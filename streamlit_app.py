import streamlit as st
import pandas as pd
import requests
import time

# 1. إعدادات السيطرة الفولاذية
st.set_page_config(page_title="Global Control V11", layout="wide")

st.title("🌐 رادار السيطرة العالمية (نسخة اختراق الحظر)")

# 2. إدارة محفظة الـ 100 جنيه
st.sidebar.title("💰 شركة الـ 100 جنيه")
asset_name = st.sidebar.text_input("اسم عملتك (مثل CHZ أو PEPE):", value="CHZ").upper()
buy_p = st.sidebar.number_input("سعر شرائك بالدولار ($):", value=0.000001, format="%.8f")

def play_alarm():
    st.components.v1.html("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>""", height=0)

def force_fetch_data():
    # بنجرب ندخل من "بوابات" مختلفة عشان نتخطى حظر السيرفر
    endpoints = [
        "https://api.coincap.io/v2/assets?limit=50",
        "https://api.coinlore.net/api/tickers/?start=0&limit=50"
    ]
    for url in endpoints:
        try:
            r = requests.get(url, timeout=4)
            if r.status_code == 200:
                res = r.json()
                return res.get('data', res)
        except: continue
    return None

placeholder = st.empty()

while True:
    raw_data = force_fetch_data()
    
    if raw_data:
        results = []
        for item in raw_data:
            try:
                # الكود ذكي بيعرف يقرأ من أي مصدر
                sym = item.get('symbol', item.get('symbol', '??')).upper()
                p = float(item.get('priceUsd', item.get('price_usd', 0)))
                c = float(item.get('changePercent24Hr', item.get('percent_change_24h', 0)))
                
                results.append({
                    "العملة": sym,
                    "السعر ($)": p,
                    "تغير %": round(c, 2),
                    "القرار": "🚀 هجوم" if c > 4 else "📡 رصد"
                })
            except: continue

        df = pd.DataFrame(results)

        with placeholder.container():
            # حساب الأرباح (الـ 100 جنيه)
            my_coin = df[df['العملة'] == asset_name]
            if not my_coin.empty:
                curr_p = my_coin.iloc[0]['السعر ($)']
                val_egp = ((2.0 / buy_p) * curr_p) * 50 if buy_p > 0 else 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric(f"قيمة الـ 100ج في {asset_name}", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("حالة الربط", "✅ تم الاختراق")
                c3.metric("تحديث الرصد", time.strftime('%H:%M:%S'))

                if "🚀 هجوم" in df['القرار'].values:
                    play_alarm()
                    st.warning("🔥 رادار الحيتان رصد هجوم في السوق!")

            st.write("---")
            st.subheader("📊 قائمة الفرص الحالية")
            st.table(df.sort_values(by="تغير %", ascending=False).head(15))
    else:
        st.error("⚠️ جاري تدوير مفاتيح الاتصال... السيرفر يقاوم")

    time.sleep(15) # وقت أطول لضمان عدم الحظر
