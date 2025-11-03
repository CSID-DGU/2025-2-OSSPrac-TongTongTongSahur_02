from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def profile():
    # 폼이 제출되었을 때 (POST 방식)
    if request.method == 'POST':
        # 폼에서 데이터 가져오기
        name = request.form.get('name')
        major = request.form.get('major')
        gender = request.form.get('gender')
        email = request.form.get('email')
        student_id = request.form.get('student_id')
        phone = request.form.get('phone')
        role = request.form.get('role')
        about_me = request.form.get('about_me')
        avatar = request.form.get('avatar')

        # 받은 데이터를 터미널에 출력 (확인용)
        print("----- 새 프로필 정보 -----")
        print(f"이름: {name}")
        print(f"학과: {major}")
        print(f"성별: {gender}")
        print(f"이메일: {email}")
        print(f"학번: {student_id}")
        print(f"전화번호: {phone}")
        print(f"역할: {role}")
        print(f"소개: {about_me}")
        print(f"아바타: {avatar}")
        print("------------------------")

        # 제출 완료 후 성공 페이지로 리디렉션
        return redirect(url_for('success'))

    # 그냥 페이지에 접속했을 때 (GET 방식)
    # templates 폴더의 index.html을 렌더링
    return render_template('input.html')

@app.route('/success')
def success():
    # 성공 메시지
    return '<h1>프로필이 성공적으로 제출되었습니다!</h1><a href="/">돌아가기</a>'

if __name__ == '__main__':
    # 디버그 모드로 앱 실행
    app.run(debug=True)
