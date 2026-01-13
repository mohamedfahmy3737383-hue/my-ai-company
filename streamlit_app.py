import streamlit as st
import pandas as pd
import yfinance as ticker
import time

st.set_page_config(page_title="Crypto Signal Pro", layout="wide")

st.title("🎯 رادار القناص: نظام الإشارات الذكي")

# 💰 إعدادات المحفظة
st.sidebar.title("💰 شركة الـ 100 جنيه")
asset_input = st.sidebar.text_input("رمز العملة للمتابعة (مثلاً CHZ-USD):", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=0.1500, format="%.4f")

crypto_watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD', 'SHIB-USD', 'PEPE24478-USD', 'BONK-USD']

placeholder = st.empty()

while True:
    try:
        # جلب البيانات (آخر ساعة بفاصل دقيقة واحدة)
        data = ticker.download(crypto_watchlist, period="1d", interval="1m", progress=False)['Close']
        
        if not data.empty:
            results = []
            data = data.fillna(method='ffill')
            
            for sym in crypto_watchlist:
                prices = data[sym]
                curr_p = prices.iloc[-1]
                # حساب المتوسط المتحرك (إشارة بسيطة للاتجاه)
                sma = prices.tail(10).mean() 
                change = ((curr_p - prices.iloc[-10]) / prices.iloc[-10]) * 100
                
                # منطق الإشارات الذكي
                if change > 0.4 and curr_p > sma:
                    signal = "🟢 شراء (Buy)"
                    action_color = "green"
                elif change < -0.3 or (curr_p < sma and change < 0):
                    signal = "🔴 بيع (Sell)"
                    action_color = "red"
                else:
                    signal = "📡 مراقبة"
                    action_color = "white"

                results.append({
                    "العملة": sym.replace("-USD", ""),
                    "السعر ($)": f"{curr_p:.8f}" if curr_p < 0.1 else f"{curr_p:.4f}",
                    "الحركة %": round(change, 3),
                    "الإشارة": signal
                })

            df = pd.DataFrame(results)

            with placeholder.container():
                # حساب قيمة الـ 100 جنيه
                try:
                    live_info = ticker.Ticker(asset_input).fast_info['last_price']
                    val_egp = ((2.0 / buy_p) * live_info) * 50 if buy_p > 0 else 100
                except: val_egp = 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric(f"قيمة الـ 100ج في {asset_input}", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("نبض السوق", "🔥 نشط جداً" if abs(df['الحركة %'].max()) > 0.5 else "🟢 مستقر")
                c3.metric("توقيت", time.strftime('%H:%M:%S'))

                st.write("---")
                st.subheader("📊 رادار الإشارات اللحظي")
                
                # تنسيق الجدول بالألوان
                def style_signals(row):
                    color = 'background-color: #004400' if "شراء" in row['الإشارة'] else \
                            'background-color: #440000' if "بيع" in row['الإشارة'] else ''
                    return [color] * len(row)

                st.table(df.style.apply(style_signals, axis=1))

                # تنبيه صوتي لو ظهرت إشارة شراء لعملتك المفضلة
                if any(df[df['العملة'] == asset_input.replace("-USD", "")]['الإشارة'].str.contains("شراء")):
                    st.toast(f"🚀 فرصة دخول في {asset_input}!", icon="💰")
                    
    except Exception as e:
        st.info("🔄 تحديث نظام الإشارات...")
    
    time.sleep(15)
