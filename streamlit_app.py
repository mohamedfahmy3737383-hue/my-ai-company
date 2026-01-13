import streamlit as st
import pandas as pd
import yfinance as ticker
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Empire Final Station", layout="wide")

# --- واجهة المدير ---
st.sidebar.title("👤 إدارة العمليات")
asset_input = st.sidebar.text_input("العملة الرئيسية (مثل CHZ-USD):", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=0.1500, format="%.4f")

watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD', 'SHIB-USD']

st.title("🏛️ مركز السيطرة النهائي")
placeholder = st.empty()

while True:
    try:
        # جلب البيانات لكل القائمة مرة واحدة لتقليل الضغط
        data = ticker.download(watchlist, period="1d", interval="2m", progress=False)['Close']
        
        if not data.empty:
            data = data.ffill().bfill()
            results = []
            
            for sym in watchlist:
                prices = data[sym]
                curr_p = prices.iloc[-1]
                
                # حساب الإشارات (سيد رادار)
                change = ((curr_p - prices.iloc[-5]) / prices.iloc[-5]) * 100
                
                # كاشف الانفجار (عصام كاشف)
                p_range = (prices.tail(15).max() - prices.tail(15).min()) / prices.tail(15).mean()
                
                # المنطق البرمجي للإشارة
                if change > 0.30: signal = "🟢 BUY"
                elif change < -0.30: signal = "🔴 SELL"
                elif p_range < 0.0025: signal = "⚠️ SQUEEZE"
                else: signal = "📡 WATCH"

                results.append({"العملة": sym.replace("-USD",""), "السعر": f"{curr_p:.4f}", "الحالة": signal})

            df = pd.DataFrame(results)

            with placeholder.container():
                # 1. حسابات مجدي (الـ 100 جنيه)
                target_p = data[asset_input].iloc[-1]
                val_egp = ((2.0 / buy_p) * target_p) * 50
                
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.metric(f"محفظة الـ 100ج ({asset_input})", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                with c2:
                    st.success(f"تحديث حي للرادار | {time.strftime('%H:%M:%S')}")

                # 2. جدول الإشارات (سيد رادار)
                st.subheader("📊 رادار الإشارات اللحظي")
                def color_rows(val):
                    color = '#00ff00' if 'BUY' in val else '#ff0000' if 'SELL' in val else '#ffa500' if 'SQUEEZE' in val else 'white'
                    return f'color: {color}; font-weight: bold'
                st.table(df.style.applymap(color_rows, subset=['الحالة']))

                # 3. الرسم البياني (خالد شارت)
                st.subheader(f"📈 تحليل حركة {asset_input}")
                hist = data[asset_input].tail(40)
                fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist.values, line=dict(color='#00ff00', width=3))])
                fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), template="plotly_dark")
                st.plotly_chart(fig, width='stretch')

    except Exception as e:
        st.error("🔄 السيرفر مجهد.. سأحاول مرة أخرى خلال ثوانٍ")
        time.sleep(10)
    
    time.sleep(20)
