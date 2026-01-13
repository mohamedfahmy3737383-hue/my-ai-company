import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Arbitrage Hunter 🔊", layout="wide")

# كود تشغيل الصوت (جرس تنبيه)
def play_sound():
    sound_html = """
    <audio autoplay>
    <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
    </audio>
    """
    st.components.v1.html(sound_html, height=0)

st.title("🏹 رادار القنص الاحترافي مع التنبيه الصوتي")

def get_mexc_data():
    url = "https://api.mexc.com/api/v3/ticker/bookTicker"
    try:
        return requests.get(url, timeout=5).json()
    except: return None

placeholder = st.empty()

while True:
    raw_data = get_mexc_data()
    if raw_data:
        # قائمة العملات
        targets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'PEPEUSDT', 'SHIBUSDT']
        final_list = []
        alert_flag = False # علامة لإطلاق الجرس

        for item in raw_data:
            if item['symbol'] in targets:
                bid = float(item['bidPrice'])
                ask = float(item['askPrice'])
                # الفارق بين سعر البيع والشراء
                spread = ((ask - bid) / bid) * 100
                net = spread - 0.2 # خصم عمولة المنصة
                
                status = "❌ ضعيفة"
                if net > 0.05: # لو الربح أكبر من 0.05%
                    status = "🔥 فرصة قوية!"
                    alert_flag = True
                elif net > 0:
                    status = "✅ ربح بسيط"

                final_list.append({
                    "العملة": item['symbol'].replace("USDT", ""),
                    "سعر الشراء الحالي": f"${bid:,.4f}",
                    "سعر البيع الفوري": f"${ask:,.4f}",
                    "صافي الربح المتوقع": f"{net:.3f}%",
                    "الحالة": status
                })

        with placeholder.container():
            # إذا وجدت فرصة، شغل الصوت
            if alert_flag:
                play_sound()
                st.balloons()
            
            c1, c2 = st.columns([3, 1])
            c1.subheader(f"📊 مراقبة السوق اللحظية - {time.strftime('%H:%M:%S')}")
            
            df = pd.DataFrame(final_list)
            
            # تنسيق الجدول
            def color_rows(val):
                if "🔥" in val: return 'background-color: #1b4d3e; color: white'
                if "✅" in val: return 'background-color: #1e3a8a; color: white'
                return ''

            st.table(df.style.applymap(color_rows, subset=['الحالة']))
            
            st.info("💡 التنبيه الصوتي يعمل تلقائياً عند ظهور 'فرصة قوية'. تأكد من رفع صوت التابلت.")

    time.sleep(5)
