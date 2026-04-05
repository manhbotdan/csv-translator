import pandas as pd
from deep_translator import GoogleTranslator
import streamlit as st

st.title("Dịch CSV/Excel từ tiếng Nhật sang tiếng Việt")

uploaded_file = st.file_uploader("Tải lên file CSV hoặc Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Thử đọc như CSV
        df = pd.read_csv(uploaded_file)
    except Exception:
        # Nếu lỗi, đọc như Excel với engine openpyxl
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    if "ja" not in df.columns:
        st.error("File không có cột 'ja'.")
    else:
        st.write("📄 Bản xem trước dữ liệu gốc:")
        st.dataframe(df.head())

        # Dịch sang tiếng Việt
        df["vi"] = df["ja"].apply(
            lambda x: GoogleTranslator(source="ja", target="vi").translate(x) if pd.notnull(x) else x
        )
        df = df.drop(columns=["ja"])

        st.write("✅ Bản xem trước dữ liệu đã dịch:")
        st.dataframe(df.head())

        # Xuất file CSV mới
        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="⬇️ Tải xuống file CSV đã dịch",
            data=csv,
            file_name="UI_translated.csv",
            mime="text/csv",
        )
