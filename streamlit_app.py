import streamlit as st
import pandas as pd
import yfinance as ticker
import time
import numpy as np

st.set_page_config(page_title="Crypto Predictor Pro", layout="wide")

st.title("🔮 كاشف الانفجار القادم (Predictor)")

# 💰 إعدادات المحفظة
st.sidebar.title("💰 شركة الـ 100 جنيه")
asset_input = st.sidebar.text_input("العملة للمتابعة:", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك ($):", value=0.1500, format="%.4f")

crypto_watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD', 'PEPE24478-USD']

placeholder = st.empty()

while True:
    try:
        # جلب بيانات كافية للحسابات الفنية (آخر 100 دقيقة)
        data = ticker.download(crypto_watchlist, period="1d", interval="1m", progress=False)['Close']
        
        if not data.empty:
            results = []
            data = data.fillna(method='ffill')
            
            for sym in crypto_watchlist:
                prices = data[sym].tail(20) # آخر 20 دقيقة
                curr_p = prices.iloc[-1]
                
                # حساب النطاق (البولينجر) - قياس التذبذب
                std_dev = prices.std()
                sma = prices.mean()
                
                # كاشف الضغط (Squeeze): لو التذبذب قليل جداً يبقى فيه انفجار جاي
                is_squeezing = std_dev < (prices.mean() * 0.001) 
                
                # حساب التغير اللحظي
                change = ((curr_p - prices.iloc[0]) / prices.iloc[0]) * 100
                
                # تحديد الحالة
                if is_squeezing:
                    status = "⚠️ شحن (انفجار قريب)"
                    color = "orange"
                elif change > 0.4:
                    status = "🚀 هجوم مستمر"
                    color = "green"
                elif change < -0.4:
                    status = "📉 هبوط حاد"
                    color = "red"
                else:
                    status = "📡 هدوء"
                    color = "white"

                results.append({
                    "العملة": sym.replace("-USD", ""),
                    "السعر ($)": f"{curr_p:.6f}" if curr_p < 0.1 else f"{curr_p:.4f}",
                    "قوة التذبذب": round(std_dev, 6),
                    "الحالة": status
                })

            df = pd.DataFrame(results)

            with placeholder.container():
                # حساب الـ 100 جنيه
                live_price = ticker.Ticker(asset_input).fast_info['last_price']
                val_egp = ((2.0 / buy_p) * live_price) * 50 if buy_p > 0 else 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric(f"قيمة الـ 100ج في {asset_input}", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("تنبؤ النظام", "⚠️ ترقب انفجار" if "شحن" in df.values else "✅ مستقر")
                c3.metric("توقيت الرصد", time.strftime('%H:%M:%S'))

                st.write("---")
                st.subheader("📊 رادار التوقع اللحظي")
                st.table(df)

                # تنبيه خاص لو عملتك في حالة شحن
                target_sym = asset_input.replace("-USD", "")
                if any((df['العملة'] == target_sym) & (df['الحالة'].str.contains("شحن"))):
                    st.warning(f"📢 يا مدير! عملة {target_sym} دلوقتي في حالة 'شحن طاقة'.. الانفجار قرب!")

    except Exception as e:
        st.info("🔄 جاري تحديث الحسابات الفنية...")
    
    time.sleep(15)
