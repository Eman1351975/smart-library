# Developed by: Eman Adil Jasim - معهد التدريب النفطي / بغداد

import streamlit as st
import os
import requests
from io import BytesIO
from groq import Groq
from PyPDF2 import PdfReader

# =========================
# الإعدادات الأساسية
# =========================
st.set_page_config(page_title="المكتبة الذكية - معهد نفط بغداد", layout="wide")
st.title("🏗   المكتبة الذكية لمناهج - معهد التدريب النفطي / بغداد - تصميم المبرمجة ايمان عادل جاسم")

import streamlit as st

st.markdown("""
<div style="
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #d4af37;
    padding: 10px 0 20px 0;
    font-family: 'Arial', sans-serif;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
">
    ✨ مكتبة إيمان الذكية ✨
</div>
""", unsafe_allow_html=True)



# مفاتيح البيئة
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GOOGLE_DRIVE_API_KEY = os.environ.get("GOOGLE_DRIVE_API_KEY")
GOOGLE_DRIVE_FOLDER_ID = os.environ.get("GOOGLE_DRIVE_FOLDER_ID", "1J5wDeX_xPMC4BYi-in5k35uSovF2ociC")

# عميل Groq
client = Groq(api_key=GROQ_API_KEY)

# =========================
# الهيكلية الإدارية
# =========================
STRUCTURE = {
    "المرحلة الأولى": {
        "قسم الميكانيك": [
            "تقنيات اللحام الغازي والكهربائي",
            "تقنيات الصحة والسلامة والبيئة",
            "المكائن والمعدات الثقيلة",
            "المضخات والتوربينات",
            "ميكانيك المعدات النفطية الثابتة",
            "تقنية خطوط الانابيب"
        ],
        "قسم النفط": [
            "حفر الابار النفطية",
            "الانتاج والقياسات الحقلية"
        ],
        "قسم التصفية": [
            "التشغيل والسيطرة",
            "تقنية الغاز",
            "التحليلات النفطية"
        ],
        "قسم الكهرباء": [
            "كهرباء المعدات النفطية",
            "القياس والسيطرة"
        ]
    },
    "المرحلة الثانية": {
        "قسم الميكانيك": [
            "تقنيات اللحام الغازي والكهربائي",
            "تقنيات الصحة والسلامة والبيئة",
            "المكائن والمعدات الثقيلة",
            "المضخات والتوربينات",
            "ميكانيك المعدات النفطية الثابتة",
            "تقنية خطوط الانابيب"
        ],
        "قسم النفط": [
            "حفر الابار النفطية",
            "الانتاج والقياسات الحقلية"
        ],
        "قسم التصفية": [
            "التشغيل والسيطرة",
            "تقنية الغاز",
            "التحليلات النفطية"
        ],
        "قسم الكهرباء": [
            "كهرباء المعدات النفطية",
            "القياس والسيطرة"
        ]
    }
}

# =========================
# دوال Google Drive
# =========================
@st.cache_data(ttl=300)
def list_drive_files(parent_id):
    """
    جلب الملفات والمجلدات داخل مجلد معين من Google Drive
    """
    url = "https://www.googleapis.com/drive/v3/files"
    params = {
        "q": f"'{parent_id}' in parents and trashed=false",
        "fields": "files(id,name,mimeType)",
        "pageSize": 1000,
        "key": GOOGLE_DRIVE_API_KEY
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json().get("files", [])


@st.cache_data(ttl=300)
def get_child_folder_id(parent_id, folder_name):
    """
    إيجاد ID لمجلد فرعي بالاسم
    """
    items = list_drive_files(parent_id)
    for item in items:
        if (
            item["mimeType"] == "application/vnd.google-apps.folder"
            and item["name"].strip() == folder_name.strip()
        ):
            return item["id"]
    return None


@st.cache_data(ttl=300)
def get_books_in_folder(folder_id):
    """
    جلب ملفات PDF فقط من داخل مجلد الاختصاص
    """
    if not folder_id:
        return []

    items = list_drive_files(folder_id)
    pdfs = []
    for item in items:
        if item["mimeType"] == "application/pdf" or item["name"].lower().endswith(".pdf"):
            pdfs.append(item)
    return pdfs


def get_drive_preview_url(file_id):
    return f"https://drive.google.com/file/d/{file_id}/preview"


def get_drive_download_url(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"


def download_pdf_bytes(file_id):
    """
    تنزيل ملف PDF كبيانات ثنائية لاستخراج النص
    """
    url = get_drive_download_url(file_id)
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.content


# =========================
# الشريط الجانبي
# =========================
with st.sidebar:
    st.header("📂 لوحة التحكم الإدارية")

    sel_stage = st.selectbox("اختر المرحلة:", list(STRUCTURE.keys()))
    sel_dept = st.selectbox("اختر القسم:", list(STRUCTURE[sel_stage].keys()))
    sel_spec = st.selectbox("اختر الاختصاص الدقيق:", STRUCTURE[sel_stage][sel_dept])

    st.markdown("---")
    st.info("📌 الكتب تُقرأ الآن مباشرة من Google Drive")
    st.caption("إذا أضفتِ كتبًا جديدة إلى نفس مجلد الاختصاص في Google Drive ستظهر هنا تلقائيًا.")

# =========================
# تحديد المجلدات من Google Drive
# =========================
stage_id = get_child_folder_id(GOOGLE_DRIVE_FOLDER_ID, sel_stage)
dept_id = get_child_folder_id(stage_id, sel_dept) if stage_id else None
spec_id = get_child_folder_id(dept_id, sel_spec) if dept_id else None

# =========================
# الواجهة الرئيسية
# =========================
st.info(f"📍 أنت الآن في: {sel_stage} ⬅️ {sel_dept} ⬅️ {sel_spec}")

if not GOOGLE_DRIVE_API_KEY:
    st.error("لم يتم العثور على GOOGLE_DRIVE_API_KEY في متغيرات البيئة داخل Render.")
    st.stop()

if not stage_id:
    st.warning(f"لم يتم العثور على مجلد المرحلة: {sel_stage}")
    st.stop()

if not dept_id:
    st.warning(f"لم يتم العثور على مجلد القسم: {sel_dept}")
    st.stop()

if not spec_id:
    st.warning(f"لم يتم العثور على مجلد الاختصاص: {sel_spec}")
    st.stop()

available_books = get_books_in_folder(spec_id)

if available_books:
    book_names = [book["name"] for book in available_books]
    selected_book_name = st.selectbox("اختر المنهج الدراسي المراد عرضه:", book_names)

    selected_book = next((b for b in available_books if b["name"] == selected_book_name), None)

    if selected_book:
        file_id = selected_book["id"]

        # معاينة الكتاب
        st.markdown("### 📖 تصفح الكتاب")
        preview_url = get_drive_preview_url(file_id)
        st.components.v1.iframe(preview_url, width=900, height=600, scrolling=True)

        st.markdown("---")
        st.markdown("### 🤖 مساعد التلخيص الذكي")

        c1, c2 = st.columns(2)
        with c1:
            s_p = st.number_input("من صفحة", min_value=1, value=1)
        with c2:
            e_p = st.number_input("إلى صفحة", min_value=1, value=3)

        user_req = st.text_area(
            "ما هو سؤالك حول هذا الجزء؟",
            "لخص النقاط الأساسية في هذا الجزء من المنهج."
        )

        if st.button("⚡️ تنفيذ التحليل"):
            with st.spinner("جاري تحميل الكتاب وتحليل الصفحات..."):
                extracted_text = ""

                try:
                    pdf_bytes = download_pdf_bytes(file_id)
                    reader = PdfReader(BytesIO(pdf_bytes))

                    total_pages = len(reader.pages)
                    start_page = max(1, s_p)
                    end_page = min(e_p, total_pages)

                    for i in range(start_page - 1, end_page):
                        content = reader.pages[i].extract_text()
                        if content:
                            extracted_text += content + "\n"

                    if not extracted_text.strip():
                        st.warning("لم يتم استخراج نص من الصفحات المحددة. قد يكون الملف صورة ممسوحة ضوئيًا.")
                    else:
                        res = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "system",
                                    "content": f"أنت مساعد أكاديمي في معهد النفط. التخصص الحالي: {sel_spec}."
                                },
                                {
                                    "role": "user",
                                    "content": f"حلل المنهج التالي:\n{extracted_text}\n\nالطلب: {user_req}"
                                }
                            ],
                            model="llama-3.3-70b-versatile",
                        )

                        ans = res.choices[0].message.content
                        st.success("✅ تم التحليل!")
                        st.info(ans)

                        st.download_button(
                            "📥 تحميل النتيجة",
                            data=ans,
                            file_name="summary.txt",
                            mime="text/plain"
                        )

                except Exception as e:
                    st.error(f"حدث خطأ أثناء قراءة الكتاب أو التحليل: {e}")

else:
    st.warning("المكتبة فارغة لهذا الاختصاص حالياً.")

# =========================
# التذييل
# =========================
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