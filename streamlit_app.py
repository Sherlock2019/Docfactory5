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
    2. Select the document type and enter the customer name.
    3. Fill in key text fields like `{CUSTOMER_NAME}`, `{SA_EMAIL}`, etc.
    4. Upload or type values for the remaining placeholders.
    5. Download your filled .docx or .pptx file.
    """)

# Step 1: Upload template and choose document type
template_file = st.file_uploader("📁 Upload a .docx or .pptx template", type=["docx", "pptx"])
doc_type = st.selectbox("📄 Select Type of Document", ["Solution Proposal", "Cloud Assessment Report/ Presentation", "Migration Plan", "Review"])
today = date.today().strftime("%Y%m%d")
customer_name = st.text_input("👤 Customer Name")

# Define placeholders that only accept text input
TEXT_ONLY_PLACEHOLDERS = {
    "CUSTOMER_NAME", "CITY NAME", "SA-NAME", "SA_EMAIL", "RAX_TEAM", "PARTNER_NAME"
}

if template_file and customer_name:
    is_docx = template_file.name.endswith(".docx")
    is_pptx = template_file.name.endswith(".pptx")
    text_blocks = []

    # Extract text from template
    if is_docx:
        doc = Document(template_file)
        text_blocks = [para.text for para in doc.paragraphs]
    elif is_pptx:
        prs = Presentation(template_file)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text_blocks.append(shape.text)

    # Detect and normalize placeholders
    raw_placeholders = re.findall(r"\{[^}]+\}", "\n".join(text_blocks))
    placeholders = list(dict.fromkeys([f"{{{ph.strip('{}').strip()}}}" for ph in raw_placeholders]))
    st.markdown("### 🔍 Detected Placeholders")
    st.write(placeholders)

    uploads = {}

    # Step 2: Text-only fields first
    st.markdown("### ✏️ Enter Values for Key Fields")
    for key in ["CUSTOMER_NAME", "SA-NAME", "SA_EMAIL", "RAX_TEAM", "PARTNER_NAME"]:
        ph = f"{{{key}}}"
        if ph in placeholders:
            value = st.text_input(f"✏️ {ph}", key=f"text_{key}")
            if value.strip():
                uploads[ph] = value.strip()

    # Step 3: All other placeholders
    st.markdown("### 📎 Upload Files or Enter Text for Remaining Placeholders")
    for ph in placeholders:
        base_ph = ph.strip("{}").strip()
        if base_ph not in TEXT_ONLY_PLACEHOLDERS:
            clean_key = base_ph.replace(" ", "_")
            col1, col2 = st.columns(2)
            with col1:
                file = st.file_uploader(f"📎 Upload file for {ph}", type=["txt", "docx", "xlsx"], key=f"file_{clean_key}")
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

    # Step 4: Replace and export
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
