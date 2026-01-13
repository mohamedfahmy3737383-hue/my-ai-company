import streamlit as st
import ccxt
import pandas as pd
import time

st.set_page_config(page_title="AI Arbitrage Radar", layout="wide")
st.title("🚀 رادار صيد فرص المراجحة")

@st.cache_resource
def init_exchanges():
    # استخدام منصات بديلة "أسهل" في الربط
    return {
        'MEXC': ccxt.mexc({'enableRateLimit': True}),
        'Bybit': ccxt.bybit({'enableRateLimit': True}),
        'OKX': ccxt.okx({'enableRateLimit': True})
    }

exchanges = init_exchanges()
# قللنا عدد العملات لـ 3 بس في البداية عشان نتأكد إن الاتصال تمام
symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']

placeholder = st.empty()

while True:
    all_data = []
    with st.spinner('جاري فحص السوق...'):
        for symbol in symbols:
            try:
                # محاولة سحب السعر بذكاء
                p_mexc = exchanges['MEXC'].fetch_ticker(symbol)['last']
                p_bybit = exchanges['Bybit'].fetch_ticker(symbol)['last']
                
                prices = {'MEXC': p_mexc, 'Bybit': p_bybit}
                min_p = min(prices.values())
                max_p = max(prices.values())
                diff = ((max_p - min_p) / min_p) * 100
                
                all_data.append({
                    "العملة": symbol,
                    "أقل سعر": min_p,
                    "أعلى سعر": max_p,
                    "الفرق %": round(diff, 3)
                })
                time.sleep(1) # استراحة ثانية بين كل عملة وعملة عشان ميتعملش بلوك
            except Exception as e:
                # لو عايز تشوف المشكلة إيه بالظبط فك السطر اللي جاي
                # st.error(f"Error fetching {symbol}: {e}")
                continue

    if len(all_data) > 0:
        df = pd.DataFrame(all_data)
        with placeholder.container():
            st.write(f"### 📊 تحديث لحظي ({time.strftime('%H:%M:%S')})")
            for _, row in df.iterrows():
                # تلوين الخلفية لو الفرق حلو
                color = "green" if row['الفرق %'] > 0.1 else "blue"
                st.info(f"**{row['العملة']}** | الفرق: **{row['الفرق %']}%** | السعر: {row['أقل سعر']} ➡️ {row['أعلى سعر']}")
            
            st.table(df)
    else:
        st.warning("🔄 جاري محاولة إعادة الاتصال بالبورصة... تأكد من استقرار الإنترنت.")

    time.sleep(15)
