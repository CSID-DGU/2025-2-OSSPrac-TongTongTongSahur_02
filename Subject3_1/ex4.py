# ex4.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pathlib import Path
import time, os

BASE = Path(__file__).resolve().parent
TEMPLATES = BASE / "templates"

app = Flask(__name__, template_folder=str(TEMPLATES))

@app.route('/', methods=['GET'])
def input_page():
    return render_template('input.html', _ver="v-Subject3_1")

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'GET':
        return redirect(url_for('input_page'))

    name = request.form.get('name', '').strip()
    student_number = request.form.get('StudentNumber', '').strip()
    major = request.form.get('Major', '').strip()
    gender = request.form.get('Gender', '').strip()
    languages_list = request.form.getlist('languages')

    result_dict = {
        'Name': name,
        'StudentNumber': student_number,
        'Gender': gender,
        'Major': major,
        'languages': ', '.join(languages_list) if languages_list else ''
    }
    return render_template('result.html', result=result_dict, _ver="v-Subject3_1")

# 🔍 내가 어떤 템플릿 폴더/파일을 보고 있는지 즉시 확인
@app.route('/_where')
def _where():
    def stat(p):
        try:
            s = os.stat(p)
            return {"exists": True, "mtime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(s.st_mtime))}
        except FileNotFoundError:
            return {"exists": False}
    return jsonify({
        "base": str(BASE),
        "templates": str(TEMPLATES),
        "input.html": stat(TEMPLATES / "input.html"),
        "result.html": stat(TEMPLATES / "result.html"),
    })

if __name__ == '__main__':
    print("BASE =", BASE)
    print("TEMPLATES =", TEMPLATES)
    app.run(debug=True, port=5050)  # ← 5050 포트로 띄워서 다른 서버와 충돌 방지
