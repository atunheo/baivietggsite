import streamlit as st
import zipfile
import io
import pandas as pd
import re

st.set_page_config(page_title="ZIP MD to Excel Converter", layout="centered")

st.title("📦 ZIP MD to Excel Converter")

uploaded_file = st.file_uploader("Tải file ZIP chứa .md", type=["zip"])

if uploaded_file:
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        md_files = [f for f in zip_ref.namelist() if f.endswith(".md")]

        if not md_files:
            st.error("❌ Không tìm thấy file .md nào trong ZIP.")
        else:
            records = []

            for md_file in md_files:
                # Đọc file .md (giữ nguyên Markdown)
                content = zip_ref.read(md_file).decode("utf-8")

                # Lấy tiêu đề từ dòng H1 đầu tiên (ví dụ: "# Tiêu đề")
                match = re.search(r"^\s*#\s+(.*)$", content, flags=re.MULTILINE)
                if match:
                    title = match.group(1).strip()
                else:
                    title = "N/A"

                # Thêm vào records: cột A tiêu đề (văn bản thuần), cột B là toàn bộ Markdown gốc
                records.append([title, content])

            # Xuất Excel
            df = pd.DataFrame(records, columns=["Tiêu đề", "Nội dung Markdown"])
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Sheet1")

            st.success("✅ Đã xử lý xong!")
            st.download_button(
                label="📥 Tải về Excel",
                data=output.getvalue(),
                file_name="converted_md.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
