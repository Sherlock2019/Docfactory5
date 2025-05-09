import streamlit as st
from pathlib import Path

SUPPORTED_FORMATS = ["docx", "xlsx", "csv", "txt", "jpg", "png"]

def placeholder_input_ui(placeholder):
    st.markdown(f"### 🧩 {placeholder}")

    uploaded = st.file_uploader(f"Upload file for {placeholder}", type=SUPPORTED_FORMATS, key=f"upload_{placeholder}")
    manual_input = st.text_area(f"Or manually enter value for {placeholder}", key=f"text_{placeholder}")

    if uploaded:
        upload_path = Path(f"uploads/{placeholder}_{uploaded.name}")
        upload_path.parent.mkdir(parents=True, exist_ok=True)
        with open(upload_path, "wb") as f:
            f.write(uploaded.read())
        return {"type": "file", "path": str(upload_path)}
    elif manual_input:
        return {"type": "text", "content": manual_input}
    else:
        return {"type": "empty"}
