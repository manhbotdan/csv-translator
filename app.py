from flask import Flask, request, render_template_string, send_file
import json
from googletrans import Translator
import io

app = Flask(__name__)
translator = Translator()

HTML = """
<!doctype html>
<title>Dịch file JSON</title>
<h1>Upload file JSON để dịch</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=text name=lang placeholder="Ngôn ngữ đích (vd: en, vi)">
  <input type=submit value=Dịch>
</form>
{% if translated %}
<h2>Kết quả dịch:</h2>
<pre>{{ translated }}</pre>
<a href="/download">Tải file JSON đã dịch</a>
{% endif %}
"""

translated_data = None

@app.route("/", methods=["GET", "POST"])
def upload_file():
    global translated_data
    translated = None
    if request.method == "POST":
        file = request.files["file"]
        lang = request.form.get("lang", "en")
        if file:
            data = json.load(file)
            def translate_json(obj):
                if isinstance(obj, dict):
                    return {k: translate_json(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [translate_json(i) for i in obj]
                elif isinstance(obj, str):
                    return translator.translate(obj, dest=lang).text
                else:
                    return obj
            translated_data = translate_json(data)
            translated = json.dumps(translated_data, ensure_ascii=False, indent=2)
    return render_template_string(HTML, translated=translated)

@app.route("/download")
def download_file():
    global translated_data
    if translated_data:
        output = io.BytesIO()
        output.write(json.dumps(translated_data, ensure_ascii=False, indent=2).encode("utf-8"))
        output.seek(0)
        return send_file(output, as_attachment=True, download_name="translated.json", mimetype="application/json")
    return "Chưa có dữ liệu dịch"

if __name__ == "__main__":
    app.run(debug=True)
