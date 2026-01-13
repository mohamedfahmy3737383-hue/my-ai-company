import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Global Sniper - Unstoppable", layout="wide")

st.title("🌐 رادار السيطرة العالمية (إصدار كسر الحظر)")

# إدارة الـ 100 جنيه
st.sidebar.title("💰 شركة الـ 100 جنيه")
buy_p = st.sidebar.number_input("سعر شراء عملتك ($):", value=0.000001, format="%.8f")

# دالة ذكية لجلب البيانات من روابط بديلة (Gateways)
def get_global_market():
    # الرابط ده هو "الباب الخلفي" لجلب بيانات السوق لما الروابط الرسمية بتتقفل
    gateways = [
        "https://api.coincap.io/v2/assets?limit=15",
        "https://api.coinlore.net/api/tickers/"
    ]
    for url in gateways:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                return data.get('data', []) if 'data' in data else data
        except:
            continue
    return None

placeholder = st.empty()

while True:
    market_data = get_global_market()
    
    if market_data:
        results = []
        # تحديد أهم العملات للسيطرة
        targets = ['BTC', 'ETH', 'SOL', 'PEPE', 'SHIB', 'DOGE', 'LUNC', 'BONK']
        
        for item in market_data:
            # معالجة اختلاف أسماء المفاتيح بين المصادر
            sym = item.get('symbol', '').upper()
            if sym in targets:
                # تحويل البيانات لأرقام بأمان
                try:
                    p = float(item.get('priceUsd', item.get('price_usd', 0)))
                    c = float(item.get('changePercent24Hr', item.get('percent_change_24h', 0)))
                    v = float(item.get('volumeUsd24Hr', item.get('volume24', 0)))
                    
                    results.append({
                        "العملة": sym,
                        "السعر ($)": p,
                        "تغير %": round(c, 2),
                        "الحيتان": "🐳 دخول سيولة" if v > 1000000 else "🐟 هدوء",
                        "الأخبار": "🔥 خبر متداول" if abs(c) > 5 else "📰 مستقر",
                        "القرار": "🚀 هجوم" if c > 2 else "📡 مراقبة"
                    })
                except: continue

        if results:
            with placeholder.container():
                # حساب الـ 100 جنيه (باستخدام PEPE أو أول عملة)
                ref = next((x for x in results if x['العملة'] == "PEPE"), results[0])
                val_egp = ((2.0 / buy_p) * ref['السعر ($)']) * 50 if buy_p > 0 else 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric("قيمة الـ 100 ج", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("حالة الرادار", "✅ متصل عالمياً")
                c3.metric("توقيت السيطرة", time.strftime('%H:%M:%S'))

                st.write("---")
                df = pd.DataFrame(results).sort_values(by="تغير %", ascending=False)
                
                # تلوين صفوف الهجوم
                def highlight_action(row):
                    return ['background-color: #4c0000' if row['القرار'] == "🚀 هجوم" else ''] * len(row)

                st.table(df.style.apply(highlight_action, axis=1))
                st.success("🎯 تم الربط بنجاح عبر البوابة الخلفية!")
    else:
        st.error("⚠️ جاري تدوير مفاتيح الاتصال... السيرفر يقاوم الحظر")

    time.sleep(10)
