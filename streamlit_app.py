import streamlit as st
from docx import Document
from pptx import Presentation
import pandas as pd
import re
from io import BytesIO
from datetime import date

st.set_page_config(page_title="🧩 Placeholder Filler", layout="wide")
st.title("📄📊 Dynamic Placeholder Filler for DOCX & PPTX")

# Upload your template
template_file = st.file_uploader("Upload a .docx or .pptx template", type=["docx", "pptx"])
customer_name = st.text_input("Customer Name")
doc_type = st.selectbox("Type of Document", ["Proposal", "Report", "Migration Plan", "Review"])
today = date.today().strftime("%Y%m%d")

if template_file and customer_name:
    is_docx = template_file.name.endswith(".docx")
    is_pptx = template_file.name.endswith(".pptx")
    text_blocks = []

    # Extract placeholders
    if is_docx:
        doc = Document(template_file)
        text_blocks = [para.text for para in doc.paragraphs]
    elif is_pptx:
        prs = Presentation(template_file)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text_blocks.append(shape.text)

    full_text = "\n".join(text_blocks)
    placeholders = list(dict.fromkeys(re.findall(r"\{[^}]+\}", full_text)))
    st.markdown("### 🔍 Detected placeholders")
    st.write(placeholders)

    # Upload or manually input each placeholder value
    uploads = {}
    for ph in placeholders:
        clean_key = ph.strip("{}").replace(" ", "_")
        col1, col2 = st.columns(2)
        with col1:
            file = st.file_uploader(f"Upload file for {ph}", type=["txt", "docx", "xlsx"], key=clean_key)
        with col2:
            manual = st.text_area(f"Or manually enter value for {ph}", height=100, key=f"text_{clean_key}")

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

    # Final replacement
    if uploads:
        final_filename = f"{customer_name}_{doc_type.replace(' ', '_')}_{today}"
        buffer = BytesIO()

        if is_docx:
            for para in doc.paragraphs:
                for ph, val in uploads.items():
                    if ph in para.text:
                        para.text = para.text.replace(ph, val)
            doc.save(buffer)
            st.download_button(
                label="📥 Download DOCX",
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
            st.download_button(
                label="📥 Download PPTX",
                data=buffer.getvalue(),
                file_name=final_filename + ".pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
