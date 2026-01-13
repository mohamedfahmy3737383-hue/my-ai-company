import streamlit as st
import pandas as pd
import yfinance as yf # مكتبة قوية جداً ومستقرة
import time

st.set_page_config(page_title="AI Arbitrage Radar", layout="wide")
st.title("🚀 رادار الأسعار العالمي")

# قائمة العملات اللي هنراقبها (بصيغة ياهو فاينانس)
symbols = {
    'BTC/USDT': 'BTC-USD',
    'ETH/USDT': 'ETH-USD',
    'SOL/USDT': 'SOL-USD',
    'XRP/USDT': 'XRP-USD'
}

placeholder = st.empty()

while True:
    data = []
    with st.spinner('جاري سحب البيانات من القمر الصناعي...'):
        for name, ticker in symbols.items():
            try:
                # سحب بيانات العملة
                crypto = yf.Ticker(ticker)
                price = crypto.fast_info['lastPrice']
                
                # إحنا هنا هنقارن السعر اللحظي بمتوسط اليوم عشان نطلع "نسبة تغير"
                # دي كبداية لحد ما نفتح الحظر عن المنصات التانية
                data.append({
                    "العملة": name,
                    "السعر اللحظي": f"${price:,.2f}",
                    "الحالة": "✅ متصل"
                })
            except:
                continue

    if data:
        with placeholder.container():
            st.success(f"📡 الرادار متصل الآن - تحديث: {time.strftime('%H:%M:%S')}")
            df = pd.DataFrame(data)
            
            # عرض البيانات بشكل كروت احترافية
            cols = st.columns(len(data))
            for i, row in df.iterrows():
                cols[i].metric(row['العملة'], row['السعر اللحظي'])
            
            st.divider()
            st.write("### 📈 جدول المراقبة اللحظي")
            st.table(df)
    else:
        st.error("🔄 السيرفر يحاول الاتصال.. تأكد من تحديث الصفحة")
    
    time.sleep(10)
