import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="AI Portfolio Manager 💰", layout="wide")

# إعدادات المحفظة في الجنب
st.sidebar.title("💰 محفظة الـ 100 جنيه")
capital_egp = 100
usd_rate = 50 # سعر افتراضي للدولار مقابل الجنيه
capital_usd = capital_egp / usd_rate

selected_coin = st.sidebar.selectbox("العملة التي اشتريتها:", ['BTC', 'ETH', 'SOL', 'PEPE', 'SHIB', 'FLOKI'])
buy_price = st.sidebar.number_input("سعر الشراء (بالدولار):", value=0.00000001, format="%.8f")

st.title("🚀 رادار الأرباح اللحظي")

def get_mexc_stats():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    stats_data = get_mexc_stats()
    if stats_data:
        targets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'PEPEUSDT', 'SHIBUSDT', 'FLOKIUSDT', 'BONKUSDT']
        final_list = []
        current_holdings_value = 0

        for item in stats_data:
            symbol_clean = item['symbol'].replace("USDT", "")
            if item['symbol'] in targets:
                price = float(item['lastPrice'])
                volume = float(item['quoteVolume'])
                change = float(item['priceChangePercent'])
                
                # حساب أرباح المحفظة لو دي العملة اللي اخترتها
                if symbol_clean == selected_coin:
                    units = capital_usd / buy_price
                    current_holdings_value = units * price
                
                final_list.append({
                    "العملة": symbol_clean,
                    "السعر": f"${price:.8f}",
                    "التغير": f"{change}%",
                    "قوة الحيتان": "🐳" if volume > 10000000 else "🐟",
                    "التوقع": "🚀 صعود" if change > 2 else "➡️ استقرار"
                })

        with placeholder.container():
            # عرض حالة الـ 100 جنيه فوق
            profit_loss = current_holdings_value - capital_usd
            profit_percent = (profit_loss / capital_usd) * 100 if capital_usd > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("قيمة الـ 100 جنيه الآن", f"{(current_holdings_value * usd_rate):,.2f} ج.م")
            col2.metric("صافي الربح/الخسارة", f"{(profit_loss * usd_rate):,.2f} ج.م", f"{profit_percent:.2f}%")
            col3.metric("توقيت السوق", time.strftime('%H:%M:%S'))

            st.write("---")
            st.write("### 📊 تحديثات العملات والسيولة")
            st.table(pd.DataFrame(final_list))

    time.sleep(5)
