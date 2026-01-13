import streamlit as st
import pandas as pd
import yfinance as ticker
import time

# 1. إعدادات السيطرة
st.set_page_config(page_title="Crypto Sniper Only", layout="wide")

st.title("🎯 رادار قناص الكريبتو (السيطرة المطلقة)")
st.write("تم تصفية الرادار ليعرض فقط العملات الرقمية الأكثر اشتعالاً في العالم")

# 2. إدارة محفظة الـ 100 جنيه
st.sidebar.title("💰 شركة الـ 100 جنيه")
asset_name = st.sidebar.text_input("اكتب اختصار عملتك (مثلاً CHZ-USD):", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولك بالدولار ($):", value=0.1500, format="%.4f")

# قائمة العملات القناصة (أقوى 10 عملات فيها حركة)
crypto_watchlist = [
    'BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD', 
    'SHIB-USD', 'PEPE24478-USD', 'BONK-USD', 'LUNC-USD', 'FLOKI-USD'
]

placeholder = st.empty()

while True:
    try:
        # سحب بيانات الكريبتو فقط
        data = ticker.download(crypto_watchlist, period="1d", interval="1m", progress=False)['Close']
        
        if not data.empty:
            results = []
            last_prices = data.iloc[-1]
            prev_prices = data.iloc[-10] if len(data) > 10 else data.iloc[0] # مقارنة بآخر 10 دقائق
            
            for sym in crypto_watchlist:
                curr_p = float(last_prices[sym])
                old_p = float(prev_prices[sym])
                change = ((curr_p - old_p) / old_p) * 100
                
                results.append({
                    "العملة": sym.replace("-USD", ""),
                    "السعر ($)": f"{curr_p:.8f}" if curr_p < 1 else f"{curr_p:.2f}",
                    "نبض الـ 10 دقائق %": round(change, 3),
                    "القرار": "🚀 هجوم" if change > 0.3 else "📡 رصد"
                })

            df = pd.DataFrame(results)

            with placeholder.container():
                # حساب الأرباح الدقيقة للـ 100 جنيه
                try:
                    live_price = ticker.Ticker(asset_name).fast_info['last_price']
                    val_egp = ((2.0 / buy_p) * live_price) * 50
                except: val_egp = 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric(f"قيمة الـ 100ج في {asset_name}", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("حالة الرادار", "🟢 متصل بالبورصة")
                c3.metric("توقيت السيطرة", time.strftime('%H:%M:%S'))

                st.write("---")
                st.subheader("📊 جدول اقتناص الصواريخ الرقمية")
                
                # تلوين الجدول لسهولة الرصد
                def color_decision(val):
                    color = '#ff4b4b' if val == "🚀 هجوم" else 'white'
                    return f'color: {color}; font-weight: bold'

                st.table(df.style.applymap(color_decision, subset=['القرار']))

                if "🚀 هجوم" in df['القرار'].values:
                    st.toast("🚨 هجوم سيولة تم رصده الآن!", icon='🔥')
        
    except Exception as e:
        st.error(f"محاولة إعادة الاتصال بمحرك الكريبتو... {e}")

    time.sleep(15)
