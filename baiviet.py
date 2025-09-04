import streamlit as st
import re
import zipfile
import io

st.set_page_config(page_title="ZIP TXT to Hyperlink Converter", layout="wide")

st.title("📦 ZIP TXT to Hyperlink Converter")

uploaded_file = st.file_uploader("Tải file ZIP chứa .txt", type=["zip"])

if uploaded_file:
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        txt_files = [f for f in zip_ref.namelist() if f.endswith(".txt")]

        if not txt_files:
            st.error("❌ Không tìm thấy file .txt nào trong ZIP.")
        else:
            for txt_file in txt_files:
                st.subheader(f"📄 {txt_file}")
                content = zip_ref.read(txt_file).decode("utf-8")

                st.text_area("Nội dung gốc", content, height=150)

                # Hàm convert link -> hyperlink
                def convert_to_html(text):
                    pattern = r'(https?://[^\s]+)'
                    return re.sub(pattern, r'<a href="\1">\1</a>', text)

                html_content = convert_to_html(content).replace("\n", "<br>")

                st.markdown("🔗 **Nội dung sau khi convert (có hyperlink):**", unsafe_allow_html=True)
                st.markdown(html_content, unsafe_allow_html=True)

                st.code(html_content, language="html")
 
