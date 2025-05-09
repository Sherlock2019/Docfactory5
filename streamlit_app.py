import streamlit as st
from utils.extract_placeholders import extract_ordered_placeholders
from utils.ui_blocks import placeholder_input_ui
from utils.fill_template import fill_template
from pathlib import Path

st.title("📄 DocAutoFactory – Dynamic RFP Generator")

uploaded_template = st.file_uploader("Upload your .docx template", type=["docx"], key="template_uploader")

if uploaded_template:
    with open("template.docx", "wb") as f:
        f.write(uploaded_template.read())
    st.success("✅ Template uploaded successfully!")

    placeholders = extract_ordered_placeholders("template.docx")
    collected_data = {}

    st.header("📥 Provide Inputs for Placeholders")
    for ph in placeholders:
        if ph in ["{CUSTOMER_NAME}", "{PARTNER_NAME}", "{COMPANY_NAME}", "{CITY_NAME}"]:
            collected_data[ph] = {"type": "text", "content": st.text_input(f"{ph}", key=f"text_{ph}")}
        else:
            collected_data[ph] = placeholder_input_ui(ph)

    if st.button("📄 Generate Filled Document"):
        fill_template("template.docx", "filled_output.docx", collected_data)
        with open("filled_output.docx", "rb") as f:
            st.download_button("⬇️ Download Filled Document", data=f, file_name="Filled_Template.docx")
