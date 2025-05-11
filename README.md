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


readme_md = """
# 🚀 Welcome to **Docfactory** – Your Smart Document Generator

**Docfactory** helps you generate project-specific Solution Proposals, Cloud Readiness Assessments (CRA), or Statements of Work (SOW) by filling dynamic placeholders in `.docx` and `.pptx` templates with your own content.

🔗 **Live App**: [Launch Docfactory](https://docfactory-dzoan.streamlit.app/#smart-placeholder-filler-for-docx-and-pptx)

---

## 🧠 How It Works

1. **Start the App**  
   Open the Docfactory app at the link above.

2. **Upload Your Template**  
   Use your company’s `.docx`, `.dotx`, or `.pptx` document with `{placeholders}` in the content.

3. **Fill In Placeholders**  
   For each detected placeholder, you can:
   - Upload a content file (e.g., `.txt`, `.xlsx`, `.jpg`)
   - Or manually type/paste the content

4. **Use Sample Files for Testing**  
   To get started quickly, use the pre-filled sample files from the folder:  
   📁 `placeholder_samples.zip` (includes `.txt`, `.xlsx`, and `.jpg`)

5. **Generate and Download**  
   Once all fields are filled, click **🛠 Generate Document** to download your customized `.docx` or `.pptx`.

6. **Swap with Real Inputs**  
   After testing, simply upload your **real customer-specific** files and regenerate your final proposal or report!

---

## 📦 Example Placeholders & Supported Formats

| Placeholder                          | Supported File Types                    |
|--------------------------------------|-----------------------------------------|
| `{EXECSUM}`                          | `.docx`, `.txt`, `.xlsx`, `.pptx`, `.jpg`, `.png` |
| `{PROJECT OVERVIEW}`                | `.docx`, `.txt`, `.xlsx`, `.pptx`, `.jpg`, `.png` |
| `{Scope}`                            | `.docx`, `.txt`, `.xlsx`, `.pptx`, `.jpg`, `.png` |
| `{TargetArchDiag}`                  | `.jpg`, `.png` *(diagram preferred)*     |
| `{DECISION_MATRIX_TABLE}`           | `.xlsx`, `.csv`, `.docx` *(table)*       |
| `{SLA_APPS_table}`                  | `.xlsx` *(RTO/RPO per app)*              |
| `{Gov_Diagram}`                     | `.jpg`, `.png` *(diagram)*               |
| `{Rackspace Support Services}`      | `.docx`, `.txt` *(free text)*            |
| `{TCO_GRAPH}`                       | `.jpg`, `.png` *(graph image)*           |
| `{APP_MIG_TABLE}`                   | `.xlsx` *(migration plan)*               |
| `{Soft_req_table}`                 | `.xlsx` *(software specs)*               |
| `{Audit tools}`                    | `.txt`, `.xlsx` *(tool list)*            |
| `{Custom_OpenStack_Components}`    | `.txt` *(bullet list)*                   |

*...and many more placeholders supported.*

---

## 🧪 Pro Tip

> For diagrams or screenshots, use **JPG or PNG** format.  
> If image upload fails, paste a description instead or embed the image in a Word document and upload that.

---

## 📁 Getting Started with Sample Files

Download this starter pack:  
🎁 [placeholder_samples.zip](sandbox:/mnt/data/placeholder_samples)

Includes:
- `.txt` files for each text block
- `.xlsx` tables for RTO, TCO, software
- `.jpg` diagrams for architecture and governance

Use these to test your first Factory-generated document in minutes!
"""


📃 License
MIT License © 2024 Dzoan Tran
