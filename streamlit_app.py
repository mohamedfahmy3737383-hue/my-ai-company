import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Opportunity Seeker PRO", layout="wide")

st.title("🏹 رادار قنص الفرص النادرة")
st.write("الرادار الآن يبحث في 'أعماق السوق' عن أي حركة مخفية للـ 100 جنيه")

def fetch_all():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    data = fetch_all()
    if data:
        # أضفنا عملات أكتر عشان "لازم" نلاقي فرصة
        targets = [
            'PEPEUSDT', 'SHIBUSDT', 'BONKUSDT', 'FLOKIUSDT', 'LUNCUSDT', 
            '1000SATSUSDT', 'RATSUSDT', 'TURBOUSDT', 'MEMEUSDT', 'PEOPLEUSDT'
        ]
        results = []
        
        for item in data:
            if item['symbol'] in targets:
                symbol = item['symbol'].replace("USDT", "")
                price = float(item['lastPrice'])
                change = float(item['priceChangePercent'])
                vol = float(item['quoteVolume'])
                
                # معادلة "الزخم الخفي" - بتكشف الحركة حتى لو السعر لسه منطلقش قوي
                momentum = (abs(change) * 2) + (vol / 1000000)
                
                if change > 0.5 and vol > 500000:
                    status = "✅ بداية تسخين"
                elif change > 3:
                    status = "🚀 انطلاق"
                else:
                    status = "💤 انتظار"

                results.append({
                    "العملة": symbol,
                    "السعر": f"${price:.8f}",
                    "قوة الحركة": round(momentum, 2),
                    "الوضع": status
                })

        with placeholder.container():
            # رتّب الجدول بحيث "أقوى" عملة تكون فوق دايماً
            df = pd.DataFrame(results).sort_values(by="قوة الحركة", ascending=False)
            
            st.subheader("📊 ترتيب العملات حسب 'الأقوى' الآن")
            
            def style_status(val):
                if "انطلاق" in val: return 'background-color: #900c3f; color: white'
                if "تسخين" in val: return 'background-color: #1d4e89; color: white'
                return ''

            st.table(df.style.applymap(style_status, subset=['الوضع']))
            
            # نصيحة لو مفيش هجوم
            if not any(x in ["🚀 انطلاق", "✅ بداية تسخين"] for x in df['الوضع']):
                st.warning("⚠️ السوق هادئ جداً الآن. لا تخاطر بالـ 100 جنيه، انتظر 'بداية تسخين' على الأقل.")
            else:
                st.balloons() # احتفال بسيط لو فيه انطلاق

    time.sleep(5)
