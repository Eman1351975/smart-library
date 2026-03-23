# 📚 Smart Library System

### 🏗 Oil Training Institute – Baghdad

---

## 🌟 Overview

The **Smart Library System** is a web-based platform designed to help students of the Oil Training Institute in Baghdad easily access and browse their academic books in a structured way.

The system organizes books based on:
**Stage → Department → Specialization → Books**

It also integrates **AI-powered features** to enhance the learning experience.

---

## 🎯 Features

* 📚 Structured navigation of books
* 🌐 Access books online directly
* 📂 Integration with Google Drive for storage
* 🤖 **AI Smart Summarization**

  * Select specific pages
  * Generate intelligent summaries
  * Download the summary result
* ⚡ Simple and user-friendly interface

---

## 🤖 AI Smart Summarization

The system provides an advanced feature that allows students to:

* Select a range of pages from the book
* Generate an intelligent summary using AI
* Download the summarized content

This feature helps students save time and focus on important concepts.

---

## 📸 Screenshots

### 🏠 Main Interface

![Main](https://github.com/Eman1351975/smart-library/raw/main/main.png)


### 🤖 AI Summarization
![AI](https://github.com/Eman1351975/smart-library/raw/main/ai.png)

---

## 🚀 Live Demo

(If available)
👉  https://smart-library-oqb1.onrender.com/


---

## 🛠 Technologies Used

* Python 🐍
* Streamlit
* PyPDF2
* Groq API
* Google Drive API

---

## ⚙️ How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/Eman1351975/smart-library.git
cd smart-library
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set the environment variables:

* `GROQ_API_KEY`
* `GOOGLE_DRIVE_API_KEY`
* `GOOGLE_DRIVE_FOLDER_ID`

4. Run the application:

```bash
streamlit run app.py
```

---

## 🔐 Environment Variables

The project depends on external services and requires the following environment variables:

* **GROQ_API_KEY** → Used for AI summarization
* **GOOGLE_DRIVE_API_KEY** → Used to access files
* **GOOGLE_DRIVE_FOLDER_ID** → Main folder ID of the library

---

## ☁️ Storage Note

Books are **not stored داخل المشروع** بسبب حجمها الكبير.

Instead, they are stored externally using **Google Drive**, and the application dynamically loads them during runtime.

---
## 📁 Google Drive Structure

The system expects a structured Google Drive folder like:

Main Folder

├── المرحلة الأولى
│   ├── قسم الميكانيك
│   │   ├── تقنيات اللحام الغازي والكهربائي
│   │   │   ├── كتاب1.pdf
│   │   │   ├── كتاب2.pdf
│   │   ├── التشغيل والسيطرة
│   │   │   ├── كتاب1.pdf
│   │   │   ├── كتاب2.pdf
│   │   ├── الانتاج والقياسات الحقلية
│   │       ├── كتاب1.pdf
│   │       ├── كتاب2.pdf
├── المرحلة الثانية


---

---

## 🧪 Testing

Basic functionality has been tested manually to ensure system stability and correctness.

---

## 👩‍💻 Developed By

**Eman Adil Jasim**

---

## ⚠️ License

This project is licensed under the MIT License.

---
