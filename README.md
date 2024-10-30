### 세팅
1. cp .env.sample .env  
2. .env 파일 수정합니다.
3. receive_email, save_login_cookie에도 sample을 복사하여 수정합니다.
4. docker compose up  

### 로그인 쿠키 생성
docker exec -i -w /app resttimemailservice-django-web-1 python -m save_login_cookie  

### 남은 근무 시간 확인
docker exec -i -w /app resttimemailservice-django-web-1 python -m calculate_rest_work_time example1030@cowave.kr  

### 메일 보내기
1. http://localhost:8052/ 에 접속하여 이메일 설정  
2. docker exec -i -w /app resttimemailservice-django-web-1 python .  
