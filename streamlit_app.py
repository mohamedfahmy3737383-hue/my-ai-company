import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="AI Arbitrage Pro", layout="wide")

# تصميم الواجهة بشكل احترافي
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 صائد فرص المراجحة الذكي")
st.write("الرادار يقوم الآن بمسح السوق العالمي وحساب العمولات")

symbols = {
    'Bitcoin': 'BTC-USD',
    'Ethereum': 'ETH-USD',
    'Solana': 'SOL-USD',
    'Ripple': 'XRP-USD',
    'Cardano': 'ADA-USD'
}

placeholder = st.empty()

while True:
    all_data = []
    with st.spinner('جاري تحليل موجات السوق...'):
        for name, ticker in symbols.items():
            try:
                crypto = yf.Ticker(ticker)
                info = crypto.fast_info
                current_price = info['lastPrice']
                high_24h = info['dayHigh']
                low_24h = info['dayLow']
                
                # حساب فرق السعر الافتراضي (بين أقل وأعلى سعر اليوم)
                diff = ((high_24h - low_24h) / low_24h) * 100
                
                # حساب صافي الربح بعد عمولة افتراضية 0.2%
                net_profit = diff - 0.2
                
                all_data.append({
                    "العملة": name,
                    "السعر الحالي": f"${current_price:,.2f}",
                    "تذبذب اليوم": f"{diff:.2f}%",
                    "الربح المتوقع": f"{net_profit:.2f}%",
                    "الحالة": "🔥 فرصة قوية" if net_profit > 1.5 else "⏳ مراقبة"
                })
            except:
                continue

    if all_data:
        with placeholder.container():
            # عرض كروت سريعة فوق
            cols = st.columns(len(all_data))
            for i, item in enumerate(all_data):
                color = "normal" if "مراقبة" in item['الحالة'] else "inverse"
                cols[i].metric(item['العملة'], item['السعر الحالي'], item['الربح المتوقع'], delta_color=color)
            
            st.divider()
            
            # عرض الجدول الملون
            df = pd.DataFrame(all_data)
            def color_status(val):
                color = '#155724' if 'فرصة' in val else '#721c24'
                return f'background-color: {color}; color: white'
            
            st.write("### 🔍 تفاصيل الفرص المكتشفة")
            st.table(df.style.applymap(color_status, subset=['الحالة']))
            
            st.caption(f"تحديث تلقائي كل 10 ثوانٍ | التوقيت الحالي: {time.strftime('%H:%M:%S')}")
    
    time.sleep(10)
