import streamlit as st
import pandas as pd
import yfinance as ticker
import time
import plotly.graph_objects as go

# إعدادات الصفحة
st.set_page_config(page_title="AI News Trader", layout="wide")

st.title("🧠 عقل الإمبراطورية: محلل الأخبار والسعر")
st.write("الوضع الحالي: جلب الأخبار الحقيقية وتحليلها لاتخاذ قرار")

# 💰 إدارة المحفظة
st.sidebar.title("👤 مكتب المدير العام")
asset_input = st.sidebar.text_input("العملة للمتابعة (مثلاً BTC-USD):", value="BTC-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=40000.0)

placeholder = st.empty()

while True:
    try:
        # 1. جلب بيانات السعر والأخبار الحقيقية
        t = ticker.Ticker(asset_input)
        curr_p = t.fast_info['last_price']
        news = t.news[:5] # جلب آخر 5 أخبار حقيقية للعملة
        
        # 2. تحليل بسيط لمشاعر الأخبار (AI Logic)
        positive_words = ['up', 'bullish', 'gain', 'buy', 'high', 'growth', 'surge', 'support']
        negative_words = ['down', 'bearish', 'loss', 'sell', 'low', 'drop', 'crash', 'risk']
        
        sentiment_score = 0
        news_list = []
        
        for n in news:
            title = n['title'].lower()
            news_list.append(n['title'])
            for word in positive_words:
                if word in title: sentiment_score += 1
            for word in negative_words:
                if word in title: sentiment_score -= 1

        # 3. اتخاذ القرار (Decision Engine)
        if sentiment_score > 0:
            ai_decision = "🚀 شراء (أخبار إيجابية)"
            decision_color = "green"
        elif sentiment_score < 0:
            ai_decision = "🔴 بيع (أخبار سلبية)"
            decision_color = "red"
        else:
            ai_decision = "📡 مراقبة (أخبار محايدة)"
            decision_color = "white"

        with placeholder.container():
            c1, c2 = st.columns([1, 1.5])
            
            with c1:
                st.subheader("🤖 قرار الـ AI اللحظي")
                st.markdown(f"### :{decision_color}[{ai_decision}]")
                
                # حساب الـ 100 جنيه
                val_egp = ((2.0 / buy_p) * curr_p) * 50
                st.metric("قيمة الـ 100ج الآن", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                st.write(f"درجة تفاؤل السوق: {sentiment_score}")

            with c2:
                st.subheader("📰 آخر الأخبار المؤثرة")
                for i, title in enumerate(news_list):
                    st.write(f"{i+1}. {title}")

            st.write("---")
            # رسم بياني سريع
            hist = t.history(period="1d", interval="5m")['Close']
            fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist.values, line=dict(color='#00ff00'))])
            fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), template="plotly_dark")
            st.plotly_chart(fig, width='stretch')

    except Exception as e:
        st.info("🔄 جاري تحديث البيانات الإخبارية والسعرية...")
    
    time.sleep(30)
