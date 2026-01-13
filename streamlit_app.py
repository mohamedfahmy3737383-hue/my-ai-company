import streamlit as st
import pandas as pd
import requests
import time

# 1. إعدادات السيطرة العالمية
st.set_page_config(page_title="Global Control Center V4", layout="wide")

# تهيئة الذاكرة
if 'prev_vol' not in st.session_state: st.session_state.prev_vol = {}
if 'last_signals' not in st.session_state: st.session_state.last_signals = {}

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>""", height=0)

# 2. إدارة المحفظة (الـ 100 جنيه) في الجانب
st.sidebar.title("💰 محفظة الـ 100 جنيه")
buy_price = st.sidebar.number_input("سعر شراء عملتك ($):", value=0.000001, format="%.8f")
target_profit = st.sidebar.slider("الهدف فوق الـ 100 (ج):", 1, 200, 50)

st.title("🌐 رادار السيطرة الشاملة (أخبار + حيتان + أرباح)")

def fetch_safe_data():
    try:
        # سحب بيانات من Binance API (الأكثر استقراراً للعالم)
        response = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"خطأ في الاتصال بالسوق: {e}")
    return None

placeholder = st.empty()

while True:
    data = fetch_safe_data()
    if data and isinstance(data, list):
        # القائمة الكاملة للسيطرة
        targets = [
            'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT', 'PEPEUSDT', 
            'SHIBUSDT', 'BONKUSDT', 'FLOKIUSDT', 'LUNCUSDT', '1000SATSUSDT', 
            'RATSUSDT', 'TURBOUSDT', 'BOMEUSDT', 'DOGEUSDT'
        ]
        
        results = []
        current_time = time.time()
        
        for item in data:
            # التأكد من أن البيانات تحتوي على المفاتيح المطلوبة لمنع الـ TypeError
            if isinstance(item, dict) and 'symbol' in item and item['symbol'] in targets:
                symbol = item['symbol']
                price = float(item.get('lastPrice', 0))
                change = float(item.get('priceChangePercent', 0))
                vol_usd = float(item.get('quoteVolume', 0))
                
                # 1. رادار السيولة اللحظية
                prev_v = st.session_state.prev_vol.get(symbol, vol_usd)
                money_flow = vol_usd - prev_v
                st.session_state.prev_vol[symbol] = vol_usd
                
                # 2. كاشف الحيتان و الأخبار
                whale_action = "🐳 حوت ضخم" if money_flow > 100000 else "🐟 تجميع" if money_flow > 5000 else "💤 هدوء"
                news = "🔥 انفجار إخباري" if change > 8 else "📈 زخم عالمي" if change > 2 else "📰 مستقر"
                
                # 3. قوة السيطرة
                power_score = (change * 5) + (money_flow / 5000)
                
                if power_score > 35:
                    st.session_state.last_signals[symbol] = current_time
                    play_alert()
                
                is_active = symbol in st.session_state.last_signals and (current_time - st.session_state.last_signals[symbol] < 60)

                results.append({
                    "العملة": symbol.replace("USDT", ""),
                    "السعر ($)": f"{price:.8f}" if price < 1 else f"{price:,.2f}",
                    "تغير %": f"{change}%",
                    "سيولة دخلت ($)": f"{money_flow:,.0f}",
                    "الحيتان": whale_action,
                    "الأخبار": news,
                    "القوة": round(power_score, 1),
                    "الأمر": "🚀 هجوم" if is_active else "📡 مراقبة"
                })

        if results:
            with placeholder.container():
                # حسابات الـ 100 جنيه
                # نأخذ سعر PEPE كمثال للحساب إذا كانت موجودة، وإلا نأخذ أول عملة
                pepe_data = next((r for r in results if r['العملة'] == "PEPE"), results[0])
                curr_p_float = float(pepe_data['السعر ($)'].replace(',', ''))
                val_egp = ((2.0 / buy_price) * curr_p_float) * 50 if buy_price > 0 else 100
                
                c1, c2, c3 = st.columns(3)
                c1.metric("قيمة الـ 100 ج الآن", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                c2.metric("إجمالي السيولة", f"${sum([float(x['سيولة دخلت ($)'].replace(',','')) for x in results]):,.0f}")
                c3.metric("توقيت السيطرة", time.strftime('%H:%M:%S'))

                st.write("---")
                # عرض الجدول الموحد
                df = pd.DataFrame(results).sort_values(by="القوة", ascending=False)
                
                def style_rows(row):
                    if row['الأمر'] == "🚀 هجوم": return ['background-color: #4c0000'] * len(row)
                    if row['الحيتان'] == "🐳 حوت ضخم": return ['background-color: #002b36'] * len(row)
                    return [''] * len(row)

                st.table(df.style.apply(style_rows, axis=1))
                st.info(f"📢 الرادار يراقب الآن {len(targets)} سوقاً عالمياً في نفس اللحظة.")

    time.sleep(5)
