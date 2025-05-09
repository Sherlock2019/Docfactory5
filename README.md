# 📄 DocAutoFactory


Smart Placeholder Filler for DOCX & PPTX
A flexible Streamlit app that lets you dynamically fill placeholders in Word or PowerPoint templates using uploaded content or manual inputs — with support for images, Excel tables, text, and more.

🚀 Features
✅ Upload .docx or .pptx templates with {placeholders}

✅ Detects all {placeholders} automatically

✏️ Supports manual input for key fields like {CUSTOMER_NAME}, {CITY NAME}, etc.

📎 Upload files to fill each placeholder:

.docx, .txt, .pptx → inserted as extracted text

.xlsx → inserted as Word table

.jpg, .png → embedded image

🛠 Only generates document when you click "Generate Document"

📥 Outputs a clean .docx or .pptx file with replaced values

📌 Works offline, fully open-source, and extensible

🧩 Example Use Case
Upload a Word proposal template like:

Dear {CUSTOMER_NAME},

Attached is the network overview for {CITY NAME}:

{NETWORK_DIAGRAM}

Here is the proposed resource table:

{NET_ALLOCATION_TABLE}


And generate:

Images in place of {NETWORK_DIAGRAM}

Excel data in place of {NET_ALLOCATION_TABLE}

Customer and city names replaced via input

📂 Supported File Formats per Placeholder
Format	Behavior
.txt	Extracts and inserts plain text
.docx	Extracts paragraph text
.pptx	Extracts text from slides
.xlsx	Inserts as a fully formatted table
.jpg/.png	Embeds image into the document

🛠 Getting Started

🛠 Getting Started
🔧 Install requirements

pip install -r requirements.txt
▶️ Run the app

streamlit run streamlit_app.py
🗃 Requirements
nginx
Copy
Edit
streamlit
python-docx
python-pptx
pandas
openpyxl
Pillow
📌 Customization
To handle a placeholder as text-only input, just add it to the list:

TEXT_ONLY_PLACEHOLDERS = {
    "CUSTOMER_NAME", "CITY NAME", "SA-NAME", "SA_EMAIL", "RAX_TEAM", "PARTNER_NAME"
}

📃 License
MIT License © 2024 Dzoan Tran
