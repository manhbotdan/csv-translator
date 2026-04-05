import time

texts = df["jp"].dropna().astype(str).tolist()
translator = GoogleTranslator(source="ja", target="vi")

translated = []
batch_size = 50  # số dòng mỗi batch

for i in range(0, len(texts), batch_size):
    batch = texts[i:i+batch_size]
    try:
        result = translator.translate_batch(batch)
        translated.extend(result)
    except Exception as e:
        st.warning(f"Lỗi khi dịch batch {i//batch_size+1}: {e}")
        translated.extend([""] * len(batch))
    time.sleep(2)  # nghỉ 2 giây giữa các batch

# Gán kết quả vào đúng vị trí
df.loc[df["jp"].notna(), "jp"] = translated
df = df.rename(columns={"jp": "vi"})
