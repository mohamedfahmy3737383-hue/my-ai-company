import streamlit as st
import pandas as pd
import yfinance as ticker
import time
import plotly.graph_objects as go

st.set_page_config(page_title="AI Sniper Elite", layout="wide")

st.title("🧠 عقل الإمبراطورية: التحليل اللحظي")

# 💰 إدارة المحفظة
st.sidebar.title("👤 مكتب المدير العام")
asset_input = st.sidebar.text_input("العملة:", value="BTC-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=40000.0)

# حالة الذاكرة للأخبار عشان متختفيش
if 'last_news' not in st.session_state:
    st.session_state['last_news'] = []

placeholder = st.empty()

while True:
    try:
        # 1. جلب السعر أولاً (بسرعة البرق)
        t = ticker.Ticker(asset_input)
        curr_p = t.fast_info['last_price']
        
        # 2. محاولة جلب الأخبار (بهدوء)
        try:
            raw_news = t.news[:5]
            if raw_news:
                st.session_state['last_news'] = [n['title'] for n in raw_news]
        except:
            pass # لو الأخبار علقت، هنستخدم آخر أخبار سجلناها

        # 3. تحليل المشاعر (AI)
        pos_w = ['up', 'bullish', 'gain', 'buy', 'high', 'surge', 'good', 'top']
        neg_w = ['down', 'bearish', 'loss', 'sell', 'low', 'drop', 'crash', 'risk']
        
        score = 0
        for title in st.session_state['last_news']:
            t_low = title.lower()
            score += sum(1 for w in pos_w if w in t_low)
            score -= sum(1 for w in neg_w if w in t_low)

        with placeholder.container():
            c1, c2 = st.columns([1, 1.5])
            
            with c1:
                st.subheader("🤖 قرار الـ AI")
                decision = "🚀 شراء" if score > 0 else "🔴 بيع" if score < 0 else "📡 مراقبة"
                d_color = "green" if score > 0 else "red" if score < 0 else "white"
                st.markdown(f"### :{d_color}[{decision}]")
                
                # حساب الـ 100 جنيه (أهم حاجة)
                val_egp = ((2.0 / buy_p) * curr_p) * 50
                st.metric("قيمة الـ 100ج", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")

            with c2:
                st.subheader("📰 نشرة أخبار الإمبراطورية")
                if st.session_state['last_news']:
                    for title in st.session_state['last_news']:
                        st.write(f"🔹 {title}")
                else:
                    st.write("⌛ جاري سحب الأخبار من السيرفر...")

            st.write("---")
            # الرسم البياني
            hist = t.history(period="1d", interval="5m")['Close']
            fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist.values, line=dict(color='#00ff00'))])
            fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), template="plotly_dark")
            st.plotly_chart(fig, width='stretch')

    except Exception as e:
        st.write("🔄 نظام الدفاع ضد الحظر نشط.. ثواني")
        time.sleep(5)
    
    time.sleep(15) # تحديث كل 15 ثانية
