import streamlit as st
import zipfile
import io
import markdown
import pandas as pd
from bs4 import BeautifulSoup

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
                # Đọc file .md
                content = zip_ref.read(md_file).decode("utf-8")
                html_content = markdown.markdown(content)

                # Parse HTML
                soup = BeautifulSoup(html_content, "html.parser")

                # Lấy tiêu đề từ <h1>
                h1_tag = soup.find("h1")
                if h1_tag:
                    title = h1_tag.get_text(strip=True)
                    h1_tag.decompose()  # xóa <h1> khỏi nội dung
                else:
                    title = "N/A"

                # Xử lý link: chỉ giữ link đầu tiên
                links = soup.find_all("a")
                if links:
                    first_link = links[0]
                    href = first_link.get("href", "")
                    text = first_link.get_text(strip=True)
                    first_link.clear()
                    first_link["href"] = href
                    first_link.string = text

                    # bỏ thẻ <a> của các link còn lại, giữ text
                    for extra_link in links[1:]:
                        extra_link.unwrap()

                # Biến mỗi đoạn <p> thành text + <br>
                lines = []
                for elem in soup.find_all(["p", "br", "a", "li"]):
                    if elem.name == "p" or elem.name == "li":
                        text = elem.get_text(" ", strip=True)
                        if text:
                            lines.append(text + "<br>")
                    elif elem.name == "br":
                        lines.append("<br>")
                    elif elem.name == "a":
                        lines.append(str(elem) + "<br>")

                # Nối lại nội dung đơn giản
                clean_html = "".join(lines)

                # Thêm vào records
                records.append([title, clean_html])

            # Xuất Excel
            df = pd.DataFrame(records, columns=["标题", "内容"])
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
