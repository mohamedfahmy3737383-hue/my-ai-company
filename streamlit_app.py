import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Global Control Final", layout="wide")

# ذاكرة الشركة الذكية
if 'prev_v' not in st.session_state: st.session_state.prev_v = {}
if 'last_signals' not in st.session_state: st.session_state.last_signals = {}

st.title("🌎 رادار السيطرة العالمية (نسخة تخطي الحجب)")

# إدارة المحفظة
st.sidebar.title("💰 محفظة الـ 100 جنيه")
buy_p = st.sidebar.number_input("سعر شراء عملتك ($):", value=0.000001, format="%.8f")

def get_data_v2():
    # استخدام رابط عالمي مجمع (Coincap) لضمان عدم الحظر وسرعة الاستجابة
    try:
        url = "https://api.coincap.io/v2/assets?limit=50"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json().get('data', [])
    except:
        return None
    return None

placeholder = st.empty()

while True:
    data = get_data_v2()
    
    if data and isinstance(data, list):
        # العملات المستهدفة للسيطرة
        targets = ['bitcoin', 'ethereum', 'solana', 'pepe', 'shiba-inu', 'dogecoin', 'xrp', 'luna-classic', 'bonk']
        results = []
        current_time = time.time()
        
        for item in data:
            coin_id = item.get('id')
            if coin_id in targets:
                sym = item.get('symbol')
                p = float(item.get('priceUsd', 0))
                c = float(item.get('changePercent24Hr', 0))
                v = float(item.get('volumeUsd24Hr', 0))
                
                # حساب تدفق السيولة اللحظي
                old_v = st.session_state.prev_v.get(sym, v)
                flow = v - old_v
                st.session_state.prev_v[sym] = v
                
                # تحليل الحيتان والأخبار
                whale = "🐳 حوت ضخم" if flow > 100000 else "🐟 تجميع"
                news = "🔥 انفجار" if c > 7 else "📈 صعود" if c > 2 else "📰 مستقر"
                
                # قوة السيطرة
                score = (c * 5) + (flow / 5000)
                if score > 30: st.session_state.last_signals[sym] = current_time
                active = sym in st.session_state.last_signals and (current_time - st.session_state.last_signals[sym] < 60)

                results.append({
                    "العملة": sym,
                    "السعر ($)": f"{p:.8f}" if p < 1 else f"{p:,.2f}",
                    "تغير %": round(c, 2),
                    "تدفق الأموال": f"${flow:,.0f}",
                    "الحيتان": whale,
                    "الأخبار": news,
                    "الأمر": "🚀 هجوم" if active else "📡 مراقبة"
                })

        if results:
            with placeholder.container():
                # حساب قيمة الـ 100 جنيه
                ref_coin = next((x for x in results if x['العملة'] == "PEPE"), results[0])
                curr_p = float(ref_coin['السعر ($)'].replace(',', ''))
                val_egp = ((2.0 / buy_p) * curr_p) * 50 if buy_p > 0 else 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric("الـ 100ج الآن", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("حالة السوق العالمي", "🔥 مشتعل" if c > 2 else "💤 هادئ")
                c3.metric("تحديث الرادار", time.strftime('%H:%M:%S'))

                st.write("---")
                df = pd.DataFrame(results).sort_values(by="تغير %", ascending=False)
                
                def color_rows(row):
                    if "هجوم" in row['الأمر']: return ['background-color: #4c0000'] * len(row)
                    return [''] * len(row)

                st.table(df.style.apply(color_rows, axis=1))

    else:
        st.info("🔄 جاري محاولة اختراق حجب السيرفر... الشركة لا تتوقف")

    time.sleep(10)
