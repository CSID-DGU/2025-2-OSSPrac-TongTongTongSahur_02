# team.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"

# ===== 경로/설정 =====
AVATAR_DIR = Path(app.root_path) / "static" / "avatars"
ALLOWED_IMG = {".png", ".jpg", ".jpeg", ".webp"}

# 데모용 메모리 저장소(실서비스는 DB 권장)
TEAM = []  # [{name, student_id, ...}]

# ===== 유틸 =====
def list_avatars():
    AVATAR_DIR.mkdir(parents=True, exist_ok=True)
    return sorted([f.name for f in AVATAR_DIR.iterdir() if f.suffix.lower() in ALLOWED_IMG])

def build_avatar_url(filename: str) -> str:
    if not filename:
        filename = "member1.png"
    return url_for("static", filename=f"avatars/{filename}")

def find_member(student_id: str):
    for m in TEAM:
        if str(m.get("student_id")) == str(student_id):
            return m
    return None

# ===== 라우트 =====
@app.route("/")
def index():
    # 메인 히어로
    return render_template("index.html")

@app.route("/input", methods=["GET", "POST"])
def input_page():
    if request.method == "GET":
        return render_template("input.html", avatars=list_avatars())

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

    # 이미 존재하면 업데이트, 아니면 추가
    old = find_member(member["student_id"])
    if old:
        old.update(member)
    else:
        TEAM.append(member)

    # 개별 상세 페이지로 이동
    return redirect(url_for("member_detail", student_id=member["student_id"]))

@app.route("/member/<student_id>")
def member_detail(student_id):
    m = find_member(student_id)
    if not m:
        abort(404)
    return render_template("result.html", member=m)

@app.route("/team")
def team_page():
    # 팀 카드(각 카드 클릭 → /member/<sid>)
    return render_template("team.html", team=TEAM)

@app.route("/contact")
def contact():
    return render_template("contact.html")

# (선택) 디버그
@app.get("/debug/avatars")
def debug_avatars():
    files = [f.name for f in AVATAR_DIR.iterdir()] if AVATAR_DIR.exists() else []
    return jsonify({
        "avatar_dir": str(AVATAR_DIR),
        "allowed_ext": sorted(list(ALLOWED_IMG)),
        "scanned": list_avatars(),
        "all_found": files,
        "team_count": len(TEAM),
        "team": TEAM,
    })

if __name__ == "__main__":
    app.run(debug=True)
