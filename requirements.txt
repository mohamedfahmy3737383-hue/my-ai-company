import streamlit as st
import ccxt
import pandas as pd
import time

st.set_page_config(page_title="AI Arbitrage Radar", layout="wide")
st.title("🚀 رادار صيد فرص المراجحة")

# تعريف المنصات
exchanges = {
    'KuCoin': ccxt.kucoin(),
    'Gate.io': ccxt.gateio(),
    'Bybit': ccxt.bybit()
}

symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'AVAX/USDT']

# مكان عرض البيانات
placeholder = st.empty()

while True:
    data = []
    for symbol in symbols:
        try:
            prices = {}
            for name, ex in exchanges.items():
                prices[name] = ex.fetch_ticker(symbol)['last']
            
            # حساب أعلى وأقل سعر بين المنصات
            max_p = max(prices.values())
            min_p = min(prices.values())
            diff = ((max_p - min_p) / min_p) * 100
            
            data.append({
                "العملة": symbol,
                "أقل سعر": min_p,
                "أعلى سعر": max_p,
                "الفرق %": round(diff, 3)
            })
        except:
            continue

    df = pd.DataFrame(data)

    with placeholder.container():
        # عرض "كروت" للفرص القوية
        cols = st.columns(len(data))
        for i, row in df.iterrows():
            color = "green" if row['الفرق %'] > 0.3 else "normal"
            cols[i].metric(row['العملة'], f"{row['الفرق %']}%", delta=f"{row['الفرق %']}%", delta_color=color)
        
        st.write("### جدول التفاصيل اللحظي")
        st.table(df)
        st.write(f"آخر تحديث: {time.strftime('%H:%M:%S')}")

    time.sleep(10) # تحديث كل 10 ثواني
