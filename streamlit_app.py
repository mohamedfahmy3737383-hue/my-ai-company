import streamlit as st
import pandas as pd
import requests
import time

# 1. إعدادات المنصة الاحترافية
st.set_page_config(page_title="شركة صيد الحيتان المتكاملة", layout="wide")

if 'prev_vol' not in st.session_state:
    st.session_state.prev_vol = {}
if 'last_signals' not in st.session_state:
    st.session_state.last_signals = {}

def play_alert():
    # تنبيه ذكي غير مزعج
    st.components.v1.html("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>""", height=0)

# 2. الجانب الأيسر: إدارة الـ 100 جنيه (المحفظة)
st.sidebar.title("💰 محفظة الـ 100 جنيه")
buy_price = st.sidebar.number_input("سعر شراء عملتك (بالدولار):", value=0.000001, format="%.8f")
target_profit = st.sidebar.slider("هدف الربح (بالجنيه):", 1, 100, 20)

st.title("🐋 مركز العمليات المشترك")
st.write("نظام مراقبة السيولة + كاشف الانفجار السعري + إدارة الأرباح")

def fetch_data():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    data = fetch_data()
    if data:
        targets = ['PEPEUSDT', 'SHIBUSDT', 'BONKUSDT', 'FLOKIUSDT', 'LUNCUSDT', '1000SATSUSDT', 'SOLUSDT', 'XRPUSDT']
        rows = []
        current_time = time.time()
        
        for item in data:
            if item['symbol'] in targets:
                symbol = item['symbol']
                price = float(item['lastPrice'])
                change = float(item['priceChangePercent'])
                current_vol = float(item['quoteVolume'])
                
                # أ- حساب السيولة اللحظية (الداخلة الآن)
                prev_v = st.session_state.prev_vol.get(symbol, current_vol)
                new_money = current_vol - prev_v
                st.session_state.prev_vol[symbol] = current_vol
                
                # ب- حساب قوة الفرصة (Power Score)
                power_score = (change * 5) + (new_money / 1000)
                
                # ج- تحديد الحالة وتجميد الإشارة
                if power_score > 30 or new_money > 5000:
                    st.session_state.last_signals[symbol] = current_time
                    play_alert()
                
                is_active = symbol in st.session_state.last_signals and (current_time - st.session_state.last_signals[symbol] < 60)
                
                rows.append({
                    "العملة": symbol.replace("USDT", ""),
                    "السعر": f"${price:.8f}",
                    "تغير 24س": f"{change}%",
                    "سيولة دخلت (لحظياً)": f"${new_money:,.0f}",
                    "قوة الفرصة": round(power_score, 1),
                    "القرار": "🚀 هجوم / دخول" if is_active else "💤 مراقبة"
                })

        with placeholder.container():
            # 3. عرض حسابات الـ 100 جنيه (الأرباح)
            # افترضنا أن العملة الأساسية للمتابعة هي أول واحدة في القائمة أو المختارة
            my_coin_data = next((item for item in rows if "🚀" in item['القرار']), rows[0])
            curr_p = float(my_coin_data['السعر'].replace('$', ''))
            val_egp = ((2.0 / buy_price) * curr_p) * 50 if buy_price > 0 else 100
            
            c1, c2, c3 = st.columns(3)
            c1.metric("قيمة الـ 100 ج الآن", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
            c2.metric("أقوى سيولة الآن", f"{max([float(r['سيولة دخلت (لحظياً)'].replace('$','').replace(',','')) for r in rows]):,.0f}$")
            c3.metric("تحديث الرادار", time.strftime('%H:%M:%S'))

            # 4. شريط التقدم للربح
            st.write(f"التقدم نحو هدف الـ {target_profit} جنيه إضافية:")
            st.progress(min(max((val_egp-100)/target_profit, 0.0), 1.0) if val_egp > 100 else 0.0)

            st.write("---")
            # 5. الجدول الشامل الملون
            df = pd.DataFrame(rows).sort_values(by="قوة الفرصة", ascending=False)
            
            def highlight_status(val):
                if "🚀" in val: return 'background-color: #900c3f; color: white'
                return ''

            st.table(df.style.applymap(highlight_status, subset=['القرار']))

    time.sleep(5)
