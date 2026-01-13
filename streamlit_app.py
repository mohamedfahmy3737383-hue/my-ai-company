import streamlit as st
import pandas as pd
import yfinance as ticker
import time

st.set_page_config(page_title="Crypto Sniper Elite", layout="wide")

st.title("🏛️ مركز قيادة الإمبراطورية: الإشارات والتوقعات")

# 💰 إدارة المحفظة
st.sidebar.title("💰 شركة الـ 100 جنيه")
asset_input = st.sidebar.text_input("رمز العملة للمتابعة (مثلاً CHZ-USD):", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=0.1500, format="%.4f")

crypto_watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD', 'SHIB-USD', 'PEPE24478-USD', 'BONK-USD']

placeholder = st.empty()

while True:
    try:
        # جلب البيانات لآخر 60 دقيقة
        data = ticker.download(crypto_watchlist, period="1d", interval="1m", progress=False)['Close']
        
        if not data.empty:
            results = []
            data = data.ffill().bfill()
            
            for sym in crypto_watchlist:
                prices = data[sym]
                curr_p = prices.iloc[-1]
                prev_p_5 = prices.iloc[-5] # سعر قبل 5 دقائق
                sma_20 = prices.tail(20).mean()
                
                # 1. حساب كاشف الانفجار (Squeeze)
                price_range = (prices.tail(20).max() - prices.tail(20).min()) / prices.tail(20).mean()
                is_squeezing = price_range < 0.0025 # نطاق ضيق جداً
                
                # 2. منطق الإشارات (Buy/Sell)
                change_5m = ((curr_p - prev_p_5) / prev_p_5) * 100
                
                if change_5m > 0.35 and curr_p > sma_20:
                    signal = "🟢 شراء (BUY)"
                elif change_5m < -0.30 or (curr_p < sma_20 and change_5m < 0):
                    signal = "🔴 بيع (SELL)"
                elif is_squeezing:
                    signal = "⚠️ شحن (انفجار قريب)"
                else:
                    signal = "📡 مراقبة"

                results.append({
                    "العملة": sym.replace("-USD", ""),
                    "السعر ($)": f"{curr_p:.8f}" if curr_p < 0.1 else f"{curr_p:.4f}",
                    "تغير 5د %": round(change_5m, 3),
                    "الإشارة / الحالة": signal
                })

            df = pd.DataFrame(results)

            with placeholder.container():
                # حساب الـ 100 جنيه
                try:
                    live_info = ticker.Ticker(asset_input).fast_info['last_price']
                    val_egp = ((2.0 / buy_p) * live_info) * 50 if buy_p > 0 else 100
                except: val_egp = 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric(f"قيمة الـ 100ج في {asset_input}", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("فرص السوق", f"{len(df[df['الإشارة / الحالة'].str.contains('شراء')])} فرصة دخول")
                c3.metric("توقيت السيطرة", time.strftime('%H:%M:%S'))

                st.write("---")
                
                # تنسيق الجدول بالألوان لتسهيل القنص
                def color_signals(val):
                    if "BUY" in val: color = '#00ff00' # أخضر فسفوري
                    elif "SELL" in val: color = '#ff0000' # أحمر
                    elif "شحن" in val: color = '#ffa500' # برتقالي
                    else: color = 'white'
                    return f'color: {color}; font-weight: bold'

                st.table(df.style.applymap(color_signals, subset=['الإشارة / الحالة']))

                # تنبيهات ذكية
                if "🟢 شراء (BUY)" in df['الإشارة / الحالة'].values:
                    st.toast("🚀 تم رصد إشارة دخول قوية!", icon="💰")
                if "⚠️ شحن" in df['الإشارة / الحالة'].values:
                    st.toast("⚠️ عملة تستعد للانفجار..", icon="⚡")

    except Exception as e:
        pass 
    
    time.sleep(12)
