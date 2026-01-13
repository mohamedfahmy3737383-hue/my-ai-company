import streamlit as st
import pandas as pd
import yfinance as ticker
import time
import plotly.graph_objects as go

# 1. إعدادات السيطرة اللحظية
st.set_page_config(page_title="Crypto Sniper 2026", layout="wide")

st.title("🎯 رادار القناص: تحديث بالثانية")

# 💰 إدارة المحفظة في الجانب
st.sidebar.title("💰 شركة الـ 100 جنيه")
asset_input = st.sidebar.text_input("العملة الرئيسية (مثلاً CHZ-USD):", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=0.1500, format="%.4f")

# القائمة المختصرة لضمان السرعة وعدم الحظر
watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'PEPE24478-USD']

placeholder = st.empty()

while True:
    try:
        # استخدام فترة زمنية صغيرة جداً لسرعة التحميل
        data = ticker.download(watchlist, period="1d", interval="1m", progress=False)['Close']
        
        if not data.empty:
            data = data.ffill().bfill()
            results = []
            
            for sym in watchlist:
                prices = data[sym]
                curr_p = prices.iloc[-1]
                prev_p_2 = prices.iloc[-2] # تغير خلال آخر دقيقتين
                
                # حساب النطاق الضيق (الانفجار)
                p_range = (prices.tail(10).max() - prices.tail(10).min()) / prices.tail(10).mean()
                change_2m = ((curr_p - prev_p_2) / prev_p_2) * 100
                
                # تحديد الإشارة
                if change_2m > 0.2: signal = "🟢 BUY (صعود)"
                elif change_2m < -0.2: signal = "🔴 SELL (هبوط)"
                elif p_range < 0.002: signal = "⚠️ SQUEEZE (شحن)"
                else: signal = "📡 WATCH"

                results.append({
                    "العملة": sym.replace("-USD", ""),
                    "السعر": f"{curr_p:.6f}" if curr_p < 1 else f"{curr_p:.2f}",
                    "تغير لحظي %": round(change_2m, 3),
                    "الإشارة": signal
                })

            df = pd.DataFrame(results)

            with placeholder.container():
                # --- القسم العلوي: الـ 100 جنيه ---
                target_data = ticker.Ticker(asset_input).fast_info
                live_price = target_data['last_price']
                val_egp = ((2.0 / buy_p) * live_price) * 50 if buy_p > 0 else 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric(f"قيمة الـ 100ج ({asset_input})", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("نبض السوق", f"{time.strftime('%H:%M:%S')}")
                c3.metric("الحالة العامة", "✅ متصل لحظياً")

                st.write("---")
                
                # --- القسم الأوسط: الرسم البياني (خالد شارت) ---
                # تحديث 2026: width='stretch' بدل use_container_width
                hist = data[asset_input].tail(30)
                fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist.values, line=dict(color='#00ff00', width=3))])
                fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0), template="plotly_dark")
                st.plotly_chart(fig, width='stretch')

                # --- القسم السفلي: الجدول الملون ---
                def style_signal(val):
                    color = '#00ff00' if 'BUY' in val else '#ff0000' if 'SELL' in val else '#ffa500' if 'SQUEEZE' in val else 'white'
                    return f'color: {color}; font-weight: bold'

                st.table(df.style.applymap(style_signal, subset=['الإشارة']))

    except Exception as e:
        st.toast(f"جاري محاولة الربط السريع...", icon="🔄")
        time.sleep(2) # انتظار قليل جداً للمحاولة مرة تانية
        continue
    
    # تحديث كل 5 ثواني (أقصى سرعة مسموحة بدون حظر)
    time.sleep(5)
