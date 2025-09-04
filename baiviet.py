import streamlit as st
import zipfile
import io
import markdown

st.set_page_config(page_title="tạo bài viết ", layout="wide")

st.title("📦 ZIP MD to Hyperlink Converter")

uploaded_file = st.file_uploader("Tải file ZIP chứa .md", type=["zip"])

if uploaded_file:
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        md_files = [f for f in zip_ref.namelist() if f.endswith(".md")]

        if not md_files:
            st.error("❌ Không tìm thấy file .md nào trong ZIP.")
        else:
            for md_file in md_files:
                st.subheader(f"📄 {md_file}")
                content = zip_ref.read(md_file).decode("utf-8")

                st.text_area("📑 Nội dung gốc (Markdown)", content, height=150)

                # Convert markdown -> HTML
                html_content = markdown.markdown(content)

                st.markdown("🔗 **Nội dung sau khi convert (HTML có hyperlink):**", unsafe_allow_html=True)
                st.markdown(html_content, unsafe_allow_html=True)

                st.code(html_content, language="html")
