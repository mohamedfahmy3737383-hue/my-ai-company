import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="My 100 EGP Growth", layout="wide")

# إعدادات المحفظة
st.sidebar.header("🕹️ لوحة تحكم الـ 100 جنيه")
buy_price = st.sidebar.number_input("سعر شراء العملة (بالدولار):", value=0.000001, format="%.8f")
target_profit_egp = st.sidebar.slider("هدفك الربحي (جنيه):", 1, 50, 10)

st.title("💸 رادار نمو رأس المال")
st.info(f"إنت بدأت بـ 100 جنيه. هدفنا نوصل لـ {100 + target_profit_egp} جنيه!")

def get_mexc_stats():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    try: return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    stats_data = get_mexc_stats()
    if stats_data:
        # هنراقب PEPE كمثال لأن حركتها سريعة وهتحسسك بالـ 100 جنيه
        target_coin = "PEPEUSDT" 
        current_price = 0
        
        for item in stats_data:
            if item['symbol'] == target_coin:
                current_price = float(item['lastPrice'])
                break
        
        # حسابات الـ 100 جنيه
        capital_usd = 2.0 # الـ 100 جنيه
        units = capital_usd / buy_price
        current_value_usd = units * current_price
        current_value_egp = current_value_usd * 50 # سعر الصرف
        net_profit_egp = current_value_egp - 100
        
        with placeholder.container():
            # العرض بالألوان عشان تحس بالفرق
            color = "green" if net_profit_egp >= 0 else "red"
            st.markdown(f"<h1 style='text-align: center; color: {color};'>قيمة فلوسك الآن: {current_value_egp:.2f} جنيه</h1>", unsafe_allow_html=True)
            
            # شريط التقدم للهدف
            progress = min(max((net_profit_egp / target_profit_egp), 0.0), 1.0)
            st.write(f"التقدم نحو الهدف (+{target_profit_egp} جنيه):")
            st.progress(progress)
            
            col1, col2 = st.columns(2)
            col1.metric("صافي الربح", f"{net_profit_egp:.2f} ج.م", delta=f"{net_profit_egp:.2f}")
            col2.metric("سعر العملة اللحظي", f"${current_price:.8f}")
            
            st.divider()
            st.write("### 📢 ملاحظة المدير:")
            if net_profit_egp > 0:
                st.success(f"مبروك! الـ 100 جنيه زادت {net_profit_egp:.2f} جنيه. هل تبيع الآن؟")
            else:
                st.warning("السعر هادئ حالياً، انتظر القنصة القادمة.")

    time.sleep(5)
