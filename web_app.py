from flask import Flask, request, send_file, render_template, jsonify
import io
from cut_doc.processor import find_and_crop_bytes, sanitize_name_for_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form.get("name", "").strip()
    save_pdf = request.form.get("save_pdf") == "true"
    pdf_file = request.files.get("pdf")

    if not name:
        return jsonify({"error": "Informe o nome/texto a buscar."}), 400
    if not pdf_file or not pdf_file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Envie um arquivo PDF válido."}), 400

    zip_bytes, count = find_and_crop_bytes(name, pdf_file.read(), save_pdf=save_pdf)

    if zip_bytes is None:
        return jsonify({"error": f"Nenhuma ocorrência de '{name}' encontrada no PDF."}), 404

    zip_name = f"{sanitize_name_for_filename(name)}-certificados.zip"
    return send_file(
        io.BytesIO(zip_bytes),
        mimetype="application/zip",
        as_attachment=True,
        download_name=zip_name,
    )


if __name__ == "__main__":
    app.run(debug=True)
