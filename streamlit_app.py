import streamlit as st
import pandas as pd
import yfinance as ticker
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Empire Command Center", layout="wide")

st.title("🏛️ مركز العمليات: الرادار والإشارات")

# 💰 مكتب المدير
st.sidebar.title("👤 مكتب المدير العام")
asset_input = st.sidebar.text_input("العملة الرئيسية:", value="BTC-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=40000.0)

# قائمة العملات المستهدفة
watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD']

placeholder = st.empty()

while True:
    try:
        # سحب بيانات كل العملات مرة واحدة (أسرع وأضمن)
        data = ticker.download(watchlist, period="1d", interval="2m", progress=False)['Close']
        
        if not data.empty:
            data = data.ffill().bfill()
            results = []
            
            for sym in watchlist:
                prices = data[sym]
                curr_p = prices.iloc[-1]
                
                # حساب الإشارة (سيد رادار)
                change = ((curr_p - prices.iloc[-5]) / prices.iloc[-5]) * 100 if len(prices) > 5 else 0
                
                # حساب الانفجار (عصام كاشف)
                p_range = (prices.tail(15).max() - prices.tail(15).min()) / prices.tail(15).mean()
                
                if change > 0.35: 
                    signal = "🟢 BUY"
                elif change < -0.35: 
                    signal = "🔴 SELL"
                elif p_range < 0.003: 
                    signal = "⚠️ SQUEEZE"
                else: 
                    signal = "📡 WATCH"

                results.append({
                    "العملة": sym.replace("-USD", ""),
                    "السعر": f"{curr_p:.4f}",
                    "الحالة": signal
                })

            df = pd.DataFrame(results)

            with placeholder.container():
                # 1. المقاييس العلوية
                c1, c2, c3 = st.columns(3)
                
                # حساب الـ 100 جنيه
                target_p = data[asset_input].iloc[-1]
                val_egp = ((2.0 / buy_p) * target_p) * 50 if buy_p > 0 else 100
                
                c1.metric(f"محفظة الـ 100ج ({asset_input})", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("عدد الفرص", f"{len(df[df['الحالة']=='🟢 BUY'])}")
                c3.metric("توقيت الرادار", time.strftime('%H:%M:%S'))

                st.write("---")
                
                # 2. الجدول الملون (الإشارات)
                def style_signal(val):
                    color = '#00ff00' if 'BUY' in val else '#ff0000' if 'SELL' in val else '#ffa500' if 'SQUEEZE' in val else 'white'
                    return f'color: {color}; font-weight: bold'
                
                st.subheader("📊 تقرير العملات والاشارات اللحظي")
                st.table(df.style.applymap(style_signal, subset=['الحالة']))

                # 3. الرسم البياني (خالد شارت)
                st.write("---")
                st.subheader(f"📈 الرسم البياني لـ {asset_input}")
                hist = data[asset_input].tail(40)
                fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist.values, line=dict(color='#00ff00', width=2))])
                fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), template="plotly_dark")
                st.plotly_chart(fig, width='stretch')

        time.sleep(20) # وقت مثالي للتحديث بدون حظر

    except Exception as e:
        st.error("🔄 السيرفر بيحاول يجمع البيانات.. ثواني وهتظهر")
        time.sleep(10)
