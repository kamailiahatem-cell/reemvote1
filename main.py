import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def send_single_vote(vote_id):
    """الدالة دي بتنفذ عملية تصويت واحدة فقط وبترجع النتيجة"""
    try:
        # لازم Session عشان السيرفر يفتكر إنك نفس الشخص اللي شاف صورة الكابتشا
        session = requests.Session()

        # 1. هنا هيكون كود تحميل الصورة وقراءتها
        extracted_code = "000000" # (كمثال)
        vote_code = "6397"
        # 6154 Ayten
        # 6943 Rehab
        # 6397 Dana
        # 6557 Ghassan
        # 6923 wafa
        # 6941 merna gamil
        # 6155 eman elsayed
        # 2. توليد طابع زمني (Timestamp)
        timestamp = int(time.time() * 1000)

        # 3. تجهيز رابط التصويت بالبيانات الجديدة
        vote_url = f"https://www.washwasha.org/service/pollcap.aspx?pid=0&hid={vote_code}&code={extracted_code}&_={timestamp}"

        # 4. إرسال التصويت (GET Request)
        response = session.get(vote_url, timeout=10)

        # 5. إرجاع النتيجة عشان نطبعها بره
        return f"[Vote #{vote_id}] Server Response: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"[Vote #{vote_id}] Connection Error: {e}"
    except Exception as e:
        return f"[Vote #{vote_id}] General Error: {e}"

# ==========================================
# إعداد وتشغيل الـ ThreadPoolExecutor
# ==========================================

NUM_THREADS = 1000 # عدد الطلبات اللي هتتبعت في نفس الوقت (حجم الدفعة)
vote_counter = 1 # عداد عشان نرقم الطلبات ونتابعها

print(f"Starting voting pool with {NUM_THREADS} concurrent threads...\n")

# استخدام with بيضمن إن الـ Executor يتقفل بشكل سليم لما البرنامج يخلص
with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    try:
        while True: # حلقة لا نهائية لإرسال الدفعات

            # بنجهز دفعة من الطلبات (Futures) نبعتها للـ Executor
            futures = []
            for _ in range(NUM_THREADS):
                futures.append(executor.submit(send_single_vote, vote_counter))
                vote_counter += 1

            # as_completed بتستقبل النتيجة أول ما الـ Thread يخلص شغله
            for future in as_completed(futures):
                result = future.result()
                print(result)

            # (اختياري) ممكن تحط وقت انتظار بسيط بين كل دفعة واللي بعدها
            # time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping the executor. Exiting program...")
