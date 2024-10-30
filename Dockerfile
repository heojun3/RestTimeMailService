# 베이스 이미지로 Python 3.8.10 사용
FROM python:3.8.10

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지들을 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 소스를 컨테이너에 복사
COPY . /app/

WORKDIR /app/receive_email

# Django 애플리케이션 실행 전에 마이그레이션 실행
CMD ["sh", "-c", "python manage.py migrate notice && python manage.py runserver 0.0.0.0:8000"]
# CMD ["python manage.py runserver 0.0.0.0:8000"]

