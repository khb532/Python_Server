# API 사용 가이드

## 서버 접속 정보

**서버 주소**: `http://172.16.100.159:8000`

> 주의: 서버 PC와 같은 네트워크(Wi-Fi/LAN)에 연결되어 있어야 합니다.

## 데이터 영구 저장

이 서버는 **database.json 파일**을 사용하여 데이터를 영구 저장합니다.
- POST로 데이터 추가 시 → 자동으로 database.json에 저장
- 서버 재시작 시 → database.json에서 데이터 자동 로드
- **서버가 꺼져도 데이터가 유지됩니다**

## 빠른 시작

### 1. 연결 테스트
```bash
curl http://172.16.100.159:8000/
```

응답:
```json
{
  "status": "running",
  "message": "Server is ready",
  "endpoint": "/api/data/{id}"
}
```

---

## API 엔드포인트

### 📌 메인 기능: ID로 데이터 조회

**요청**
```
GET http://172.16.100.159:8000/api/data/{id}
```

**파라미터**
- `id` (int, 필수): 조회할 데이터의 ID

**응답 예시**
```json
{
  "success": true,
  "id": 1,
  "data": "박원서 바보"
}
```

**사용 예시**

```bash
# curl 사용
curl http://172.16.100.159:8000/api/data/1

# Python requests 사용
import requests
response = requests.get("http://172.16.100.159:8000/api/data/1")
data = response.json()
print(data["data"])  # "박원서 바보"

# JavaScript fetch 사용
fetch('http://172.16.100.159:8000/api/data/1')
  .then(response => response.json())
  .then(data => console.log(data.data));

# Java 사용
URL url = new URL("http://172.16.100.159:8000/api/data/1");
HttpURLConnection con = (HttpURLConnection) url.openConnection();
con.setRequestMethod("GET");
```

**에러 응답**
```json
{
  "detail": "Data with id 999 not found"
}
```
HTTP Status: 404

---

### 📋 모든 데이터 조회

**요청**
```
GET http://172.16.100.159:8000/api/data
```

**응답 예시**
```json
{
  "success": true,
  "data": [
    {"id": 1, "data": "박원서 바보"},
    {"id": 2, "data": "김재민 바보"},
    {"id": 3, "data": "박순례할머니의 마무리일격"},
    {"id": 4, "data": "네 덱은 널 짐으로 생각한다"},
    {"id": 5, "data": "NULL"}
  ],
  "count": 5
}
```

**사용 예시**
```bash
curl http://172.16.100.159:8000/api/data
```

---

### ➕ 데이터 추가

**요청**
```
POST http://172.16.100.159:8000/api/data?id={id}&data={data}
```

**파라미터**
- `id` (int, 필수): 새로운 데이터의 ID
- `data` (string, 필수): 저장할 문자열 데이터

**응답 예시**
```json
{
  "success": true,
  "id": 10,
  "data": "새로운 데이터",
  "message": "Data added successfully"
}
```

**사용 예시**

```bash
# curl 사용
curl -X POST "http://172.16.100.159:8000/api/data?id=10&data=새로운데이터"

# Python requests 사용
import requests
response = requests.post(
    "http://172.16.100.159:8000/api/data",
    params={"id": 10, "data": "새로운 데이터"}
)
print(response.json())
```

**에러 응답**
```json
{
  "detail": "Data with id 10 already exists"
}
```
HTTP Status: 400

---

### 🏥 헬스 체크

**요청**
```
GET http://172.16.100.159:8000/health
```

**응답**
```json
{
  "status": "healthy"
}
```

---

## 현재 등록된 데이터

| ID | 데이터 |
|----|--------|
| 1  | 박원서 바보 |
| 2  | 김재민 바보 |
| 3  | 박순례할머니의 마무리일격 |
| 4  | 네 덱은 널 짐으로 생각한다 |
| 5  | NULL |

---

## 다양한 언어별 사용 예시

### Python
```python
import requests

# 데이터 조회
response = requests.get("http://172.16.100.159:8000/api/data/1")
result = response.json()
print(result["data"])

# 데이터 추가
response = requests.post(
    "http://172.16.100.159:8000/api/data",
    params={"id": 100, "data": "테스트"}
)
print(response.json())
```

### JavaScript (Node.js)
```javascript
const axios = require('axios');

// 데이터 조회
axios.get('http://172.16.100.159:8000/api/data/1')
  .then(response => {
    console.log(response.data.data);
  });

// 데이터 추가
axios.post('http://172.16.100.159:8000/api/data', null, {
  params: { id: 100, data: '테스트' }
})
  .then(response => {
    console.log(response.data);
  });
```

### JavaScript (브라우저)
```javascript
// 데이터 조회
fetch('http://172.16.100.159:8000/api/data/1')
  .then(response => response.json())
  .then(data => console.log(data.data));

// 데이터 추가
fetch('http://172.16.100.159:8000/api/data?id=100&data=테스트', {
  method: 'POST'
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Java
```java
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;

// 데이터 조회
URL url = new URL("http://172.16.100.159:8000/api/data/1");
HttpURLConnection con = (HttpURLConnection) url.openConnection();
con.setRequestMethod("GET");

BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream())
);
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());
```

### C#
```csharp
using System.Net.Http;
using System.Threading.Tasks;

// 데이터 조회
var client = new HttpClient();
var response = await client.GetAsync("http://172.16.100.159:8000/api/data/1");
var content = await response.Content.ReadAsStringAsync();
Console.WriteLine(content);
```

### Go
```go
package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
)

func main() {
    // 데이터 조회
    resp, _ := http.Get("http://172.16.100.159:8000/api/data/1")
    defer resp.Body.Close()
    body, _ := ioutil.ReadAll(resp.Body)
    fmt.Println(string(body))
}
```

---

## 대화형 API 문서 (Swagger UI)

브라우저에서 아래 주소로 접속하면 대화형 API 문서를 볼 수 있습니다:

**Swagger UI**: http://172.16.100.159:8000/docs

여기서 직접 API를 테스트해볼 수 있습니다.

---

## 문제 해결

### 연결이 안 될 때

1. **같은 네트워크에 연결되어 있는지 확인**
   - 서버 PC와 동일한 Wi-Fi 또는 LAN에 연결되어 있어야 합니다.

2. **서버가 실행 중인지 확인**
   - 서버 PC에서 `python server.py`가 실행 중이어야 합니다.

3. **방화벽 확인**
   - Windows 방화벽에서 8000번 포트가 허용되어 있어야 합니다.

4. **IP 주소 확인**
   - 서버 IP가 변경되었을 수 있습니다.
   - 서버 PC에서 `ipconfig` 명령어로 현재 IP를 확인하세요.

### CORS 에러가 발생할 때

이 서버는 모든 도메인에서의 접근을 허용하도록 설정되어 있습니다. CORS 에러가 발생하지 않아야 합니다.

---

## 응답 형식

모든 응답은 **JSON 형식**입니다.

**성공 응답 구조**
```json
{
  "success": true,
  "id": 1,
  "data": "문자열 데이터"
}
```

**에러 응답 구조**
```json
{
  "detail": "에러 메시지"
}
```

---

## 연락처

문제가 발생하거나 질문이 있으면 서버 관리자에게 문의하세요.
