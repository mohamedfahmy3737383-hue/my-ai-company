import streamlit as st
import pandas as pd
import yfinance as ticker
import time

# إعدادات بسيطة جداً
st.set_page_config(page_title="مدير الإمبراطورية", layout="centered")

st.title("🏛️ لوحة تحكم شركة الـ 100 جنيه")
st.write("مرحباً بك يا مدير.. السيستم يعمل الآن لتأمين أرباحك.")

#Sidebar للمدخلات البسيطة
asset = st.sidebar.text_input("العملة التي نراقبها:", value="BTC-USD")
my_money = 100 # رأس مالنا

# قائمة العملات اللي بنصطاد منها
watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'CHZ-USD', 'DOGE-USD']

placeholder = st.empty()

while True:
    try:
        # سحب البيانات بطلقة واحدة سريعة
        df_raw = ticker.download(watchlist, period="1d", interval="2m", progress=False)['Close']
        
        if not df_raw.empty:
            df_raw = df_raw.ffill().bfill()
            
            with placeholder.container():
                # 1. حساب المكسب والخسارة (ببساطة)
                current_price = df_raw[asset].iloc[-1]
                # نفترض إننا اشترينا عند أول السعر المتاح في الجدول
                entry_price = df_raw[asset].iloc[0]
                profit_percent = ((current_price - entry_price) / entry_price)
                total_now = my_money + (my_money * profit_percent)
                
                c1, c2 = st.columns(2)
                c1.metric("رأس مالك الآن", f"{total_now:.2f} ج.م", f"{total_now - 100:.2f}")
                c2.metric("السعر الحالي", f"${current_price:.2f}")

                st.write("---")
                
                # 2. جدول "سيد رادار" (الإشارات الواضحة)
                st.subheader("🎯 توصيات الموظفين الآن:")
                reports = []
                for sym in watchlist:
                    p = df_raw[sym]
                    change = ((p.iloc[-1] - p.iloc[-5]) / p.iloc[-5]) * 100
                    status = "🟢 فرصتك! (شراء)" if change > 0.3 else "🔴 خطر! (بيع)" if change < -0.3 else "📡 راقب بهدوء"
                    reports.append({"العملة": sym, "القرار": status})
                
                st.table(pd.DataFrame(reports))

                # 3. رسمة خالد (الرسم البياني)
                st.line_chart(df_raw[asset].tail(30))

    except:
        st.write("🔄 جاري تحديث البيانات..")
    
    time.sleep(15) # تحديث كل 15 ثانية (سرعة مثالية)
