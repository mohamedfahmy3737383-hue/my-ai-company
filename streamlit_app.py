import streamlit as st
import pandas as pd
import yfinance as ticker
import time

# 1. إعدادات السيطرة
st.set_page_config(page_title="Global Sniper Elite", layout="wide")

st.title("🌐 رادار السيطرة العالمية (النسخة النووية)")
st.write("البيانات تتدفق الآن عبر أقوى سيرفرات البورصة العالمية")

# 2. إدارة محفظة الـ 100 جنيه
st.sidebar.title("💰 شركة الـ 100 جنيه")
asset_name = st.sidebar.text_input("اكتب اختصار عملتك (مثلاً CHZ-USD أو PEPE24478-USD):", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر شرائك بالدولار ($):", value=0.15, format="%.4f")

placeholder = st.empty()

# قائمة العملات اللي هنراقبها (أقوى عملات العالم)
watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD', 'SHIB-USD', 'PEPE24478-USD']

while True:
    try:
        # سحب البيانات من سيرفرات ياهو فاينانس (الأقوى عالمياً)
        data = ticker.download(watchlist, period="1d", interval="1m", progress=False)['Close']
        
        if not data.empty:
            results = []
            last_prices = data.iloc[-1]
            prev_prices = data.iloc[-5] if len(data) > 5 else data.iloc[0]
            
            for sym in watchlist:
                curr_p = float(last_prices[sym])
                old_p = float(prev_prices[sym])
                change = ((curr_p - old_p) / old_p) * 100
                
                results.append({
                    "العملة": sym.replace("-USD", ""),
                    "السعر ($)": f"{curr_p:.6f}" if curr_p < 1 else f"{curr_p:.2f}",
                    "تغير لحظي %": round(change, 2),
                    "القرار": "🚀 هجوم" if change > 0.5 else "📡 رصد"
                })

            df = pd.DataFrame(results)

            with placeholder.container():
                # حساب الأرباح (الـ 100 جنيه)
                # بنشوف سعر العملة اللي انت كاتبها في السايد بار
                try:
                    target_data = ticker.Ticker(asset_name).fast_info['last_price']
                    val_egp = ((2.0 / buy_p) * target_data) * 50 if buy_p > 0 else 100
                except:
                    val_egp = 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric(f"قيمة الـ 100ج في {asset_name}", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("حالة الربط", "✅ فولاذي")
                c3.metric("نبض السوق", time.strftime('%H:%M:%S'))

                st.write("---")
                st.subheader("📊 رادار الانفجارات اللحظي")
                st.table(df.sort_values(by="تغير لحظي %", ascending=False))
                
                if "🚀 هجوم" in df['القرار'].values:
                    st.warning("🔥 انتباه! فيه عملة بتنفجر دلوقتي، بص على الجدول!")
        
    except Exception as e:
        st.error(f"جاري إعادة الاتصال بالسيرفر النووي... {e}")

    time.sleep(20)
