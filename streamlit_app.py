import streamlit as st
import pandas as pd
import requests
import time

# 1. إعدادات السيطرة
st.set_page_config(page_title="Global Command Final", layout="wide")

if 'prev_v' not in st.session_state: st.session_state.prev_v = {}

st.title("🌐 رادار السيطرة العالمية (نسخة اختراق الحجب)")
# إضافة صوت تنبيه عند الهجوم
def play_alarm():
    st.components.v1.html(
        """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>""",
        height=0,
    )

# داخل حلقة الـ While، لو فيه هجوم:
if "🚀 هجوم" in df['القرار'].values:
    play_alarm()
# 2. محفظة الـ 100 جنيه
st.sidebar.title("💰 محفظة الـ 100 جنيه")
asset_name = st.sidebar.text_input("اسم عملتك (مثل PEPE):", value="PEPE").upper()
buy_p = st.sidebar.number_input("سعر شرائك بالدولار ($):", value=0.000001, format="%.8f")

# 3. دالة جلب البيانات "المصفحة"
def get_data_no_matter_what():
    # بنجرب 3 بوابات مختلفة، لو واحدة مقفولة التانية تفتح
    urls = [
        "https://api.coincap.io/v2/assets?limit=100",
        "https://api.coinlore.net/api/tickers/",
        "https://api.binance.com/api/v3/ticker/24hr"
    ]
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                d = r.json()
                # تنسيق البيانات حسب المصدر اللي رد
                if 'data' in d: return d['data']
                return d
        except: continue
    return None

placeholder = st.empty()

while True:
    raw = get_data_no_matter_what()
    
    if raw:
        results = []
        for item in raw:
            try:
                # محاولة قراءة البيانات بمرونة (لأن كل موقع له أسامي مختلفة)
                sym = item.get('symbol', item.get('symbol', '??')).upper()
                p = float(item.get('priceUsd', item.get('price_usd', item.get('lastPrice', 0))))
                c = float(item.get('changePercent24Hr', item.get('percent_change_24h', item.get('priceChangePercent', 0))))
                v = float(item.get('volumeUsd24Hr', item.get('volume24', item.get('quoteVolume', 0))))
                
                results.append({
                    "العملة": sym,
                    "السعر ($)": p,
                    "تغير %": round(c, 2),
                    "السيولة": v,
                    "القرار": "🚀 هجوم" if c > 5 else "📡 مراقبة"
                })
            except: continue

        df = pd.DataFrame(results)

        with placeholder.container():
            # حساب الأرباح
            my_coin = df[df['العملة'] == asset_name]
            if not my_coin.empty:
                curr_p = my_coin.iloc[0]['السعر ($)']
                val_egp = ((2.0 / buy_p) * curr_p) * 50 if buy_p > 0 else 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric(f"قيمة الـ 100ج في {asset_name}", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("حالة السوق", "🔥 نشط" if c > 0 else "❄️ هادئ")
                c3.metric("آخر تحديث", time.strftime('%H:%M:%S'))

            st.write("---")
            st.subheader("📊 أقوى 15 عملة في العالم حالياً")
            st.table(df.sort_values(by="تغير %", ascending=False).head(15))
            
    else:
        st.error("⚠️ السيرفر محجوب مؤقتاً.. سأقوم بالمحاولة مرة أخرى خلال ثوانٍ")

    time.sleep(12)
