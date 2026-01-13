import streamlit as st
import pandas as pd
import yfinance as ticker
import time
import plotly.graph_objects as go

# 1. إعدادات 2026 المستقرة
st.set_page_config(page_title="Empire Stable Pro", layout="wide")

st.title("🏛️ رادار الإمبراطورية (نسخة الاستقرار القصوى)")
st.write(f"⚙️ الحالة: متصل ومستقر | التوقيت الحالي: {time.strftime('%H:%M:%S')}")

# 2. مكتب المدير العام
st.sidebar.title("👤 مكتب المدير العام")
asset_input = st.sidebar.text_input("العملة للمتابعة:", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=0.1500, format="%.4f")

# القائمة الذهبية (الأكثر استقراراً في ياهو فاينانس)
watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD']

placeholder = st.empty()

while True:
    try:
        # جلب البيانات بهدوء لضمان عدم الحظر
        # طلبنا البيانات لآخر ساعتين فقط لتقليل الحجم
        data = ticker.download(watchlist, period="1d", interval="2m", progress=False)['Close']
        
        if not data.empty:
            data = data.ffill().bfill()
            results = []
            
            for sym in watchlist:
                prices = data[sym]
                curr_p = prices.iloc[-1]
                # حساب التغير في آخر 10 دقائق
                change = ((curr_p - prices.iloc[-5]) / prices.iloc[-5]) * 100 if len(prices) > 5 else 0
                
                # إشارات القناص
                if change > 0.3: signal = "🟢 شراء (BUY)"
                elif change < -0.3: signal = "🔴 بيع (SELL)"
                else: signal = "📡 مراقبة"

                results.append({
                    "العملة": sym.replace("-USD", ""),
                    "السعر": f"{curr_p:.4f}",
                    "نبض 10د %": round(change, 3),
                    "الإشارة": signal
                })

            df = pd.DataFrame(results)

            with placeholder.container():
                # --- المقاييس ---
                c1, c2, c3 = st.columns(3)
                
                # حساب الـ 100 جنيه
                target_p = ticker.Ticker(asset_input).fast_info['last_price']
                val_egp = ((2.0 / buy_p) * target_p) * 50 if buy_p > 0 else 100
                
                c1.metric(f"قيمة الـ 100ج ({asset_input})", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("حالة الموظفين", "✅ مستقر")
                c3.metric("تحديث الرادار", time.strftime('%H:%M:%S'))

                st.write("---")
                
                # --- خالد شارت (بصيغة 2026) ---
                st.subheader(f"📈 حركة {asset_input} اللحظية")
                hist = data[asset_input].tail(30)
                fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist.values, line=dict(color='#00ff00', width=2))])
                fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), template="plotly_dark")
                st.plotly_chart(fig, width='stretch')

                # الجدول الملون
                def style_df(val):
                    color = '#00ff00' if 'شراء' in val else '#ff0000' if 'بيع' in val else 'white'
                    return f'color: {color}; font-weight: bold'
                
                st.table(df.style.applymap(style_df, subset=['الإشارة']))

    except Exception as e:
        # لو حصل حظر مؤقت، السيستم يهدأ لوحده
        st.warning("⚠️ البورصة مضغوطة.. هريح 30 ثانية وأرجع لك.")
        time.sleep(30)
        continue
    
    # السرعة الآمنة لمنع رسائل "جاري الربط"
    time.sleep(20)
