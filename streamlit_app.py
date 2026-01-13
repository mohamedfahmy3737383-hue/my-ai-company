import streamlit as st
import pandas as pd
import requests
import time

# 1. إعدادات السيطرة
st.set_page_config(page_title="Global Sniper Pro", layout="wide")

if 'prev_v' not in st.session_state: st.session_state.prev_v = {}

def play_alarm():
    # تنبيه صوتي هادئ عند الهجوم
    st.components.v1.html("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>""", height=0)

st.title("🌐 رادار السيطرة العالمية (صوت + حيتان + أرباح)")

# 2. إدارة المحفظة
st.sidebar.title("💰 شركة الـ 100 جنيه")
asset_name = st.sidebar.text_input("اسم عملتك للمتابعة:", value="CHZ").upper()
buy_p = st.sidebar.number_input("سعر شرائك بالدولار ($):", value=0.000001, format="%.8f")

def get_data_v10():
    try:
        url = "https://api.coincap.io/v2/assets?limit=150"
        r = requests.get(url, timeout=5)
        if r.status_code == 200: return r.json().get('data', [])
    except: return None
    return None

placeholder = st.empty()

while True:
    data = get_data_v10()
    
    if data:
        results = []
        for item in data:
            try:
                sym = item.get('symbol', '').upper()
                p = float(item.get('priceUsd', 0))
                c = float(item.get('changePercent24Hr', 0))
                v = float(item.get('volumeUsd24Hr', 0))
                
                # قرار الهجوم بناءً على الزخم والسيولة
                status = "🚀 هجوم" if c > 5 else "📡 مراقبة"
                
                results.append({
                    "العملة": sym,
                    "السعر ($)": p,
                    "تغير %": round(c, 2),
                    "السيولة": v,
                    "نشاط الحيتان": "🐳 دخول ضخم" if v > 50000000 else "🐟 أفراد",
                    "القرار": status
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
                c2.metric("حالة الرادار", "✅ متصل ونشط")
                c3.metric("توقيت السيطرة", time.strftime('%H:%M:%S'))

                # إذا كان هناك هجوم على أي عملة، شغل الصوت
                if "🚀 هجوم" in df['القرار'].values:
                    play_alarm()
                    st.warning(f"📢 تنبيه: رصد هجوم سيولة الآن في عملات متصدرة!")

            st.write("---")
            st.subheader("📊 قائمة السيطرة (مرتبة حسب الأقوى)")
            
            # عرض أول 20 عملة
            st.table(df.sort_values(by="تغير %", ascending=False).head(20))
            
            # تحليل خاص لـ CHZ لو موجودة
            if asset_name == "CHZ":
                st.info("💡 تحليل القائد: عملة CHZ مرتبطة بالزخم الرياضي. الهجوم الحالي يعني احتمالية كسر مقاومة سعرية قوية.")
    else:
        st.info("🔄 السيرفر يحاول جلب البيانات... لا تقلق")

    time.sleep(12)
