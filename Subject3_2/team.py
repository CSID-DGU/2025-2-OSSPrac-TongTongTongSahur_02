from flask import Flask, render_template, request, redirect, url_for, render_template_string, jsonify
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"

# ===== 경로/설정 =====
# 실행 디렉터리와 무관하게 앱 루트 기준으로 접근
AVATAR_DIR = Path(app.root_path) / "static" / "avatars"
ALLOWED_IMG = {".png", ".jpg", ".jpeg", ".webp"}

# 데모용 메모리 저장소(실서비스는 DB 권장)
TEAM = []

# ===== 유틸 =====
def list_avatars():
    """static/avatars 폴더의 허용 확장자 이미지를 정렬해 반환"""
    AVATAR_DIR.mkdir(parents=True, exist_ok=True)
    return sorted([f.name for f in AVATAR_DIR.iterdir() if f.suffix.lower() in ALLOWED_IMG])

def build_avatar_url(filename: str) -> str:
    """파일명을 static url로 변환"""
    if not filename:
        filename = "member1.png"
    return url_for("static", filename=f"avatars/{filename}")

# ===== 라우트 =====
@app.route("/")
def index():
    # index.html이 아직 없을 수 있으니 입력 페이지로 안내
    try:
        return render_template("index.html")
    except Exception:
        return redirect(url_for("input_page"))

@app.route("/contact")
def contact():
    # contact.html 준비 전 임시 텍스트
    return "Contact page (templates/contact.html로 교체 예정)"

@app.route("/team")
def team_page():
    # 간단 카드 목록
    tpl = """
    <!doctype html><html lang="ko"><meta charset="utf-8">
    <body style="background:#0f0f12;color:#fff;font-family:system-ui">
    <div style="max-width:900px;margin:20px auto">
      <h1>우리 팀을 소개합니다</h1>
      <p><a href="{{ url_for('input_page') }}" style="color:#a78bfa">추가 입력</a> ·
         <a href="{{ url_for('index') }}" style="color:#a78bfa">홈</a></p>
      {% if team %}
        {% for m in team %}
          <div style="display:grid;grid-template-columns:120px 1fr;gap:14px;background:#18181c;border:1px solid #2b2b33;border-radius:14px;padding:12px;margin:12px 0">
            <img src="{{ m.avatar_url }}" style="width:120px;height:120px;object-fit:contain;background:#0d0d11;border-radius:10px">
            <div>
              <h3 style="margin:0">{{ m.name }} <small style="color:#a78bfa">{{ m.role }}</small></h3>
              <div>학번: {{ m.student_id }} / 전공: {{ m.major }}</div>
              <div style="color:#b7b9c3">{{ m.about }}</div>
            </div>
          </div>
        {% endfor %}
      {% else %}
        <p style="color:#b7b9c3">아직 팀원이 없습니다. 먼저 입력해 주세요.</p>
      {% endif %}
    </div></body></html>
    """
    return render_template_string(tpl, team=TEAM)

@app.route("/input", methods=["GET", "POST"])
def input_page():
    if request.method == "GET":
        # 아바타 목록을 자동 전달
        return render_template("input.html", avatars=list_avatars())

    # POST: 폼 수신
    f = request.form
    avatar_file = f.get("avatar_file", "member1.png")

    member = {
        "name": f.get("name", "").strip(),
        "student_id": f.get("student_id", "").strip(),
        "gender": f.get("gender", ""),
        "major": f.get("major", ""),
        "phone": f.get("phone", ""),
        "email": f.get("email", ""),
        "about": f.get("about", ""),
        "role": f.get("role", "TeamMember"),
        "avatar_url": build_avatar_url(avatar_file),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    if not member["name"] or not member["student_id"]:
        return "이름/학번은 필수입니다.", 400

    TEAM.append(member)
    # templates/result.html 사용
    return render_template("result.html", member=member)

# ===== 디버그(목록 안 보일 때 확인용) =====
@app.get("/debug/avatars")
def debug_avatars():
    files = [f.name for f in AVATAR_DIR.iterdir()] if AVATAR_DIR.exists() else []
    return jsonify({
        "avatar_dir": str(AVATAR_DIR),
        "allowed_ext": sorted(list(ALLOWED_IMG)),
        "scanned": list_avatars(),
        "all_found": files
    })

# ===== 실행 =====
if __name__ == "__main__":
    app.run(debug=True)