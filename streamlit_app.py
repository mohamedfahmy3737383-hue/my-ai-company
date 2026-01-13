import streamlit as st
import pandas as pd
import requests
import time

# إعدادات السيطرة الفورية - نسخة خفيفة جداً
st.set_page_config(page_title="Global Sniper V5", layout="wide")

st.title("🏹 رادار السيطرة العالمية (النسخة السريعة)")

# إدارة الـ 100 جنيه
st.sidebar.title("💰 الشركة")
buy_p = st.sidebar.number_input("سعر شراء عملتك ($):", value=0.000001, format="%.8f")

# دالة سحب البيانات مع حماية من التهنيج
def get_market_data():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        r = requests.get(url, timeout=2)
        return r.json()
    except:
        return None

# مكان عرض البيانات
placeholder = st.empty()

# الذاكرة اللحظية
if 'prev_v' not in st.session_state:
    st.session_state.prev_v = {}

# حلقة العمل (بسيطة ومباشرة)
while True:
    data = get_market_data()
    
    if data:
        # أهم العملات اللي بتتحرك في العالم
        targets = ['BTCUSDT', 'SOLUSDT', 'XRPUSDT', 'PEPEUSDT', 'SHIBUSDT', 'BONKUSDT', 'FLOKIUSDT', '1000SATSUSDT', 'LUNCUSDT', 'DOGEUSDT']
        results = []
        
        for item in data:
            sym = item.get('symbol')
            if sym in targets:
                p = float(item['lastPrice'])
                c = float(item['priceChangePercent'])
                v = float(item['quoteVolume'])
                
                # حساب تدفق السيولة
                old_v = st.session_state.prev_v.get(sym, v)
                flow = v - old_v
                st.session_state.prev_v[sym] = v
                
                # إضافة الأخبار ونشاط الحيتان بشكل مختصر
                results.append({
                    "العملة": sym.replace("USDT",""),
                    "السعر": f"{p:.8f}" if p < 1 else f"{p:,.2f}",
                    "تغير%": c,
                    "سيولة دخلت": round(flow, 2),
                    "الحالة": "🚀 هجوم حيتان" if flow > 50000 else "📡 مراقبة"
                })
        
        with placeholder.container():
            # حساب الأرباح (الـ 100 جنيه)
            # نأخذ PEPE كمرجع للسرعة
            ref_coin = next((x for x in results if x['العملة'] == "PEPE"), results[0])
            curr_ref_p = float(ref_coin['السعر'].replace(',',''))
            val_egp = ((2.0 / buy_p) * curr_ref_p) * 50 if buy_p > 0 else 100
            
            # عرض عدادات السيطرة
            col1, col2, col3 = st.columns(3)
            col1.metric("قيمة الـ 100ج الآن", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
            col2.metric("أقوى حركة عالمية", f"{max([x['تغير%'] for x in results])}%")
            col3.metric("نبض السيرفر", time.strftime('%H:%M:%S'))

            # الجدول الذكي
            df = pd.DataFrame(results).sort_values(by="تغير%", ascending=False)
            st.table(df) # table أضمن في التحميل من dataframe لما السيرفر يكون تقيل
            
    time.sleep(7) # زودنا الوقت لـ 7 ثواني عشان السيرفر "يرتاح"
