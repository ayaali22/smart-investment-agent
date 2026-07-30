


import streamlit as st
import numpy as np
import importlib

faiss = None
try:
    faiss = importlib.import_module("faiss")
except ImportError:
    faiss = None
from openai import OpenAI

user_input = st.session_state.get("user_input", "")
bot_response = st.session_state.get("bot_response", "")

if user_input:
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)

if bot_response:
    with st.chat_message("assistant", avatar="🤖"): 
        st.write(bot_response)

# 🎨 إضافة تنسيقات CSS لتحسين الخط وجعل الاتجاه من اليمين لليسار (RTL)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');

html, body, [class*="css"], div, p, span, input, button, textarea {
font-family: 'Cairo', sans-serif !important;
direction: rtl !important;
text-align: right !important;
}
/* محاذاة خانة الشات والأيقونات للغة العربية */
.stChatInputContainer {
direction: rtl !important;
}
.stChatMessage {
direction: rtl !important;
text-align: right !important;
border-radius: 12px;
padding: 10px;
margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# --- 3. تصدير بطاقة تقرير الجاهزية للاستثمار ---
# تهيئة القيم الأساسية لتجنب أخطاء عدم تعريف المتغيرات عند تحميل الصفحة
user_name = st.session_state.get("user_name", "")
user_phone = st.session_state.get("user_phone", "")
user_email = st.session_state.get("user_email", "")
capital = st.session_state.get("capital", 0)
years = st.session_state.get("years", 0)
profit = st.session_state.get("profit", 0.0)
consent = st.session_state.get("consent", False)

st.sidebar.divider()
st.sidebar.subheader("📄 تصدير تقرير الجاهزية")

# تجهيز نص التقرير للتحميل
report_text = f"""
==================================================
تقرير جاهزية المستثمر - بورصة مسقط (MSX)
==================================================
الاسم الكامل: {user_name if user_name else 'غير محدد'}
رقم الهاتف: {user_phone if user_phone else 'غير محدد'}
البريد الإلكتروني: {user_email if user_email else 'غير محدد'}
المبلغ المستهدف للاستثمار: {capital} ريال عُماني
تاريخ إصدار التقرير: 2026-07-28

نتائج محاكاة التقييم:
- الأرباح التقديرية (بعد {years} سنوات): {profit:,.2f} ريال عُماني
- حالة تفويض البيانات: {'مُعتمد ومُرسل للمؤسسة' if consent else 'غير مُفوض'}

المؤسسات المرشحة للتواصل:
- أوبار الكابيتال / صندوق أمان العقاري (MSX)
==================================================
تم استخراج هذا التقرير بواسطة وكيل الاستثمار الذكي 🇴🇲
"""

st.sidebar.download_button(
label="📥 تحميل تقرير الجاهزية (TXT)",
data=report_text,
file_name=f"Investment_Report_{user_name if user_name else 'User'}.txt",
mime="text/plain"
)


st.title("📈 مرشد الاستثمار الذكي")
st.caption("رحلتك التأهيلية الموثوقة: تعلم ⬅️ تدرب بمحاكي ⬅️ تقرير الجاهزية ⬅️ الربط بشركات بورصة مسقط")

# 2. مفتاح OpenAI
api_key = "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"
client = OpenAI(api_key=api_key)

# 3. قاعدة المعرفة الموثوقة المربوطة بـ بورصة مسقط للأوراق المالية (RAG Base)
knowledge_base = [
# المؤسسات والشركات المعتمدة في بورصة مسقط (MSX)
"شركة أوبار الكابيتال (Ubar Capital) - وسيط معتمد في بورصة مسقط: متخصصة في تداول الأسهم العُمانية وصناديق المؤشرات والاستثمار المؤسسي. الحد الأدنى: 500 ريال عُماني. العائد المتوقع: 8%-18% سنوياً. المخاطرة: متوسطة إلى عالية.",
"شركة المتحدة للإستراتيجية الاستثمارية - التداول في بورصة مسقط: تقدم خدمات إدارة المحافظ المالية والأسهم القيادية بأسواق سلطنة عُمان. الحد الأدنى: 1,000 ريال عُماني. العائد المتوقع: 10%-15%. المخاطرة: متوسطة.",
"صندوق أمان العقاري (Aman REIT) - مدرج في بورصة مسقط (MSX): صندوق استثمار عقاري متداول يمنح توزيعات أرباح دورية ناتجة عن أصول عقارية عُمانية. الحد الأدنى: 200 ريال عُماني. العائد المتوقع: 6%-9% سنوياً. المخاطرة: منخفضة إلى متوسطة.",
"الصكوك الوطنية والسندات الحكومية العُمانية (بورصة مسقط): أدوات دين سيادية وآمنة تضمن رأس المال وتوفر عائدًا ثابتًا. الحد الأدنى: 500 ريال عُماني. العائد: 5%-7% سنوياً. المخاطرة: منخفضة جداً.",
"صناديق الذهب والسبائك عبر الشركات المعتمدة بسلطنة عُمان: أدوات حفظ الثروة والتحوط من التضخم العالمي. الحد الأدنى: 100 ريال عُماني. العائد: حفظ قيمة المال على المدى الطويل. المخاطرة: منخفضة.",

# القواعد والمعارف الموثوقة
"الفرق بين الادخار والاستثمار: الادخار هو حفظ الأموال في البنوك للاحتياجات القريبة، بينما الاستثمار في بورصة مسقط يهدف لتنمية المال ومواجهة التضخم عبر توزيعات الأرباح ونمو أسعار الأسهم والعقارات.",
"استراتيجية تنويع المحفظة الاستثمارية: يُنصح توزيع رأس المال بين أسهم نمو في بورصة مسقط (40%)، صناديق عقارية REITs (30%)، وصكوك أو ذهب لحماية المحفظة (30%).",
"تقرير درجة الجاهزية للاستثمار: يتضمن تقييم درجة المستخدم من 100 بناءً على توفر صندوق طوارئ، فهم أخطاء التسرع، والتوزيع المتوازن أثناء المحاكاة الافتراضية."
]

# 4. بناء فهرس FAISS للـ RAG
@st.cache_resource
def build_rag_index():
    embeddings = []
    for doc in knowledge_base:
        res = client.embeddings.create(input=doc, model="text-embedding-3-small")
        embeddings.append(res.data[0].embedding)

    embeddings_np = np.array(embeddings).astype('float32')

    # Fallback if faiss is not available: use a simple numpy-based index with same interface
    if faiss is None:
        class NumpyIndex:
            def __init__(self, vectors):
                self.vectors = vectors

            def add(self, vectors):
                if hasattr(self, 'vectors') and self.vectors.size:
                    self.vectors = np.vstack([self.vectors, vectors])
                else:
                    self.vectors = vectors

            def search(self, query_vec, top_k):
                # query_vec: (1, dim)
                # compute L2 distances
                diffs = self.vectors - query_vec
                dists = np.linalg.norm(diffs, axis=1)
                idx = np.argsort(dists)[:top_k]
                return dists[idx][None, :], idx[None, :]

        index = NumpyIndex(embeddings_np)
        return index

    index = faiss.IndexFlatL2(embeddings_np.shape[1])
    index.add(embeddings_np)
    return index

with st.spinner("جاري تحميل بيانات بورصة مسقط والقاعدة المعرفية..."):
    index = build_rag_index()

def retrieve_relevant_docs(query, top_k=2):
    res = client.embeddings.create(input=query, model="text-embedding-3-small")
    query_vec = np.array([res.data[0].embedding]).astype('float32')
    distances, indices = index.search(query_vec, top_k)
    return "\n".join([knowledge_base[i] for i in indices[0]])

# 5. إدارة جلسة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Initialize file_context before using it
file_context = ""


def save_investor_data(name, phone, email, capital_amount, consent_flag):
    """Save investor data locally in session state and return status.
    This is a lightweight placeholder for a real DB save.
    Returns (success: bool, result: str).
    """
    try:
        st.session_state['saved_investor'] = {
            'name': name,
            'phone': phone,
            'email': email,
            'capital': capital_amount,
            'consent': bool(consent_flag)
        }
        return True, "تم الحفظ"
    except Exception as e:
        return False, str(e)

with st.sidebar:
    st.header("📁 إرفاق المستندات")
    st.write("يمكنك رفع ملفاتك الاستثمارية أو كشف الحساب ليقوم الوكيل بتحليلها:")
    uploaded_file = st.file_uploader("اختر ملفاً (PDF, TXT, CSV)", type=["pdf", "txt", "csv"])

if uploaded_file is not None:
    st.success("تم رفع الملف بنجاح! سيتم تحليله بواسطة الوكيل.")
    # قراءة محتوى الملفات النصية كنموذج
    if uploaded_file.name.endswith('.txt'):
        file_context = uploaded_file.read().decode("utf-8")
    else:
        file_context = f"[تم إرفاق ملف باسم: {uploaded_file.name}]"
# 6. التفاعل ومعالجة الردود
if prompt := st.chat_input("اكتب إجابتك أو سؤالك الاستثماري هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # استرجاع سياق RAG
            context = retrieve_relevant_docs(prompt)
            # تحضير بيانات المستخدم
            user_data_context = f"""الاسم: {user_name}
رقم الهاتف: {user_phone}
البريد الإلكتروني: {user_email}
المبلغ: {capital} ريال عُماني
المدة: {years} سنة
التفويض: {'مُعتمد' if consent else 'غير مُفوض'}"""
            
            # التعليمات الصارمة والواضحة للوكيل
            # صياغة الـ Prompt المحدث لمنع التكرار وجعل الحوار نقاشياً وتفاعلياً
            agent_system_prompt = f"""
أنت "وكيل الاستثمار الذكي المعتمد لبورصة مسقط والمؤسسات الاستثمارية العُمانية 🇴🇲".

قاعدة المعرفة الموثوقة المتاحة لديك (RAG):
---
{context}
---

بيانات المستخدم والتفويض (إن وجد):
---
{user_data_context}
---

بيانات المستند المرفق (إن وجد):
---
{file_context}
---

🧠 **قواعد الذكاء والتفاعل الحواري:**

1️⃣ **إذا كان السؤال يخص الاستثمار، المال، الذهب، المؤسسات، أو بورصة مسقط (حتى لو كرر السؤال بطريقة أخرى):**
- ❌ **ممنوع منعاً باتاً** تكرار جملة "أنا وكيل استثماري متخصص...".
- ✅ **رد فوراً برد جديد ونقاشي مبتكر** يحلل سؤال المستخدم مباشرة، ويجيب على تفاصيله، ويقترب منه أكثر لتكملة رحلته الاستثمارية.
- ناقشه في الأرقام، الميزانيات، أنواع الأسهم العُمانية، أو نسب الذهب بكل مرونة وتفاعل.

2️⃣ **إذا كان السؤال خارج نطاق الاستثمار والمال بنسبة 100% (مثل: الطبخ، البرمجة، الطقس، الألعاب):**
- رد بهذه العبارة فقط:
"أنا وكيل استثماري متخصص في مجالات الاستثمار وبورصة مسقط للأوراق المالية فقط 🇴🇲. كيف يمكنني مساعدتك في رحلتك الاستثمارية أو ميزانيتك اليوم؟"

---

🎯 **مراحل رحلة الوكيل النقاشية (قد المستخدم عبرها بأسلوب متجدد):**
- **المرحلة 1:** التعرف على الميزانية الكلية بالريال العُماني + النسبة المحددة للادخار بالذهب.
- **المرحلة 2:** مناقشة فوائد توزيع الأصول بين الذهب، العقار (REITs)، والأسهم العُمانية.
- **المرحلة 3:** محاكاة تفاعلية أرقامها حية بناءً على ميزانية المستخدم.
- **المرحلة 4:** تقديم "تقرير درجة الجاهزية للاستثمار" (برقم من 100) متضمناً تحليلاً لنقاط قوته.
ا.🔹 **المرحلة الخامسة: التوجيه والربط**
• ترشيح المؤسسة العُمانية الملائمة مع إرسال وتضمين الروابط الإلكترونية الرسمية الخاصة بالمؤسسة لتسهيل وصول المستخدم إليها.
"""

            api_messages = [{"role": "system", "content": agent_system_prompt}]
            for m in st.session_state.messages:
                api_messages.append({"role": m["role"], "content": m["content"]})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages,
                temperature=0.2 # درجة حرارة منخفضة جداً لمنع أي إجابات خارج النص
            )

            full_response = response.choices[0].message.content
            message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال: {e}")





with st.sidebar:
    st.header("📋 بيانات التواصل والتفويض")
    st.write("أدخل بياناتك ليتم ربطك بالمؤسسة الاستثمارية المناسبة:")

    user_name = st.text_input("الاسم الكامل")
    user_phone = st.text_input("رقم الهاتف")
    user_email = st.text_input("البريد الإلكتروني")
    consent = st.checkbox("أوافق على مشاركة بياناتي أعلاه مع المؤسسة الاستثمارية المرشحة")

    
    # زر الإرسال المباشر
    if st.button("📤 إرسال البيانات"):
        if consent:
            if user_name and user_phone and user_email:
                # استدعاء دالة الحفظ
                success, result = save_investor_data(user_name, user_phone, user_email, capital, consent)
                if success:
                    st.success("✅ تم إرسال وحفظ بياناتك بنجاح !")
                    user_data_context = f"""
بيانات المستخدم المعتمدة للتواصل مع المؤسسة:
- الاسم: {user_name}
- رقم الهاتف: {user_phone}
- البريد الإلكتروني: {user_email}
- حالة التفويض: تم منح الموافقة الصريحة لمشاركة البيانات مع المؤسسة
"""
                else:
                    st.error(f"❌ حدث خطأ أثناء الحفظ: {result}")
            else:
                st.warning("⚠️ يرجى إكمال جميع الحقول (الاسم، الهاتف، الإيميل) لتفعيل التفويض.")
        else:
            st.warning("⚠️ يرجى تحديد خيار الموافقة على مشاركة البيانات أولاً.")




    user_data_context = ""

    capital = st.number_input("إجمالي المبلغ المستثمر (ر.ع)", min_value=100, value=1000, step=100)
    years = st.slider("المدى الزمني للاستثمار (سنوات)", min_value=1, max_value=10, value=3)
    expected_return = st.slider("نسبة العائد السنوي المتوقع (%)", min_value=3.0, max_value=20.0, value=10.0)



    # --- عرض سياق بيانات المستخدم والمستندات بطريقة آمنة
    summary_md = f"""
---
{user_data_context}
---
"""
    system_prompt = f"""
بيانات المستند المرفق (إن وجد):
---
{file_context}

**خطوات رحلة الوكيل بالتفصيل:**
1️⃣ **المرحلة الأولى (التعرف):** اسأل المستخدم عن: العمر، والهدف المالي...
2️⃣ **المرحلة الثانية (التوعية والتعليم):** اشرح له باختصار فائدة تخصيص نسبة للذهب...
3️⃣ **المرحلة الثالثة (المحاكي الافتراضي):** خذ المبلغ الذي حدده، وطبق عليه محاكاة توزيع الأصول...
4️⃣ **المرحلة الرابعة (تقرير الجاهزية):** اعرض له تقرير الجاهزية (درجة من 100)...
5️⃣ **المرحلة الخامسة (الترشيح والربط):** ترشيح المؤسسة العُمانية الأنسب...

⛔ **قاعدة الحظر:** ارفض أي أسئلة خارج نطاق المال والاستثمار.
"""

    # 2. طباعة ملخص النتائج للمستخدم فقط (إذا كان متوفراً)
    if 'summary_md' in locals() and summary_md:
        st.markdown(summary_md, unsafe_allow_html=True)

    st.sidebar.divider()
    st.sidebar.subheader("📈 محاكي نمو أرباح الاستثمار")

    # معادلة الفائدة المركبة البسيطة للنمو
    future_value = capital * ((1 + (expected_return / 100)) ** years)
    profit = future_value - capital

    st.sidebar.info(f"""
📈 **النمو المتوقع بعد {years} سنوات:**
- **المبلغ النهائي المتوقع:** {future_value:,.2f} ر.ع
- **صافي الأرباح المتوقعة:** {profit:,.2f} ر.ع
""")


# --- 2. شارة حالة الربط المباشر مع المؤسسة ---
if consent and user_name and user_phone and user_email:
    st.sidebar.markdown("""
<div style="background-color: #064e3b; border: 1px solid #10b981; border-radius: 8px; padding: 10px; margin-top: 10px; text-align: center;">
<span style="color: #34d399; font-weight: bold; font-size: 14px;">
📡 حالة الربط: مُتصل بالمؤسسة
</span>
<p style="color: #a7f3d0; font-size: 11px; margin: 4px 0 0 0;">
تم تجهيز وإرسال ملف البيانات والتفويض إلى الوسيط المعتمد في بورصة مسقط.
</p>
</div>
""", unsafe_allow_html=True)


if st.button("🗑️ مسح المحادثة والبدء من جديد"):
    st.session_state.messages = []
    st.rerun() 

try:
    supabase_module = importlib.import_module("supabase")
    create_client = supabase_module.create_client
    Client = getattr(supabase_module, "Client", None)
except ImportError:
    create_client = None
    Client = None
    st.error("مكتبة supabase غير مثبتة. يرجى تثبيتها لتفعيل حفظ البيانات.")

# --- 1. إعداد الاتصال بقاعدة البيانات Supabase ---
# استبدلي هذه القيم بـ (URL و API Key) الخاصة بمشروعك في Supabase Dashboard -> Settings -> API
SUPABASE_URL = "https://ndybefityrnplutoilzv.supabase.co"
SUPABASE_KEY = "sb_publishable_4Sx4Y6FY1rVAugdcpsGbVw_Gebiz_NU"
# اختبار الاتصال بقاعدة البيانات

@st.cache_resource
def init_supabase():
    if create_client is None:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase = init_supabase()
    if supabase is None:
        raise ImportError("supabase library not available")
except Exception:
    st.error("تعذر الاتصال بقاعدة البيانات")
    supabase = None

# --- 2. دالة حفظ بيانات المستثمر ---
def save_investor_data(name, phone, email, capital, consent):
    try:
        if supabase is None:
            return False, "Supabase client غير متوفر"

        data = {
            "Name": str(name) if name else "بدون اسم",
            "Phone": str(phone) if phone else "بدون رقم",
            "Email": str(email) if email else "بدون إيميل",
            "capital": int(capital) if capital else 0,
            "consent": bool(consent)
        }

        response = supabase.table("investors").insert(data).execute()
        return True, response

    except Exception as e:
        return False, str(e)


            
