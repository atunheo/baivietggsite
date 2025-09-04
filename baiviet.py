import streamlit as st
import zipfile
import io
import markdown
import pandas as pd
from bs4 import BeautifulSoup

st.set_page_config(page_title="ZIP to Excel", layout="centered")

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

                # Dùng BeautifulSoup để lấy <h1>
                soup = BeautifulSoup(html_content, "html.parser")
                h1_tag = soup.find("h1")
                if h1_tag:
                    title = h1_tag.get_text(strip=True)
                else:
                    title = "N/A"

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
