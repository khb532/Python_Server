# Python HTTP Server

클라이언트에서 HTTP GET 요청으로 서버에서 데이터를 가져오는 프로젝트입니다.

## 설치

```bash
pip install -r requirements.txt
```

## 서버 실행

```bash
python server.py
```

또는 직접 uvicorn으로 실행:

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

서버는 `http://localhost:8000`에서 실행됩니다.

### API 문서 확인

서버 실행 후 다음 주소에서 자동 생성된 API 문서를 확인할 수 있습니다:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## API 엔드포인트

### 1. 서버 상태 확인
```
GET /health
```

**응답:**
```json
{
  "status": "ok"
}
```

---

### 2. 데이터 스키마 조회
```
GET /api/schema
```

**응답:**
```json
{
  "endpoint": "/api/get-data",
  "method": "GET or POST",
  "request_format": {
    "id": "integer (데이터베이스의 사용자 ID)"
  },
  "response_format": {
    "success": "boolean",
    "id": "integer",
    "data": "string"
  },
  "available_ids": [1, 2, 3, 4, 5]
}
```

---

### 3. 데이터 조회 (GET 방식)
```
GET /api/get-data?id=1
```

**요청 파라미터:**
- `id` (정수): 조회할 사용자 ID

**응답 (성공):**
```json
{
  "success": true,
  "id": 1,
  "data": "Alice"
}
```

**응답 (실패):**
```json
{
  "success": false,
  "error": "id 999에 해당하는 데이터가 없습니다"
}
```

---

### 4. 데이터 조회 (POST 방식)
```
POST /api/get-data
Content-Type: application/json

{
  "id": 1
}
```

**응답:**
```json
{
  "success": true,
  "id": 1,
  "data": "Alice"
}
```

---

## Python 클라이언트 테스트

```bash
python client.py
```

이 스크립트는 GET, POST 방식 모두 테스트합니다.

---

## 가상 DB 데이터

현재 서버에는 다음 데이터가 저장되어 있습니다:

| ID | Data     |
|----|----------|
| 1  | Alice    |
| 2  | Bob      |
| 3  | Charlie  |
| 4  | Diana    |
| 5  | Eve      |

---

## 실제 DB 연동

`server.py`의 `mock_db` 딕셔너리를 실제 데이터베이스 쿼리로 변경하면 됩니다.

### MySQL 예시:

```python
import mysql.connector

def get_data_from_db(user_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        database="your_db"
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT data FROM users WHERE id = {user_id}")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
```

---

## 트러블슈팅

### CORS 에러가 발생하는 경우

```bash
pip install flask-cors
```

그리고 `server.py`에 추가:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
```

---

## 라이센스

MIT
