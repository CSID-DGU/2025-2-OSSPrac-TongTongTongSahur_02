# 1. Python 3.10-slim 버전을 기반 이미지로 사용함
FROM python:3.10-slim

# 2. 컨테이너 내의 작업 디렉토리를 설정함
WORKDIR /usr/src/app

# 3. uWSGI 빌드에 필요한 C 컴파일러 및 개발 도구 설치함
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. requirements.txt 파일을 컨테이너로 복사
COPY requirements.txt ./

# 5. pip 자체를 업그레이드함
RUN pip install --upgrade pip

# 6. requirements.txt 파일에 명시된 모든 라이브러리를 설치함
RUN pip install --no-cache-dir -r requirements.txt

# 7. 현재 디렉토리의 모든 파일(main.py, app/ 폴더 등)을 컨테이너로 복사함.
COPY . .

# 8. uWSGI가 Nginx와 통신하기 위해 5000번 포트를 엶.
EXPOSE 5000

CMD ["uwsgi", "--ini", "uwsgi.ini"]