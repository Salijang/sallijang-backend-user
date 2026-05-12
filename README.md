# sallijang-backend-user

사용자 인증 및 계정 관리 서비스입니다.

## 기술 스택

- **Python 3.11** / FastAPI
- **PostgreSQL** (asyncpg, SQLAlchemy, Alembic)
- **JWT** (HttpOnly 쿠키 기반 인증)
- **bcrypt** (비밀번호 해싱)

## 주요 기능

- 회원가입 / 로그인 / 로그아웃 (JWT 쿠키 발급)
- 사용자 프로필 조회
- 찜하기 (가게 위시리스트) CRUD

## API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | `/api/v1/auth/signup` | 회원가입 |
| POST | `/api/v1/auth/login` | 로그인 |
| POST | `/api/v1/auth/logout` | 로그아웃 |
| GET | `/api/v1/auth/me` | 현재 사용자 정보 |
| GET | `/api/v1/users/{user_id}` | 사용자 프로필 조회 |
| POST | `/api/v1/wishlists/` | 찜 추가 |
| GET | `/api/v1/wishlists/` | 찜 목록 조회 |
| DELETE | `/api/v1/wishlists/{wishlist_id}` | 찜 삭제 |
| GET | `/api/v1/wishlists/count` | 가게 찜 개수 조회 |

## 사용자 역할

- `buyer` - 상품 구매자
- `seller` - 가게 판매자

## 환경 변수

| 변수명 | 설명 |
|--------|------|
| `DB_HOST` | PostgreSQL 호스트 |
| `DB_PORT` | PostgreSQL 포트 (기본값: 5432) |
| `DB_USER` | DB 사용자명 |
| `DB_NAME` | DB 이름 |
| `DB_PASSWORD` | DB 비밀번호 (미설정 시 RDS IAM 인증) |
| `AWS_REGION` | AWS 리전 (기본값: ap-northeast-2) |
| `SECRET_KEY` | JWT 서명 키 |

## 로컬 실행

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker

```bash
docker build -t sallijang-user .
docker run -p 8000:8000 \
  -e DB_HOST=<host> \
  -e DB_USER=<user> \
  -e DB_PASSWORD=<password> \
  -e SECRET_KEY=<secret> \
  sallijang-user
```
