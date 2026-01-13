import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Whale Hunter Pro 🐋", layout="wide")

st.title("🐋 رادار كشف الحيتان وتوقعات السوق")
st.write("رأس المال: 100 جنيه | نظام تحليل السيولة المتقدم")

def get_mexc_stats():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try:
        response = requests.get(url, timeout=5)
        return response.json()
    except:
        return None

placeholder = st.empty()

while True:
    stats_data = get_mexc_stats()
    if stats_data:
        # قائمة العملات المستهدفة (الكبيرة والرخيصة)
        targets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'PEPEUSDT', 'SHIBUSDT', 'FLOKIUSDT', 'BONKUSDT', 'LUNCUSDT', 'XRPUSDT']
        final_list = []

        for item in stats_data:
            if item['symbol'] in targets:
                price = float(item['lastPrice'])
                volume = float(item['quoteVolume'])
                change = float(item['priceChangePercent'])
                
                # ذكاء اصطناعي بسيط للتوقع بناءً على السعر والحجم
                if change > 0 and volume > 5000000:
                    prediction = "🚀 صعود مستمر"
                elif change < -5 and volume > 5000000:
                    prediction = "📉 هبوط حاد"
                elif change > 3:
                    prediction = "↗️ ارتداد إيجابي"
                else:
                    prediction = "➡️ استقرار"

                final_list.append({
                    "العملة": item['symbol'].replace("USDT", ""),
                    "السعر": f"${price:.8f}",
                    "تغير 24س": change,
                    "السيولة": volume,
                    "قوة الحيتان": "🐳 حيتان" if volume > 10000000 else "🐟 أفراد",
                    "توقع الذكاء": prediction
                })

        if final_list:
            df = pd.DataFrame(final_list)
            
            with placeholder.container():
                # كروت الإحصائيات (بدون أخطاء حسابية)
                c1, c2, c3 = st.columns(3)
                top_coin = df.iloc[df['السيولة'].idxmax()]
                c1.metric("أكثر عملة سيولة", top_coin['العملة'])
                c2.metric("حجم سيولتها", f"${top_coin['السيولة']:,.0f}")
                c3.metric("تحديث تلقائي", time.strftime('%H:%M:%S'))

                st.write("### 📊 لوحة تحكم الصياد")
                
                # تنسيق الجدول الملون
                def style_prediction(val):
                    if "🚀" in val: return 'color: #00ff00; font-weight: bold'
                    if "📉" in val: return 'color: #ff0000; font-weight: bold'
                    return ''

                # عرض الجدول بشكل احترافي
                display_df = df.copy()
                display_df['تغير 24س'] = display_df['تغير 24س'].map("{:.2f}%".format)
                display_df['السيولة'] = display_df['السيولة'].map("${:,.0f}".format)
                
                st.table(display_df.style.applymap(style_prediction, subset=['توقع الذكاء']))
                
                if "🚀" in df['توقع الذكاء'].values:
                    st.toast("تم رصد عملة تنطلق الآن!", icon="🔥")

    time.sleep(10)
