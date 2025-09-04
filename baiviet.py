import streamlit as st
import zipfile
import io
import markdown
import pandas as pd
import re
import os

st.set_page_config(page_title="ZIP to Excel ", layout="centered")

st.title("📦 ZIP to Excel ")

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

                # Lấy tên file sạch
                clean_name = md_file
                if clean_name.endswith("README.md"):
                    clean_name = os.path.dirname(clean_name)
                    clean_name = os.path.basename(clean_name)
                else:
                    clean_name = os.path.basename(clean_name)

                # Bỏ số ở đầu
                clean_name = re.sub(r'^\d+[-_ ]*', '', clean_name)

                # Cột 1: tiêu đề
                title = f"{clean_name} 【链接地址： 】"

                # Thêm vào records
                records.append([title, html_content])

            # Xuất Excel
            df = pd.DataFrame(records, columns=["标题", "内容"])
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Sheet1")

            st.download_button(
                label="📥 Tải về Excel",
                data=output.getvalue(),
                file_name="converted_md.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
