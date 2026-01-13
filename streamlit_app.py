import streamlit as st
import pandas as pd
import requests
import time

# 1. إعدادات السيطرة العالمية
st.set_page_config(page_title="Global Sniper V6", layout="wide")

# تهيئة الذاكرة
if 'prev_v' not in st.session_state: st.session_state.prev_v = {}
if 'last_signals' not in st.session_state: st.session_state.last_signals = {}

st.title("🌐 رادار السيطرة الشاملة (النسخة المحمية)")

# 2. إدارة المحفظة
st.sidebar.title("💰 شركة الـ 100 جنيه")
buy_p = st.sidebar.number_input("سعر شراء عملتك ($):", value=0.000001, format="%.8f")

def get_market_data():
    try:
        # استخدام رابط بديل وسريع
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

placeholder = st.empty()

while True:
    data = get_market_data()
    
    # حماية: التأكد أن البيانات عبارة عن قائمة (List) وليست نصاً أو خطأ
    if data and isinstance(data, list):
        targets = ['BTCUSDT', 'SOLUSDT', 'XRPUSDT', 'PEPEUSDT', 'SHIBUSDT', 'BONKUSDT', 'FLOKIUSDT', '1000SATSUSDT', 'LUNCUSDT', 'DOGEUSDT']
        results = []
        current_time = time.time()
        
        for item in data:
            # حماية إضافية: التأكد أن كل عنصر هو قاموس (Dict)
            if isinstance(item, dict) and item.get('symbol') in targets:
                sym = item['symbol']
                p = float(item.get('lastPrice', 0))
                c = float(item.get('priceChangePercent', 0))
                v = float(item.get('quoteVolume', 0))
                
                # حساب تدفق السيولة
                old_v = st.session_state.prev_v.get(sym, v)
                flow = v - old_v
                st.session_state.prev_v[sym] = v
                
                # كاشف الحيتان والأخبار
                whale = "🐳 حوت ضخم" if flow > 50000 else "🐟 أفراد"
                news = "🔥 انفجار" if c > 7 else "📈 صعود" if c > 2 else "📰 مستقر"
                
                # قوة السيطرة (Power Score)
                score = (c * 5) + (flow / 2000)
                
                if score > 35: st.session_state.last_signals[sym] = current_time
                active = sym in st.session_state.last_signals and (current_time - st.session_state.last_signals[sym] < 60)

                results.append({
                    "العملة": sym.replace("USDT",""),
                    "السعر": f"{p:.8f}" if p < 1 else f"{p:,.2f}",
                    "تغير%": c,
                    "تدفق ($)": round(flow, 2),
                    "الحيتان": whale,
                    "الأخبار": news,
                    "الأمر": "🚀 هجوم" if active else "📡 مراقبة"
                })
        
        if results:
            with placeholder.container():
                # حساب الـ 100 جنيه (باستخدام أول عملة متاحة كمرجع)
                ref_coin = results[0]
                curr_p = float(ref_coin['السعر'].replace(',',''))
                val_egp = ((2.0 / buy_p) * curr_p) * 50 if buy_p > 0 else 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric("قيمة الـ 100ج الآن", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("أقوى سيولة دخلت", f"${max([x['تدفق ($)'] for x in results]):,.0f}")
                c3.metric("تحديث الرادار", time.strftime('%H:%M:%S'))

                st.write("---")
                df = pd.DataFrame(results).sort_values(by="تغير%", ascending=False)
                
                # تلوين الجدول
                def style_rows(row):
                    if row['الأمر'] == "🚀 هجوم": return ['background-color: #4c0000'] * len(row)
                    return [''] * len(row)

                st.table(df.style.apply(style_rows, axis=1))
    
    else:
        st.warning("🔄 السيرفر يحاول الاتصال بالسوق العالمي... انتظر ثواني")

    time.sleep(10) # 10 ثواني لضمان استقرار السيرفر
