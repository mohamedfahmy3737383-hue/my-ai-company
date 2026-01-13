import streamlit as st
import pandas as pd
import yfinance as ticker
import time
import plotly.graph_objects as go

# 1. إعدادات 2026
st.set_page_config(page_title="Empire Control 2026", layout="wide")

st.title("🏛️ المركز الرئيسي للإمبراطورية (تحديث 2026)")
st.write(f"🔄 النظام يعمل بنظام التبريد لتجنب الحظر | التوقيت: {time.strftime('%H:%M:%S')}")

# 2. مكتب المدير العام
st.sidebar.title("👤 مكتب المدير العام")
asset_input = st.sidebar.text_input("العملة للمتابعة:", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=0.1500, format="%.4f")
target_profit = st.sidebar.slider("هدف الربح (ج.م):", 105, 500, 120)

# تقليل القائمة لضمان استقرار السيرفر
watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD']

placeholder = st.empty()

while True:
    try:
        # طلب البيانات مع نظام هادئ
        data = ticker.download(watchlist, period="1d", interval="2m", progress=False)
        
        if not data.empty:
            prices_df = data['Close'].ffill().bfill()
            report_data = []
            
            for sym in watchlist:
                prices = prices_df[sym]
                curr_p = prices.iloc[-1]
                
                # حساب الـ Squeeze و RSI
                p_range = (prices.tail(15).max() - prices.tail(15).min()) / prices.tail(15).mean()
                change = ((curr_p - prices.iloc[-5]) / prices.iloc[-5]) * 100
                
                status = "🟢 BUY" if change > 0.4 else "⚠️ SQUEEZE" if p_range < 0.003 else "📡 WATCH"
                
                report_data.append({
                    "العملة": sym.replace("-USD",""),
                    "السعر": f"{curr_p:.4f}",
                    "الحالة": status
                })

            df = pd.DataFrame(report_data)

            with placeholder.container():
                # --- المقاييس الذكية ---
                m1, m2, m3 = st.columns(3)
                
                with m1:
                    target_p = ticker.Ticker(asset_input).fast_info['last_price']
                    val_egp = ((2.0 / buy_p) * target_p) * 50
                    st.metric("قيمة الـ 100ج", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                    if val_egp >= target_profit: st.balloons()

                with m2:
                    st.warning("🕵️‍♂️ عصام كاشف")
                    st.write(f"نبض العملة الحالي: {status}")

                with m3:
                    st.success("🎯 سيد رادار")
                    st.write(f"آخر تحديث: {time.strftime('%H:%M:%S')}")

                st.write("---")
                
                # --- خالد شارت (بتحديث 2026) ---
                st.subheader(f"📈 الرسم البياني لـ {asset_input}")
                hist = ticker.download(asset_input, period="1d", interval="2m", progress=False)['Close']
                fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist.values, line=dict(color='#00ff00'))])
                fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), template="plotly_dark")
                # التعديل المطلوب لعام 2026: width='stretch'
                st.plotly_chart(fig, width='stretch')

                st.table(df)

    except Exception as e:
        st.info("😴 السيرفر في استراحة قصيرة لتجنب الحظر (Cooling Down...)")
        time.sleep(30)
        continue

    # زيادة وقت النوم لراحة السيرفر
    time.sleep(25)
