import streamlit as st
from docx import Document
from pptx import Presentation
import pandas as pd
import re
from io import BytesIO
from datetime import date

st.set_page_config(page_title="🧩 Placeholder Filler", layout="wide")
st.title("📄📊 Dynamic Placeholder Filler for DOCX & PPTX")

# 🚀 Quick Start Guide
with st.expander("ℹ️ Quick Steps to Use This App", expanded=True):
    st.markdown("""
    1. **Upload your template** (.docx or .pptx) containing `{placeholders}`.
    2. The app will **automatically detect all placeholders** like `{CUSTOMER_NAME}`, `{PROJECT OVERVIEW}`, etc.
    3. For each placeholder:
       - If it's a short field like `{CUSTOMER_NAME}`, enter it directly in the text box.
       - For others, you can either **upload a file** (`.txt`, `.docx`, `.xlsx`) or **type the value** manually.
    4. Once all placeholders are filled, the app will generate a final Word or PowerPoint file.
    5. **Download the result** using the provided button. The file will be named like:  
       `CustomerName.TypeOfDoc.Date.docx`
    """)

# ✏️ Placeholders that should only use text input
TEXT_ONLY_PLACEHOLDERS = {
    "CUSTOMER_NAME", "CITY NAME", "SA-NAME", "SA_EMAIL", "RAX_TEAM", "PARTNER_NAME"
}

# Upload template
template_file = st.file_uploader("📁 Upload a .docx or .pptx template", type=["docx", "pptx"])
customer_name = st.text_input("👤 Customer Name")
doc_type = st.selectbox("🧾 Type of Document", ["Proposal", "Report", "Migration Plan", "Review"])
today = date.today().strftime("%Y%m%d")

if template_file and customer_name:
    is_docx = template_file.name.endswith(".docx")
    is_pptx = template_file.name.endswith(".pptx")
    text_blocks = []

    # Extract text from the template
    if is_docx:
        doc = Document(template_file)
        text_blocks = [para.text for para in doc.paragraphs]
    elif is_pptx:
        prs = Presentation(template_file)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text_blocks.append(shape.text)

    # Detect placeholders
    full_text = "\n".join(text_blocks)
    placeholders = list(dict.fromkeys(re.findall(r"\{[^}]+\}", full_text)))
    st.markdown("### 🔍 Detected Placeholders")
    st.write(placeholders)

    uploads = {}

    # Step 1: Show only text input placeholders at the top
    if any(ph.strip("{}") in TEXT_ONLY_PLACEHOLDERS for ph in placeholders):
        st.markdown("### ✏️ Enter Values for Key Fields")
        for ph in placeholders:
            base_ph = ph.strip("{}")
            if base_ph in TEXT_ONLY_PLACEHOLDERS:
                clean_key = base_ph.replace(" ", "_")
                manual = st.text_input(f"✏️ {ph}", key=f"text_{clean_key}")
                if manual.strip():
                    uploads[ph] = manual.strip()

    # Step 2: Show upload + manual fields for remaining placeholders
    st.markdown("### 📎 Upload Files or Enter Text for Remaining Placeholders")
    for ph in placeholders:
        base_ph = ph.strip("{}")
        if base_ph not in TEXT_ONLY_PLACEHOLDERS:
            clean_key = base_ph.replace(" ", "_")
            col1, col2 = st.columns(2)
            with col1:
                file = st.file_uploader(f"📎 Upload file for {ph}", type=["txt", "docx", "xlsx"], key=clean_key)
            with col2:
                manual = st.text_area(f"✏️ Or manually enter value for {ph}", height=100, key=f"text_{clean_key}")

            content = ""
            if file:
                if file.name.endswith(".txt"):
                    content = file.read().decode("utf-8")
                elif file.name.endswith(".docx"):
                    d = Document(file)
                    content = "\n".join([p.text for p in d.paragraphs])
                elif file.name.endswith(".xlsx"):
                    df = pd.read_excel(file)
                    content = df.to_string(index=False)
            elif manual.strip():
                content = manual.strip()

            if content:
                uploads[ph] = content

    # Step 3: Replace placeholders and generate download
    if uploads:
        final_filename = f"{customer_name}_{doc_type.replace(' ', '_')}_{today}"
        buffer = BytesIO()

        if is_docx:
            for para in doc.paragraphs:
                for ph, val in uploads.items():
                    if ph in para.text:
                        para.text = para.text.replace(ph, val)
            doc.save(buffer)
            st.success("✅ Your DOCX file has been successfully generated!")
            st.download_button(
                label="📥 Download Filled DOCX",
                data=buffer.getvalue(),
                file_name=final_filename + ".docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        elif is_pptx:
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        for ph, val in uploads.items():
                            if ph in shape.text:
                                shape.text = shape.text.replace(ph, val)
            prs.save(buffer)
            st.success("✅ Your PowerPoint file has been successfully generated!")
            st.download_button(
                label="📥 Download Filled PPTX",
                data=buffer.getvalue(),
                file_name=final_filename + ".pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
