import streamlit as st
import pandas as pd
import yfinance as ticker
import time

# 1. إعدادات الهيكل الإداري
st.set_page_config(page_title="Empire HQ - Full Control", layout="wide")

# منع الأخطاء العابرة
if 'init' not in st.session_state:
    st.session_state['init'] = True

# --- واجهة القيادة ---
st.title("🏛️ مقر إدارة إمبراطورية الـ 100 جنيه (النسخة الشاملة)")
st.write(f"📡 النظام يعمل بكامل طاقته | {time.strftime('%H:%M:%S')}")

# 2. مكتب المدير العام (Sidebar)
st.sidebar.title("👤 مكتب المدير العام")
asset_input = st.sidebar.text_input("العملة للمتابعة (مثل CHZ-USD):", value="CHZ-USD").upper()
buy_p = st.sidebar.number_input("سعر دخولنا ($):", value=0.1500, format="%.4f")
refresh_rate = st.sidebar.slider("سرعة الرصد (ثانية):", 10, 60, 15)

# قائمة العملات القناصة
watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD', 'SHIB-USD', 'PEPE24478-USD', 'BONK-USD']

placeholder = st.empty()

while True:
    try:
        # جلب البيانات لآخر 60 دقيقة لضمان دقة "عصام كاشف" و "سيد رادار"
        raw_data = ticker.download(watchlist, period="1d", interval="1m", progress=False)['Close']
        
        if not raw_data.empty:
            raw_data = raw_data.ffill().bfill()
            report_data = []
            
            for sym in watchlist:
                prices = raw_data[sym]
                curr_p = prices.iloc[-1]
                prev_p_5 = prices.iloc[-5] if len(prices) > 5 else prices.iloc[0]
                sma_20 = prices.tail(20).mean()
                
                # حساب كاشف الانفجار (Squeeze) - تخصص عصام كاشف
                p_range = (prices.tail(20).max() - prices.tail(20).min()) / prices.tail(20).mean()
                is_squeeze = p_range < 0.0025
                
                # حساب الإشارات (Buy/Sell) - تخصص سيد رادار
                change_5m = ((curr_p - prev_p_5) / prev_p_5) * 100
                
                if change_5m > 0.35 and curr_p > sma_20:
                    status = "🟢 BUY (شراء)"
                    color = "#00ff00"
                elif change_5m < -0.30 or (curr_p < sma_20 and change_5m < 0):
                    status = "🔴 SELL (بيع)"
                    color = "#ff0000"
                elif is_squeeze:
                    status = "⚠️ SQUEEZE (شحن)"
                    color = "#ffa500"
                else:
                    status = "📡 WATCH (رصد)"
                    color = "#ffffff"
                
                report_data.append({
                    "العملة": sym.replace("-USD",""),
                    "السعر ($)": f"{curr_p:.8f}" if curr_p < 0.1 else f"{curr_p:.4f}",
                    "نبض 5د %": round(change_5m, 3),
                    "تقرير الموظفين": status
                })

            df = pd.DataFrame(report_data)

            with placeholder.container():
                # --- غرفة اجتماعات الموظفين (المقاييس) ---
                m1, m2, m3 = st.columns(3)
                
                with m1:
                    st.info("👨‍💼 **مجدي حسابات**")
                    try:
                        target_p = ticker.Ticker(asset_input).fast_info['last_price']
                        val_egp = ((2.0 / buy_p) * target_p) * 50 if buy_p > 0 else 100
                        st.metric(f"قيمة الـ 100ج في {asset_input}", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
                    except: st.write("مجدي بيراجع الدفاتر...")

                with m2:
                    st.warning("🕵️‍♂️ **عصام كاشف**")
                    squeezes = df[df['تقرير الموظفين'].str.contains("SQUEEZE")]['العملة'].tolist()
                    if squeezes: st.write(f"فيه انفجار جاي في: {', '.join(squeezes)}")
                    else: st.write("السوق مستقر حالياً")

                with m3:
                    st.success("🎯 **سيد رادار**")
                    buys = df[df['تقرير الموظفين'].str.contains("BUY")]['العملة'].tolist()
                    if buys: st.write(f"اضرب يا مدير! دخول في: {', '.join(buys)}")
                    else: st.write("بندور على فرصة صيد...")

                st.write("---")
                
                # الجدول النهائي الملون (بدون أي NaN)
                def apply_color(val):
                    if "BUY" in val: return 'color: #00ff00; font-weight: bold'
                    if "SELL" in val: return 'color: #ff0000; font-weight: bold'
                    if "SQUEEZE" in val: return 'color: #ffa500; font-weight: bold'
                    return 'color: white'

                st.subheader("📊 بيان العمليات المركزية")
                st.table(df.style.applymap(apply_color, subset=['تقرير الموظفين']))

                # تنبيهات فورية
                if "🟢 BUY" in df['تقرير الموظفين'].values:
                    st.toast("🚨 إشارة BUY جديدة! اطلب سيد رادار", icon="💰")

    except Exception as e:
        st.write("🔄 السيرفر بيحاول يجمع بيانات... ثواني")
    
    time.sleep(refresh_rate)
