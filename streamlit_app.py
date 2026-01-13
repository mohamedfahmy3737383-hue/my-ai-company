import streamlit as st
import pandas as pd
import yfinance as ticker
import time
import plotly.graph_objects as go

# 1. إعدادات القيادة المركزية
st.set_page_config(page_title="Empire Global Control", layout="wide")

st.title("🏛️ المركز الرئيسي لإمبراطورية الـ 100 جنيه")
st.write(f"🚀 جميع الأقسام تعمل الآن | التوقيت: {time.strftime('%H:%M:%S')}")

# 2. مكتب المدير العام (Sidebar)
st.sidebar.title("👤 مكتب المدير العام")
asset_input = st.sidebar.text_input("العملة للمتابعة:", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=0.1500, format="%.4f")
target_profit = st.sidebar.slider("حدد هدف ربحك (ج.م):", 105, 500, 120)

watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD', 'PEPE24478-USD', 'BONK-USD']

placeholder = st.empty()

while True:
    try:
        # جلب البيانات
        data = ticker.download(watchlist, period="1d", interval="1m", progress=False)['Close']
        
        if not data.empty:
            data = data.ffill().bfill()
            report_data = []
            
            for sym in watchlist:
                prices = data[sym]
                curr_p = prices.iloc[-1]
                # حساب RSI مبسط (مؤشر القوة)
                delta = prices.diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs.iloc[-1]))
                
                # كاشف الانفجار (Squeeze)
                p_range = (prices.tail(20).max() - prices.tail(20).min()) / prices.tail(20).mean()
                
                # الإشارات
                change = ((curr_p - prices.iloc[-5]) / prices.iloc[-5]) * 100
                
                if rsi > 70: status = "🔴 SELL (تشبع شراء)"
                elif rsi < 30 or (change > 0.4): status = "🟢 BUY (دخول قوي)"
                elif p_range < 0.0025: status = "⚠️ SQUEEZE (شحن)"
                else: status = "📡 WATCH (رصد)"
                
                report_data.append({
                    "العملة": sym.replace("-USD",""),
                    "السعر": f"{curr_p:.6f}" if curr_p < 0.1 else f"{curr_p:.4f}",
                    "RSI": round(rsi, 2),
                    "الحالة": status
                })

            df = pd.DataFrame(report_data)

            with placeholder.container():
                # --- تقارير الموظفين ---
                m1, m2, m3 = st.columns(3)
                
                with m1:
                    st.info("👨‍💼 **مجدي حسابات**")
                    curr_target_p = ticker.Ticker(asset_input).fast_info['last_price']
                    val_egp = ((2.0 / buy_p) * curr_target_p) * 50
                    st.metric("قيمة الـ 100ج", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                    if val_egp >= target_profit:
                        st.balloons()
                        st.success(f"🎯 مبروك يا مدير! وصلنا للهدف: {val_egp:.2f} ج.م")

                with m2:
                    st.warning("🕵️‍♂️ **عصام كاشف**")
                    sqz = df[df['الحالة'].str.contains("SQUEEZE")]['العملة'].tolist()
                    st.write(f"الانفجارات القادمة: {', '.join(sqz) if sqz else 'لا يوجد'}")
                    st.write(f"نبض السوق: {asset_input} عند RSI {df[df['العملة']==asset_input.replace('-USD','')]['RSI'].values[0]}")

                with m3:
                    st.success("🎯 **سيد رادار**")
                    buys = df[df['الحالة'].str.contains("BUY")]['العملة'].tolist()
                    st.write(f"فرص ضرب الآن: {', '.join(buys) if buys else 'ننتظر الإشارة'}")

                st.write("---")
                
                # --- خالد شارت (الرسام) ---
                st.subheader(f"📈 حركة {asset_input} في آخر ساعة")
                target_history = ticker.download(asset_input, period="1d", interval="1m", progress=False)['Close']
                fig = go.Figure(data=[go.Scatter(x=target_history.index, y=target_history.values, line=dict(color='#00ff00', width=2))])
                fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

                # الجدول المركزى
                st.subheader("📊 بيان العمليات المركزية")
                st.table(df)

    except: pass
    time.sleep(15)
