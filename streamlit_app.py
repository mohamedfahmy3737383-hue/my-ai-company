import ccxt
import time

def start_analyst_bot():
    ex1 = ccxt.kucoin()
    ex2 = ccxt.gateio()
    symbol = 'BTC/USDT'
    investment = 1000  # تخيل إننا داخلين بـ 1000 دولار
    
    print(f"--- الموظف المحلل بدأ العمل (رأس المال الافتراضي: ${investment}) ---")
    
    for i in range(15):
        try:
            p1 = ex1.fetch_ticker(symbol)['last']
            p2 = ex2.fetch_ticker(symbol)['last']
            
            # حساب الفرق والنسبة
            diff = abs(p1 - p2)
            p_diff = (diff / min(p1, p2)) * 100
            
            # خصم العمولات (تقريباً 0.2% للعملية الكاملة)
            net_profit_percent = p_diff - 0.2
            potential_money = (net_profit_percent / 100) * investment
            
            if net_profit_percent > 0:
                print(f"✅ فرصة ربح! صافي الربح: {net_profit_percent:.4f}% | دولار: ${potential_money:.2f}")
            else:
                print(f"⏳ مراقبة.. الفرق الحالي {p_diff:.4f}% (غير مربح بعد الخصم)")
                
            time.sleep(4)
        except Exception as e:
            print(f"تنبيه: {e}")

start_analyst_bot()
