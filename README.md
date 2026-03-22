📚 Smart Library System
🏗 Oil Training Institute – Baghdad
________________________________________
🌟 Overview
The Smart Library System is a web-based platform designed to help students of the Oil Training Institute in Baghdad easily access and browse their academic books in a structured way.
The system organizes books based on:
Stage → Department → Specialization → Books
It also integrates AI-powered features to enhance the learning experience.
________________________________________
🎯 Features
•	📚 Structured navigation of books
•	🌐 Access books online directly
•	📂 Integration with Google Drive for storage
•	🤖 AI Smart Summarization
o	Select specific pages
o	Generate intelligent summaries
o	Download the summary result
•	⚡ Simple and user-friendly interface
________________________________________
🤖 AI Smart Summarization
The system provides an advanced feature that allows students to:
•	Select a range of pages from the book
•	Generate an intelligent summary using AI
•	Download the summarized content
This feature helps students save time and focus on important concepts.
________________________________________
📸 Screenshots
🏠 Main Interface
![Main](https://github.com/Eman1351975/smart-library/raw/main/main.png)
 
🤖 AI Summarization
![AI](https://github.com/Eman1351975/smart-library/raw/main/ai.png)

________________________________________
🚀 Live Demo
(If available)
👉 https://your-render-link.onrender.com
________________________________________
🛠 Technologies Used
•	Python 🐍
•	Streamlit
•	PyPDF2
•	Groq API
•	Google Drive API
________________________________________
⚙️ How to Run Locally
1.	Clone the repository:
git clone https://github.com/Eman1351975/smart-library.git
cd smart-library
2.	Install dependencies:
pip install -r requirements.txt
3.	Set the environment variables:
•	GROQ_API_KEY
•	GOOGLE_DRIVE_API_KEY
•	GOOGLE_DRIVE_FOLDER_ID
4.	Run the application:
streamlit run app.py
________________________________________
🔐 Environment Variables
The project depends on external services and requires the following environment variables:
•	GROQ_API_KEY → Used for AI summarization
•	GOOGLE_DRIVE_API_KEY → Used to access files
•	GOOGLE_DRIVE_FOLDER_ID → Main folder ID of the library
________________________________________
☁️ Storage Note
Books are not stored داخل المشروع بسبب حجمها الكبير.
Instead, they are stored externally using Google Drive, and the application dynamically loads them during runtime.
________________________________________
📁 Google Drive Structure
The system expects a structured folder like:
Main Folder
├── المرحلة الأولى
│   ├── قسم الميكاميك
│   │   ├── اللحام
│  │   │   ├── كتاب1.pdf
│  │   │   ├── كتاب2.pdf
│   ├── قسم النفط
│   │   ├── الانتاج
│   │   │   ├── كتاب1.pdf
│  │   │    ├── كتاب2.pdf
├── المرحلة الثانية
________________________________________
🧪 Testing
Basic functionality has been tested manually to ensure system stability and correctness.
________________________________________
👩‍💻 Developed By
Eman Adil Jasim
________________________________________
⚠️ License
This project is licensed under the MIT License.
________________________________________

