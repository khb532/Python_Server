# FastAPI 테스트 서버

다른 PC에서 통신 가능한 간단한 FastAPI 서버입니다. 테스트용 가상 데이터를 사용하며, 나중에 SQL DB로 교체 예정입니다.

## 설치 방법

```bash
pip install -r requirements.txt
```

## 서버 실행

```bash
python server.py
```

서버가 실행되면:
- 로컬: `http://localhost:8000`
- 외부 PC: `http://<your-ip>:8000`

## 외부 PC에서 접속하기

1. 본인 PC의 IP 주소 확인:
   ```bash
   # Windows
   ipconfig

   # Linux/Mac
   ifconfig
   ```

2. 방화벽 설정: 8000번 포트 허용 필요

3. 다른 PC에서 접속: `http://<your-ip>:8000`

## API 문서

서버 실행 후 Swagger UI에서 테스트 가능:
- `http://localhost:8000/docs` (로컬)
- `http://<your-ip>:8000/docs` (외부)

## DB 구조

하나의 데이터베이스만 사용:
```python
database = {
    id (int): string_data (str)
}
```

## API 엔드포인트

### 기본
- `GET /` - 서버 상태 확인
- `GET /health` - 헬스 체크

### 데이터 조회 (메인 기능)
**클라이언트에서 int형 id로 GET 요청 시 해당 string 데이터 반환**
- `GET /api/data/{id}` - ID로 문자열 데이터 조회 (SQL: SELECT data FROM table WHERE id=?)
- `GET /api/data` - 모든 데이터 조회 (SQL: SELECT * FROM table)
- `POST /api/data` - 새 데이터 추가 (SQL: INSERT INTO table, 파라미터: id, data)

## 사용 예시

### ID로 문자열 데이터 조회 (메인 기능)
```bash
# 로컬에서
curl http://localhost:8000/api/data/1

# 다른 PC에서
curl http://192.168.0.100:8000/api/data/1
```

응답 예시:
```json
{
  "success": true,
  "id": 1,
  "data": "첫 번째 데이터입니다"
}
```

### 모든 데이터 조회
```bash
curl http://localhost:8000/api/data
```

### 새 데이터 추가
```bash
curl -X POST "http://localhost:8000/api/data?id=999&data=새로운%20데이터입니다"
```


## 프로젝트 구조

- `server.py` - FastAPI 서버 (테스트용, SQL DB로 교체 예정)
- `requirements.txt` - 필요한 패키지 목록
