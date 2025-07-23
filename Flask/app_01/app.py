import os
import re
from flask import Flask, render_template, request, jsonify, session, send_file
from dotenv import load_dotenv
import google.generativeai as genai
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret")

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Markdown stripper
def strip_markdown(md):
    md = re.sub(r'\*\*(.*?)\*\*', r'\1', md)
    md = re.sub(r'\*(.*?)\*', r'\1', md)
    md = re.sub(r'__(.*?)__', r'\1', md)
    md = re.sub(r'_(.*?)_', r'\1', md)
    md = re.sub(r'~~(.*?)~~', r'\1', md)
    md = re.sub(r'`{1,3}(.*?)`{1,3}', r'\1', md)
    md = re.sub(r'^#{1,6}\s*', '', md, flags=re.MULTILINE)
    md = re.sub(r'^\s*[\*\-\+]\s+', '', md, flags=re.MULTILINE)
    return md.strip()

# PDF Export
def export_chat_to_pdf(messages):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFont("Helvetica", 11)
    width, height = 595, 842
    y = height - 40
    for msg in messages:
        role = "You" if msg["role"] == "user" else "Gemini"
        lines = [f"{role}: {msg['content']}"]
        for line in lines:
            split_lines = line.split('\n')
            for part in split_lines:
                if y < 40:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 11)
                    y = height - 40
                pdf.drawString(40, y, part[:1000])
                y -= 20
    pdf.save()
    buffer.seek(0)
    return buffer

@app.route("/")
def home():
    if "messages" not in session:
        session["messages"] = []
    return render_template("index.html", messages=session["messages"])

@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.form.get("message")
    session["messages"].append({"role": "user", "content": user_message})
    response = model.generate_content(user_message)
    clean_bot = strip_markdown(response.text.strip())
    session["messages"].append({"role": "assistant", "content": clean_bot})
    session.modified = True
    return jsonify({"message": clean_bot})

@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400
    file_type = uploaded_file.content_type
    if file_type.startswith("image/"):
        image = Image.open(uploaded_file)
        response = model.generate_content([image, "Describe this image in detail."])
        output = strip_markdown(response.text.strip())
        session["messages"].append({"role": "assistant", "content": f"📷 Image:\n{output}"})
    elif file_type.startswith("text/"):
        content = uploaded_file.read().decode("utf-8")
        response = model.generate_content(f"Analyze this text:\n{content}")
        output = strip_markdown(response.text.strip())
        session["messages"].append({"role": "assistant", "content": f"📄 Text:\n{output}"})
    else:
        output = "Unsupported file type."
    session.modified = True
    return jsonify({"message": output})

@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    session["messages"] = []
    return jsonify({"status": "cleared"})

@app.route("/download_pdf")
def download_pdf():
    pdf_buffer = export_chat_to_pdf(session.get("messages", []))
    return send_file(pdf_buffer, mimetype="application/pdf", as_attachment=True, download_name="chat.pdf")

if __name__ == "__main__":
    app.run(debug=True)
