import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="AI Arbitrage Radar", layout="wide")
st.title("🚀 رادار صيد فرص المراجحة - النسخة السريعة")

# دالة بسيطة جداً لسحب الأسعار من غير تعقيد
def get_price(symbol):
    try:
        # هنجيب السعر من منصة Binance و MEXC و GateIO عبر API عام وسريع
        urls = {
            'Binance': f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.replace('/', '')}",
            'MEXC': f"https://www.mexc.com/open/api/v2/market/ticker?symbol={symbol.replace('/', '_')}"
        }
        prices = {}
        for name, url in urls.items():
            res = requests.get(url, timeout=5).json()
            if name == 'Binance': prices[name] = float(res['price'])
            if name == 'MEXC': prices[name] = float(res['data'][0]['last'])
        return prices
    except:
        return None

symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT']
placeholder = st.empty()

while True:
    data = []
    with st.spinner('جاري قنص الأسعار...'):
        for sym in symbols:
            prices = get_price(sym)
            if prices and len(prices) > 1:
                p_list = list(prices.values())
                min_p, max_p = min(p_list), max_p(p_list)
                diff = ((max_p - min_p) / min_p) * 100
                data.append({"العملة": sym, "أقل سعر": min_p, "أعلى سعر": max_p, "الفرق %": round(diff, 3)})
    
    if data:
        with placeholder.container():
            st.success(f"✅ الرادار يعمل بكفاءة - تحديث: {time.strftime('%H:%M:%S')}")
            df = pd.DataFrame(data)
            
            # عرض كروت سريعة للتابلت
            cols = st.columns(len(data))
            for i, row in df.iterrows():
                cols[i].metric(row['العملة'], f"{row['الفرق %']}%")
            
            st.table(df)
    else:
        st.error("⚠️ السيرفر يحاول تجاوز حماية المنصة.. انتظر ثواني")
    
    time.sleep(10)
