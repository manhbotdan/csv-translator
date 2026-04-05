import pandas as pd
import streamlit as st
import requests

st.title("Dịch CSV/Excel từ tiếng Nhật sang tiếng Việt")

# Thay bằng key và endpoint của bạn (nếu dùng Microsoft Translator API)
AZURE_KEY = "YOUR_AZURE_TRANSLATOR_KEY"
AZURE_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
AZURE_REGION = "YOUR_REGION"  # ví dụ: "eastasia"

def translate_texts(texts, from_lang="ja", to_lang="vi"):
    path = '/translate?api-version=3.0'
    params = f"&from={from_lang}&to={to_lang}"
    constructed_url = AZURE_ENDPOINT + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_KEY,
        'Ocp-Apim-Subscription-Region': AZURE_REGION,
        'Content-type': 'application/json'
    }

    body = [{"text": t} for t in texts]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return [item['translations'][0]['text'] for item in response]

uploaded_file = st.file_uploader("Tải lên file CSV hoặc Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Đọc file
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8", sep=None, engine="python")
    except Exception:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Kiểm tra cột jp
    if "jp" not in df.columns:
        st.error("File không có cột 'jp'.")
    else:
        st.write("📄 Bản xem trước dữ liệu gốc:")
        st.dataframe(df.head())

        # Lấy danh sách cần dịch
        texts = df["jp"].dropna().astype(str).tolist()

        # Dịch sang tiếng Việt
        translated = translate_texts(texts)

        # Gán kết quả dịch vào cột jp
        df.loc[df["jp"].notna(), "jp"] = translated

        # Đổi tên cột jp thành vi
        df = df.rename(columns={"jp": "vi"})

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
