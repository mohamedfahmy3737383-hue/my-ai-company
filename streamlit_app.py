import streamlit as st
import pandas as pd
import yfinance as ticker
import time
import plotly.graph_objects as go

# 1. إعدادات القيادة
st.set_page_config(page_title="Empire Stealth Mode", layout="wide")

st.title("🏛️ رادار الإمبراطورية (تجاوز الحظر)")
st.write(f"🛡️ وضع التخفي نشط | التوقيت: {time.strftime('%H:%M:%S')}")

# 2. مكتب المدير
st.sidebar.title("👤 مكتب المدير")
asset_input = st.sidebar.text_input("العملة:", value="BTC-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=40000.0)

placeholder = st.empty()

while True:
    try:
        # طلب البيانات بأخف طريقة ممكنة
        t = ticker.Ticker(asset_input)
        # سحب السعر اللحظي فقط بدون الأخبار لتقليل الحمل
        price_data = t.fast_info
        curr_p = price_data['last_price']
        
        # حساب الـ 100 جنيه
        val_egp = ((2.0 / buy_p) * curr_p) * 50 if buy_p > 0 else 100
        change_day = price_data['year_change'] # مجرد نبض للسوق

        with placeholder.container():
            c1, c2, c3 = st.columns(3)
            
            with c1:
                st.metric(f"قيمة الـ 100ج في {asset_input}", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
            
            with c2:
                st.metric("السعر اللحظي ($)", f"{curr_p:.2f}")
                
            with c3:
                status = "🟢 صامد" if val_egp >= 100 else "🔴 تراجع"
                st.metric("حالة الإمبراطورية", status)

            st.write("---")
            # رسم بياني خفيف (آخر يوم بفاصل ساعة لتقليل الضغط)
            st.subheader("📈 نبض السوق (60 دقيقة)")
            hist = t.history(period="1d", interval="60m")['Close']
            fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist.values, line=dict(color='#00ff00'))])
            fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), template="plotly_dark")
            st.plotly_chart(fig, width='stretch')

        # لو وصلنا هنا يبقى الطلب نجح، نريح 25 ثانية عشان منتحظرش تاني
        time.sleep(25)

    except Exception as e:
        # لو حصل حظر، نختفي تماماً لمدة دقيقة ونرجع
        st.warning("⚠️ السيرفر كشفنا! جاري تغيير التكتيك والانتظار 60 ثانية لفك الحظر...")
        time.sleep(60)
