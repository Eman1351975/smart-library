import streamlit as st
import os
from groq import Groq
from PyPDF2 import PdfReader
from streamlit_pdf_viewer import pdf_viewer

# --- الإعدادات الأساسية ---
st.set_page_config(page_title="المكتبة الذكية - معهد نفط بغداد", layout="wide")
st.title("🏗️ المكتبة الذكية لمناهج - معهد التدريب النفطي / بغداد")

# 🔑 المفتاح الخاص بك (Groq)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

# --- تعريف الهيكلية الإدارية للأقسام والاختصاصات ---
STRUCTURE = {
    "المرحلة الأولى": {
        "قسم الميكانيك": ["تقنيات اللحام الغازي والكهربائي", "تقنيات الصحة والسلامة والبيئة", "المكائن والمعدات الثقيلة", "المضخات والتوربينات", "ميكانيك المعدات النفطية الثابتة", "تقنية خطوط الانابيب"],
        "قسم النفط": ["حفر الابار النفطية", "الانتاج والقياسات الحقلية"],
        "قسم التصفية": ["التشغيل والسيطرة", "تقنية الغاز", "التحليلات النفطية"],
        "قسم الكهرباء": ["كهرباء المعدات النفطية", "القياس والسيطرة"]
    },
    "المرحلة الثانية": {
        "قسم الميكانيك": ["تقنيات اللحام الغازي والكهربائي", "تقنيات الصحة والسلامة والبيئة", "المكائن والمعدات الثقيلة", "المضخات والتوربينات", "ميكانيك المعدات النفطية الثابتة", "تقنية خطوط الانابيب"],
        "قسم النفط": ["حفر الابار النفطية", "الانتاج والقياسات الحقلية"],
        "قسم التصفية": ["التشغيل والسيطرة", "تقنية الغاز", "التحليلات النفطية"],
        "قسم الكهرباء": ["كهرباء المعدات النفطية", "القياس والسيطرة"]
    }
}

BASE_DIR = "institute_library"

# إنشاء المجلدات تلقائياً حسب الهيكلية
for stage, depts in STRUCTURE.items():
    for dept, specialties in depts.items():
        for spec in specialties:
            path = os.path.join(BASE_DIR, stage, dept, spec)
            if not os.path.exists(path):
                os.makedirs(path)

# --- القائمة الجانبية (Sidebar) للتنقل والرفع ---
with st.sidebar:
    st.header("📂 لوحة التحكم الإدارية")
    
    # الاختيارات المتسلسلة
    sel_stage = st.selectbox("اختر المرحلة:", list(STRUCTURE.keys()))
    sel_dept = st.selectbox("اختر القسم:", list(STRUCTURE[sel_stage].keys()))
    sel_spec = st.selectbox("اختر الاختصاص الدقيق:", STRUCTURE[sel_stage][sel_dept])
    
    st.markdown("---")
    st.subheader(f"📤 رفع كتاب لـ {sel_spec}")
    uploaded_file = st.file_uploader("اختر ملف PDF", type="pdf")
    
    if st.button("حفظ في الأرشيف"):
        if uploaded_file:
            save_path = os.path.join(BASE_DIR, sel_stage, sel_dept, sel_spec, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"تم حفظ الكتاب في أرشيف {sel_spec}")
        else:
            st.warning("يرجى اختيار ملف.")

# --- الواجهة الرئيسية ---
st.info(f"📍 أنت الآن في: {sel_stage} ⬅️ {sel_dept} ⬅️ {sel_spec}")

current_path = os.path.join(BASE_DIR, sel_stage, sel_dept, sel_spec)
available_books = [f for f in os.listdir(current_path) if f.endswith('.pdf')]

if available_books:
    selected_book = st.selectbox("اختر المنهج الدراسي المراد عرضه:", available_books)
    book_full_path = os.path.join(current_path, selected_book)

    # 📖 معاينة الكتاب
    st.markdown("### 📖 تصفح الكتاب")
    with st.expander("فتح القارئ المباشر", expanded=True):
        pdf_viewer(book_full_path, width=800, height=500)

    st.markdown("---")
    st.markdown("### 🤖 مساعد التلخيص الذكي")
    
    c1, c2 = st.columns(2)
    with c1: s_p = st.number_input("من صفحة", min_value=1, value=1)
    with c2: e_p = st.number_input("إلى صفحة", min_value=1, value=3)
    
    user_req = st.text_area("ما هو سؤالك حول هذا الجزء؟", "لخص النقاط الأساسية في هذا الجزء من المنهج.")

    if st.button("⚡ تنفيذ التحليل"):
        with st.spinner("جاري المعالجة..."):
            extracted_text = ""
            try:
                reader = PdfReader(book_full_path)
                for i in range(s_p-1, min(e_p, len(reader.pages))):
                    content = reader.pages[i].extract_text()
                    if content: extracted_text += content + "\n"
            except Exception as e: st.error(f"خطأ في القراءة: {e}")

            if extracted_text.strip():
                try:
                    res = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": f"أنت مساعد أكاديمي في معهد النفط. التخصص الحالي: {sel_spec}."},
                            {"role": "user", "content": f"حلل المنهج:\n{extracted_text}\n\nالطلب: {user_req}"}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    ans = res.choices[0].message.content
                    st.success("✅ تم التحليل!")
                    st.info(ans)
                    
                    st.download_button("📥 تحميل النتيجة", data=ans, file_name="summary.txt")
                except Exception as e: st.error(f"خطأ API: {e}")
else:
    st.warning("المكتبة فارغة لهذا الاختصاص حالياً.")

# --- التذييل الرسمي (تصميم ست ايمان) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #1f4e79; padding: 15px; font-size: 16px; font-weight: bold; background-color: #f0f2f6; border-radius: 10px;">
        معهد التدريب النفطي / بغداد - نظام المكتبة الذكية 2026 - تصميم المبرمجة : ايمان عادل العكيلي / رئيس مبرمجين اقدم اول
    </div>
    """, 
    unsafe_allow_html=True
)