import streamlit as st
import ccxt
import pandas as pd
import time

st.set_page_config(page_title="AI Arbitrage Radar", layout="wide")
st.title("🚀 رادار صيد فرص المراجحة")

# تعريف المنصات
@st.cache_resource
def get_exchanges():
    return {
        'KuCoin': ccxt.kucoin(),
        'Gate.io': ccxt.gateio(),
        'Bybit': ccxt.bybit()
    }

exchanges = get_exchanges()
symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'AVAX/USDT']

placeholder = st.empty()

while True:
    data = []
    for symbol in symbols:
        try:
            prices = {}
            for name, ex in exchanges.items():
                ticker = ex.fetch_ticker(symbol)
                prices[name] = ticker['last']
            
            max_p = max(prices.values())
            min_p = min(prices.values())
            diff = ((max_p - min_p) / min_p) * 100
            
            data.append({
                "العملة": symbol,
                "أقل سعر": f"${min_p:,.2f}",
                "أعلى سعر": f"${max_p:,.2f}",
                "الفرق %": round(diff, 3)
            })
        except Exception as e:
            continue

    if data:
        df = pd.DataFrame(data)
        with placeholder.container():
            st.write("### 📊 لوحة الفرص اللحظية")
            
            # عرض العملات كـ "بطاقات" تحت بعض عشان شاشة التابلت
            for item in data:
                diff_val = item['الفرق %']
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric(item['العملة'], f"{diff_val}%")
                with col2:
                    if diff_val > 0.2:
                        st.success(f"🔥 فرصة قوية! الفرق بين المنصات هو {diff_val}%")
                    else:
                        st.info("🔎 مراقبة الأسعار.. لا يوجد فرق كبير حالياً.")
            
            st.divider()
            st.write("### 📝 جدول البيانات التفصيلي")
            st.table(df)
            st.caption(f"آخر تحديث: {time.strftime('%H:%M:%S')}")

    time.sleep(15) # تحديث كل 15 ثانية عشان المنصات متعملش Block
