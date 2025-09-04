import streamlit as st
import zipfile
import io
import markdown
import pandas as pd
import re
import os

st.set_page_config(page_title="tạo bài viết", layout="centered")

st.title("📦tạo bài viết ")

uploaded_file = st.file_uploader("Tải file ZIP chứa .md", type=["zip"])

if uploaded_file:
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        md_files = [f for f in zip_ref.namelist() if f.endswith(".md")]

        if not md_files:
            st.error("❌ Không tìm thấy file .md nào trong ZIP.")
        else:
            records = []
            for md_file in md_files:
                content = zip_ref.read(md_file).decode("utf-8")
                html_content = markdown.markdown(content)

                # Lấy tên file gốc
                clean_name = md_file

                # Nếu là README.md thì lấy tên thư mục cha
                if clean_name.endswith("README.md"):
                    clean_name = os.path.dirname(clean_name)
                    clean_name = os.path.basename(clean_name)

                else:
                    clean_name = os.path.basename(clean_name)

                # Bỏ số ở đầu tên
                clean_name = re.sub(r'^\d+[-_ ]*', '', clean_name)

                records.append({
                    "Tên file": clean_name,
                    "Markdown gốc": content,
                    "HTML đã convert": html_content
                })

            # Xuất Excel
            df = pd.DataFrame(records)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Converted")

            st.download_button(
                label="📥 Tải về Excel",
                data=output.getvalue(),
                file_name="converted_md.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
