# 프로젝트 셋팅

***
### 1. pipenv 설치
~~~
pip install pipenv
~~~

### 2. docker-compose build
~~~
docker-compose -f ./docker-compose.yml up --build
~~~

### 3. DB 마이그레이션
~~~
#1. alembic 자동생성
pipenv run alembic revision --autogenerate

## 아래부터 모델 변경될때 마다 실행
# 2. 모델 업테이트 확인 
pipenv run alembic upgrade head

# 3. alembic 자동생성
pipenv run alembic revision --autogenerate
~~~

### 4. swagger 접속
~~~
http://127.0.0.1:8080/docs
~~~