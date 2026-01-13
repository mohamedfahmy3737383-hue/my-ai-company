import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Whale Hunter Radar 🐋", layout="wide")

def get_mexc_stats():
    # جلب بيانات الأسعار والحجم معاً
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

st.title("🐋 رادار كشف الحيتان والعملات الرخيصة")
st.write("رأس المال: 100 جنيه | الهدف: قنص السيولة العالية")

placeholder = st.empty()

while True:
    stats_data = get_mexc_stats()
    if stats_data:
        targets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'PEPEUSDT', 'SHIBUSDT', 'FLOKIUSDT', 'BONKUSDT', 'LUNCUSDT', 'GALAUSDT']
        final_list = []

        for item in stats_data:
            if item['symbol'] in targets:
                price = float(item['lastPrice'])
                volume = float(item['quoteVolume']) # حجم التداول بالدولار
                change = float(item['priceChangePercent'])
                
                # تصنيف قوة الحيتان
                if volume > 10000000: whale_status = "🐳 حيتان ضخمة"
                elif volume > 1000000: whale_status = "🐬 حركة قوية"
                else: whale_status = "🐟 حركة هادئة"

                final_list.append({
                    "العملة": item['symbol'].replace("USDT", ""),
                    "السعر الحالي": f"${price:.8f}",
                    "تغير 24س": f"{change}%",
                    "السيولة ($)": f"${volume:,.0f}",
                    "قوة الحيتان": whale_status
                })

        with placeholder.container():
            df = pd.DataFrame(final_list)
            
            # كروت ملخصة
            c1, c2 = st.columns(2)
            top_vol = df.loc[df['السيولة ($)'].replace('$', '').replace(',', '', regex=True).astype(float).idxmax()]
            c1.metric("أعلى سيولة الآن", top_vol['العملة'], top_vol['السيولة ($)'])
            c2.metric("توقيت الرادار", time.strftime('%H:%M:%S'))

            st.write("### 📊 جدول المراقبة ودخول السيولة")
            
            def color_whale(val):
                if "🐳" in val: return 'background-color: #0d47a1; color: white'
                if "🐬" in val: return 'background-color: #00838f; color: white'
                return ''

            st.table(df.style.applymap(color_whale, subset=['قوة الحيتان']))
            
            if "🐳" in df['قوة الحيتان'].values:
                st.toast("انتباه: حيتان تتحرك في السوق الآن!", icon="🚨")

    time.sleep(10)
