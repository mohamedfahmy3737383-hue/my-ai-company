import streamlit as st
import pandas as pd
import requests
import time

# 1. إعدادات السيطرة الكونية
st.set_page_config(page_title="Global Control & News Center", layout="wide")

if 'prev_vol' not in st.session_state:
    st.session_state.prev_vol = {}
if 'last_signals' not in st.session_state:
    st.session_state.last_signals = {}

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>""", height=0)

# 2. إدارة المحفظة (الـ 100 جنيه)
st.sidebar.title("💰 محفظة الـ 100 جنيه")
buy_price = st.sidebar.number_input("سعر شراء عملتك ($):", value=0.000001, format="%.8f")
target_profit = st.sidebar.slider("الهدف فوق الـ 100 (ج):", 1, 200, 50)

st.title("🌐 مركز عمليات السيطرة العالمية (إصدار الأخبار والحيتان)")

def fetch_all():
    # سحب بيانات السوق العالمي + محاكاة رادار الأخبار اللحظي
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    data = fetch_all()
    if data:
        # القائمة الكاملة (الكبيرة والرخيصة والمجنونة)
        targets = [
            'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT', 'PEPEUSDT', 
            'SHIBUSDT', 'BONKUSDT', 'FLOKIUSDT', 'LUNCUSDT', '1000SATSUSDT', 
            'RATSUSDT', 'TURBOUSDT', 'BOMEUSDT', 'DOGEUSDT'
        ]
        
        results = []
        current_time = time.time()
        
        for item in data:
            if item['symbol'] in targets:
                symbol = item['symbol']
                price = float(item['lastPrice'])
                change = float(item['priceChangePercent'])
                vol_usd = float(item['quoteVolume'])
                
                # أ- رادار السيولة اللحظية
                prev_v = st.session_state.prev_vol.get(symbol, vol_usd)
                money_flow = vol_usd - prev_v
                st.session_state.prev_vol[symbol] = vol_usd
                
                # ب- كاشف الحيتان (Whale Activity)
                whale_action = "🐳 حوت يشتري" if money_flow > 50000 else "🐟 أفراد" if money_flow > 0 else "💤 خمول"
                
                # ج- رادار الأخبار العاجلة (محاكاة ذكية بناءً على الزخم)
                if change > 10: news = "🔥 خبر انفجاري منتشر!"
                elif change > 5: news = "📈 اهتمام متزايد عالمياً"
                elif change < -5: news = "⚠️ إشاعات سلبية"
                else: news = "📰 أخبار مستقرة"
                
                # د- مؤشر السيطرة والقوة
                power_score = (change * 5) + (money_flow / 2000)
                
                if power_score > 40:
                    st.session_state.last_signals[symbol] = current_time
                    play_alert()
                
                is_active = symbol in st.session_state.last_signals and (current_time - st.session_state.last_signals[symbol] < 60)

                results.append({
                    "العملة": symbol.replace("USDT", ""),
                    "السعر العالمي": f"${price:.8f}",
                    "تغير %": f"{change}%",
                    "سيولة دخلت ($)": f"{money_flow:,.0f}",
                    "نشاط الحيتان": whale_action,
                    "أخبار عاجلة": news,
                    "قوة السيطرة": round(power_score, 1),
                    "أمر السيطرة": "🚀 هـجـوم" if is_active else "📡 مراقبة"
                })

        with placeholder.container():
            # حسابات الـ 100 جنيه
            target_coin = next((r for r in results if r['العملة'] == "PEPE"), results[0])
            curr_p = float(target_coin['السعر العالمي'].replace('$', ''))
            val_egp = ((2.0 / buy_price) * curr_p) * 50 if buy_price > 0 else 100
            
            c1, c2, c3 = st.columns(3)
            c1.metric("قيمة الـ 100 ج الآن", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
            c2.metric("إجمالي تدفق السوق", f"${sum([float(x['سيولة دخلت ($)'].replace(',','')) for x in results]):,.0f}")
            c3.metric("توقيت السيطرة", time.strftime('%H:%M:%S'))

            st.write("---")
            # الجدول العملاق (تم إضافة الأخبار ونشاط الحيتان)
            df = pd.DataFrame(results).sort_values(by="قوة السيطرة", ascending=False)
            
            def style_global(s):
                bg = ''
                if s['أمر السيطرة'] == "🚀 هـجـوم": bg = 'background-color: #4c0000'
                elif s['نشاط الحيتان'] == "🐳 حوت يشتري": bg = 'background-color: #002b36'
                return [bg] * len(s)

            st.table(df.style.apply(style_global, axis=1))
            
            #
