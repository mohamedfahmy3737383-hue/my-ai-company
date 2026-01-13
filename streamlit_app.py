import streamlit as st
import pandas as pd
import yfinance as ticker
import time

st.set_page_config(page_title="Global Empire Dashboard", layout="wide")

st.title("🏛️ إمبراطورية الـ 100 جنيه - مركز السيطرة العالمي")
st.write("الرادار يراقب الآن: الكريبتو، الأسهم الأمريكية، والذهب")

# 💰 إدارة الأصول المتعددة
st.sidebar.title("💳 محفظة الإمبراطورية")
asset_type = st.sidebar.selectbox("نوع الأصول:", ["كريبتو", "أسهم عالمية", "معادن"])
target_asset = st.sidebar.text_input("رمز الأصول (مثلاً AAPL أو Gold):", value="CHZ-USD").upper()
buy_price = st.sidebar.number_input("سعر دخولك ($):", value=0.15, format="%.4f")

# القائمة العالمية الجديدة
world_radar = {
    'الذهب': 'GC=F',
    'بتكوين': 'BTC-USD',
    'تسلا': 'TSLA',
    'إنفيدا': 'NVDA',
    'أبل': 'AAPL',
    'تشيليز': 'CHZ-USD',
    'الدولار/جنيه': 'EGP=X'
}

placeholder = st.empty()

while True:
    try:
        # سحب بيانات السوق الشامل
        data = ticker.download(list(world_radar.values()), period="1d", interval="1m", progress=False)['Close']
        
        if not data.empty:
            results = []
            last_p = data.iloc[-1]
            prev_p = data.iloc[-5] if len(data) > 5 else data.iloc[0]
            
            for name, sym in world_radar.items():
                curr = float(last_p[sym])
                change = ((curr - float(prev_p[sym])) / float(prev_p[sym])) * 100
                
                results.append({
                    "الأصل": name,
                    "الرمز": sym,
                    "السعر الحالي": f"{curr:,.2f}$",
                    "الحركة اللحظية %": round(change, 3),
                    "الوضع": "🔥 انفجار" if change > 0.2 else "🟢 صعود" if change > 0 else "🔴 هبوط"
                })

            df = pd.DataFrame(results)

            with placeholder.container():
                # حساب قيمة الـ 100 جنيه في الإمبراطورية
                try:
                    live_price = ticker.Ticker(target_asset).fast_info['last_price']
                    current_value = ((2.0 / buy_price) * live_price) * 50
                except: current_value = 100

                c1, c2, c3 = st.columns(3)
                c1.metric("قيمة الـ 100ج الآن", f"{current_value:.2f} ج.م", f"{current_value-100:.2f}")
                c2.metric("أقوى أصل متحرك", df.sort_values(by="الحركة اللحظية %").iloc[-1]['الأصل'])
                c3.metric("توقيت الإمبراطورية", time.strftime('%H:%M:%S'))

                st.write("---")
                st.subheader("📊 رادار الأسواق العالمية المختلطة")
                st.table(df)
                
                # نصيحة الإمبراطور
                if "🔥 انفجار" in df['الوضع'].values:
                    st.balloons()
                    st.success("🚨 يا مدير! فيه فرصة تاريخية بتحصل في الأسواق دلوقتي!")

    except Exception as e:
        st.error(f"محاولة ربط الإمبراطورية بالسوق... {e}")

    time.sleep(20)
