import streamlit as st
import numpy as np
try:
    import faiss  # type: ignore[import-not-found]
except ImportError:
    faiss = None
from openai import OpenAI

# 1. إعداد عنوان الصفحة وشكل الواجهة
st.set_page_config(page_title="مرشد الاستثمار الذكي (RAG)", page_icon="🤖", layout="centered")

st.title("🤖 مرشد الاستثمار الذكي (المدعوم بـ RAG)")
st.write("أهلاً بك! أنا مرشدك الذكي، أعتمد على قاعدة معرفية موثوقة لمساعدتك في الاستثمار فقط.")

# 2. إعداد عميل OpenAI
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

# 3. بناء القاعدة المعرفية الموثوقة (Knowledge Base)
investment_knowledge = [
    # بيانات المشاريع المتاحة
    "مشروع SME-001: مخبز وحلويات سحابية | قطاع الأغذية | الحد الأدنى للاستثمار: 500 ريال | العائد المتوقع: 12-18% | المخاطرة: منخفضة إلى متوسطة.",
    "مشروع SME-002: متجر إلكتروني للمستلزمات الرياضية | تجارة إلكترونية | الحد الأدنى للاستثمار: 1500 ريال | العائد المتوقع: 15-25% | المخاطرة: متوسطة.",
    "مشروع SME-003: تطبيق إدارة المخزون للمتاجر | تكنولوجيا وذكاء اصطناعي | الحد الأدنى للاستثمار: 3000 ريال | العائد المتوقع: 20-35% | المخاطرة: عالية.",
    # قواعد واستراتيجيات الاستثمار الموثوقة
    "قاعدة إدارة المخاطر: لا تستثمر أبداً أموال الطوارئ أو الأموال التي تحتاجها في المدى القريب (أقل من 6 أشهر).",
    "التنويع الاستثماري: يُفضل توزيع رأس المال على أكثر من مجال للحد من الخسائر (مثل وضع جزء في مخاطرة منخفضة وجزء في مخاطرة متوسطة).",
    "العائد والمخاطرة: توجد علاقة طردية دائماً؛ كلما زاد العائد المتوقع زادت نسبة المخاطرة، ولا يوجد استثمار آمن بنسبة 100% بعائد مرتفع.",
    "الأخطاء الشائعة: الاندفاع خلف العوائد المرتفعة السريعة دون دراسة جدوى، وتوظيف كل رأس المال في مشروع واحد.",
    "خطوات البدء للاستثمار للمبتدئين: 1) تحديد صندوق الطوارئ أولاً، 2) تحديد الميزانية المتاحة للاستثمار، 3) اختيار المدى الزمني والمخاطرة المناسبة."
]

# 4. دالة لتحويل النصوص إلى Embeddings وبناء فهرس FAISS للبحث السريع
@st.cache_resource
def build_rag_index():
    embeddings = []
    for doc in investment_knowledge:
        res = client.embeddings.create(
            input=doc,
            model="text-embedding-3-small"
        )
        embeddings.append(res.data[0].embedding)

    embeddings_np = np.array(embeddings).astype('float32')
    if faiss is not None:
        dimension = embeddings_np.shape[1]
        # إنشاء فهرس البحث في FAISS
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings_np)
        return index, embeddings_np

    return None, embeddings_np

# بناء الفهرس
with st.spinner("جاري تحميل القاعدة المعرفية الموثوقة..."):
    index, embeddings_np = build_rag_index()

# دالة استرجاع المعلومات ذات الصلة (Retrieval)
def retrieve_relevant_docs(query, top_k=2):
    res = client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    query_vec = np.array([res.data[0].embedding]).astype('float32')

    if index is not None:
        distances, indices = index.search(query_vec, top_k)
    else:
        distances = np.linalg.norm(embeddings_np - query_vec, axis=1)
        indices = np.argsort(distances)[:top_k][np.newaxis, :]

    retrieved_context = [investment_knowledge[i] for i in indices[0]]
    return "\n".join(retrieved_context)

# 5. حفظ سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. استقبال مدخلات المستخدم واستخدام الـ RAG
if prompt := st.chat_input("اكتب سؤالك الاستثماري هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # خطوة الـ Retrieval: استرجاع السياق الموثوق بناءً على سؤال المستخدم
            context = retrieve_relevant_docs(prompt)
            # صياغة الـ System Prompt الصارم المعتمد على الـ RAG فقط
            system_instruction = f"""
أنت "مرشد الاستثمار الذكي". وظيفتك الإجابة عن الأسئلة الاستثمارية المباشرة فقط وتوجيه المستثمرين.

قواعدك الصارمة جداً:
1. اعتمد بشكل أساسي ومباشر على المراجع الاستثمارية التالية المأخوذة من القاعدة المعرفية:
---
{context}
---
2. إذا كان سؤال المستخدم خارج نطاق الاستثمار أو إدارة الأموال أو المشاريع (مثل الأسئلة العامة أو الطب أو البرمجة أو غيرها)، اعتذر منه بلباقة واذكر: "أنا مرشد استثماري متخصص في مجال الاستثمار والمشاريع فقط، كيف يمكنني مساعدتك في ميزانيتك الاستثمارية اليوم؟".
3. لا تقم بتأليف معلومات أو تقديم نصائح مالية غير موجودة أو غير مدعومة بالأسس المذكورة أعلاه.
4. حافظ على أسلوب مشجع، واضح، ومباشر.
"""
            # تجهيز الرسائل للنموذج
            api_messages = [{"role": "system", "content": system_instruction}]
            for m in st.session_state.messages:
                api_messages.append({"role": m["role"], "content": m["content"]})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages,
                temperature=0.2 # درجة حرارة منخفضة لضمان الالتزام بالسياق
            )

            full_response = response.choices[0].message.content
            message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"حدث خطأ: {e}")
