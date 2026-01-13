import streamlit as st
import pandas as pd
import yfinance as ticker
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Empire Stealth Mode", layout="wide")

st.title("🏛️ رادار الإمبراطورية (نمط التخفي)")
st.write(f"🛡️ نظام تجاوز الحظر نشط | {time.strftime('%H:%M:%S')}")

# 2. مكتب المدير العام
st.sidebar.title("👤 مكتب المدير العام")
asset_input = st.sidebar.text_input("العملة للمتابعة:", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=0.1500, format="%.4f")

# القائمة الذهبية - قللناها عشان السرعة
watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD']

placeholder = st.empty()

while True:
    results = []
    try:
        for sym in watchlist:
            # طلب منفرد لكل عملة (أخف بكتير على السيرفر)
            t = ticker.Ticker(sym)
            curr_p = t.fast_info['last_price']
            
            # حساب إشارة سريعة
            results.append({
                "العملة": sym.replace("-USD", ""),
                "السعر": f"{curr_p:.4f}",
                "الحالة": "📡 رصد مستمر"
            })
            time.sleep(1) # تبريد ثانية بين كل عملة والتانية

        df = pd.DataFrame(results)

        with placeholder.container():
            c1, c2, c3 = st.columns(3)
            
            # مجدي حسابات - طلب مباشر
            target_p = ticker.Ticker(asset_input).fast_info['last_price']
            val_egp = ((2.0 / buy_p) * target_p) * 50 if buy_p > 0 else 100
            
            c1.metric(f"قيمة الـ 100ج ({asset_input})", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
            c2.metric("حالة الربط", "✅ آمن")
            c3.metric("توقيت", time.strftime('%H:%M:%S'))

            st.write("---")
            
            # خالد شارت - نسخة مبسطة لعدم التهنيج
            st.subheader(f"📈 نبض {asset_input}")
            hist = ticker.download(asset_input, period="1d", interval="5m", progress=False)['Close']
            fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist.values, line=dict(color='#00ff00'))])
            fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), template="plotly_dark")
            st.plotly_chart(fig, width='stretch')

            st.table(df)

    except Exception as e:
        st.info("🔄 السيرفر بيحمل بيانات جديدة.. خليك معايا")
        time.sleep(10)
        continue
    
    time.sleep(30) # تحديث كل 30 ثانية لضمان الاستمرارية
