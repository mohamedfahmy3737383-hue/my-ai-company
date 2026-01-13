import streamlit as st
import ccxt
import pandas as pd
import time

# إعداد الصفحة
st.set_page_config(page_title="AI Arbitrage Radar", layout="wide")
st.title("🚀 رادار صيد فرص المراجحة")

# تفعيل الربط مع المنصات
@st.cache_resource
def init_exchanges():
    return {
        'KuCoin': ccxt.kucoin(),
        'Gate.io': ccxt.gateio(),
        'Bybit': ccxt.bybit()
    }

exchanges = init_exchanges()
symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT']

placeholder = st.empty()

while True:
    all_data = []
    
    # رسالة تحميل بسيطة
    with st.spinner('جاري صيد الأسعار من المنصات...'):
        for symbol in symbols:
            try:
                prices = {}
                for name, ex in exchanges.items():
                    ticker = ex.fetch_ticker(symbol)
                    prices[name] = ticker['last']
                
                min_p = min(prices.values())
                max_p = max(prices.values())
                diff = ((max_p - min_p) / min_p) * 100
                
                all_data.append({
                    "العملة": symbol,
                    "أقل سعر": min_p,
                    "أعلى سعر": max_p,
                    "الفرق %": round(diff, 3)
                })
            except:
                continue

    # التأكد من وجود بيانات قبل الرسم لتجنب الخطأ اللي ظهرلك
    if len(all_data) > 0:
        df = pd.DataFrame(all_data)
        with placeholder.container():
            st.write("### 📊 الأسعار اللحظية")
            
            # عرض كل عملة في سطر منفصل (أضمن للتابلت وللكود)
            for _, row in df.iterrows():
                with st.expander(f"💰 {row['العملة']} - الفرق الحالي: {row['الفرق %']}%", expanded=True):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("أقل سعر", f"${row['أقل سعر']:,.2f}")
                    c2.metric("أعلى سعر", f"${row['أعلى سعر']:,.2f}")
                    c3.metric("الربح المتوقع", f"{row['الفرق %']}%")
            
            st.divider()
            st.caption(f"آخر تحديث للسيرفر: {time.strftime('%H:%M:%S')}")
    else:
        st.warning("⚠️ لم يتمكن الموظف الـ AI من سحب البيانات حالياً.. سيحاول مجدداً خلال ثواني.")

    time.sleep(20) # راحة للسيرفر
