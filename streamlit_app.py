import streamlit as st
import pandas as pd
import requests
import time

# إعداد واجهة احترافية
st.set_page_config(page_title="AI Crypto Hunter", layout="wide")

# CSS لتحسين شكل الجدول والكروت
st.markdown("""
    <style>
    .stDataFrame { border-radius: 15px; overflow: hidden; }
    .status-box { padding: 20px; border-radius: 10px; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 صائد الفرص الذكي - MEXC Pro")

# دالة جلب البيانات
def get_data():
    url = "https://api.mexc.com/api/v3/ticker/bookTicker"
    try:
        res = requests.get(url, timeout=5).json()
        return res
    except:
        return None

placeholder = st.empty()

while True:
    raw_data = get_data()
    if raw_data:
        targets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'DOTUSDT', 'DOGEUSDT']
        final_list = []

        for item in raw_data:
            if item['symbol'] in targets:
                bid = float(item['bidPrice'])
                ask = float(item['askPrice'])
                # الفارق بين السعرين
                spread = ((ask - bid) / bid) * 100
                # صافي الربح بعد خصم عمولة البيع والشراء (0.2% إجمالي)
                net = spread - 0.2
                
                # تحديد القرار
                if net > 0:
                    action = "✅ فرصة ربح!"
                elif net > -0.1:
                    action = "⏳ مراقبة"
                else:
                    action = "❌ لا توجد فائدة"

                final_list.append({
                    "العملة": item['symbol'].replace("USDT", ""),
                    "سعر الشراء 🟢": f"${bid:,.4f}",
                    "سعر البيع 🔴": f"${ask:,.4f}",
                    "الفارق (Spread)": f"{spread:.3f}%",
                    "صافي الربح 💰": f"{net:.3f}%",
                    "القرار": action
                })

        with placeholder.container():
            # كروت علوية سريعة
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("حالة الرادار", "نشط 🛰️", delta="متصل بـ API")
            with c2:
                st.metric("آخر تحديث", time.strftime('%H:%M:%S'))
            with c3:
                # إيجاد أعلى ربح متاح
                top_profit = max([float(x['صافي الربح 💰'].replace('%','')) for x in final_list])
                st.metric("أعلى فرصة حالية", f"{top_profit}%")

            st.divider()

            # عرض الجدول بتنسيق احترافي
            df = pd.DataFrame(final_list)
            
            def style_action(val):
                if "ربح" in val: color = '#28a745'
                elif "مراقبة" in val: color = '#ffc107'
                else: color = '#dc3545'
                return f'color: white; background-color: {color}; font-weight: bold; text-align: center;'

            st.write("### 📊 قائمة المراقبة المباشرة")
            st.table(df.style.applymap(style_action, subset=['القرار']))
            
            # تشغيل تنبيه بسيط لو فيه ربح
            if top_profit > 0:
                st.toast(f"تم اكتشاف فرصة بربح {top_profit}%", icon='🔥')
                
    time.sleep(5)
