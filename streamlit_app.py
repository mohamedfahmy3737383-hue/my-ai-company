import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Global Market Dominator", layout="wide")

st.title("🌎 رادار السيطرة الشاملة (كافة عملات العالم)")
st.write("الرادار يراقب الآن آلاف العملات لاصطياد أقوى الانفجارات السعرية")

# إدارة المحفظة
st.sidebar.title("💰 شركة الـ 100 جنيه")
user_asset = st.sidebar.selectbox("اختر عملتك للمتابعة:", ["PEPE", "SHIB", "DOGE", "BTC", "SOL", "LUNC"])
buy_p = st.sidebar.number_input("سعر شراء عملتك ($):", value=0.000001, format="%.8f")

def get_all_world_assets():
    # سحب بيانات الـ 2000 عملة الأوائل في العالم (تغطية شاملة)
    try:
        url = "https://api.coincap.io/v2/assets?limit=2000"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json().get('data', [])
    except:
        return None
    return None

placeholder = st.empty()

while True:
    all_data = get_all_world_assets()
    
    if all_data:
        results = []
        for item in all_data:
            try:
                p = float(item.get('priceUsd', 0))
                c = float(item.get('changePercent24Hr', 0))
                v = float(item.get('volumeUsd24Hr', 0))
                sym = item.get('symbol')
                
                results.append({
                    "الترتيب": int(item.get('rank')),
                    "العملة": sym,
                    "الاسم": item.get('name'),
                    "السعر ($)": p,
                    "تغير %": round(c, 2),
                    "السيولة (24س)": v,
                    "القرار": "🚀 انفجار" if c > 15 else "🔥 صعود قوي" if c > 7 else "📡 مستقر"
                })
            except: continue

        df_all = pd.DataFrame(results)

        with placeholder.container():
            # 1. قسم الانفجارات اللحظية (أعلى 5 عملات في العالم حالياً)
            st.subheader("⚠️ أكبر انفجارات في العالم الآن")
            top_explosions = df_all.sort_values(by="تغير %", ascending=False).head(5)
            cols = st.columns(5)
            for i, (index, row) in enumerate(top_explosions.iterrows()):
                cols[i].metric(row['العملة'], f"${row['السعر ($)']:.4f}", f"{row['تغير %']}%")

            st.write("---")

            # 2. حسابات الـ 100 جنيه للعملة المختارة
            my_coin = df_all[df_all['العملة'] == user_asset].iloc[0] if user_asset in df_all['العملة'].values else results[0]
            val_egp = ((2.0 / buy_p) * my_coin['السعر ($)']) * 50 if buy_p > 0 else 100
            
            c1, c2, c3 = st.columns(3)
            c1.metric(f"قيمة الـ 100ج في {user_asset}", f"{val_egp:.2f} ج.م", f"{val_egp-100:.2f}")
            c2.metric("إجمالي العملات المراقبة", f"{len(df_all)}")
            c3.metric("توقيت السيطرة", time.strftime('%H:%M:%S'))

            # 3. جدول السيطرة الشامل (قابل للبحث والترتيب)
            st.subheader("📊 قائمة العملات العالمية (رتب حسب التغير أو السيولة)")
            
            # فلتر سريع للبحث
            search = st.text_input("🔍 ابحث عن أي عملة في العالم (مثلاً: BONK, FLOKI, BTC):")
            if search:
                display_df = df_all[df_all['العملة'].str.contains(search.upper())]
            else:
                display_df = df_all.head(100) # عرض أول 100 عملة افتراضياً للسرعة

            st.dataframe(display_df.style.highlight_max(axis=0, subset=['تغير %']), use_container_width=True)

    else:
        st.warning("🔄 الرادار يقوم بمسح آلاف العملات الآن... انتظر ثواني")

    time.sleep(15) # تحديث كل 15 ثانية لمواكبة حجم البيانات الضخم
