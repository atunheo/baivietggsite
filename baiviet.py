import streamlit as st
import re

st.set_page_config(page_title="TXT to Hyperlink Converter", layout="centered")

st.title("📄 TXT to Hyperlink Converter")

uploaded_file = st.file_uploader("Tải file .txt", type=["txt"])

if uploaded_file:
    # Đọc nội dung file
    text = uploaded_file.read().decode("utf-8")

    st.subheader("📑 Nội dung gốc (.txt)")
    st.text(text)

    # Chuyển link thành HTML hyperlink
    def convert_to_html(text):
        pattern = r'(https?://[^\s]+)'
        return re.sub(pattern, r'<a href="\1">\1</a>', text)

    html_content = convert_to_html(text).replace("\n", "<br>")

    st.subheader("🔗 Nội dung đã convert (có hyperlink)")
    st.markdown(html_content, unsafe_allow_html=True)

    st.code(html_content, language="html")

    st.success("✅ Bạn có thể copy đoạn HTML ở trên và dán vào Google Sites (chế độ Văn bản thường).")
