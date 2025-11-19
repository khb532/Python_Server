from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import logging

app = FastAPI(title="Simple Test Server")

# 모든 응답은 자동으로 JSON 형식으로 반환됩니다

# 로깅 설정
LOG_FILE = "server.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # 콘솔에도 출력
    ]
)
logger = logging.getLogger(__name__)

# CORS 설정 - 모든 origin 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 요청 로깅 미들웨어
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """모든 요청을 로그 파일에 기록"""
    client_ip = request.client.host
    method = request.method
    url = request.url.path
    query = str(request.query_params) if request.query_params else ""

    # 요청 로깅
    log_message = f"IP: {client_ip} | {method} {url}"
    if query:
        log_message += f" | Params: {query}"

    logger.info(log_message)

    # 요청 처리
    response = await call_next(request)

    return response

# JSON 파일 경로
DB_FILE = "database.json"

# JSON 파일에서 DB 로드
def load_database():
    """JSON 파일에서 데이터베이스 로드"""
    if not os.path.exists(DB_FILE):
        print(f"ERROR: Database file '{DB_FILE}' not found!")
        print(f"Please create '{DB_FILE}' file in the same directory as server.py")
        raise FileNotFoundError(f"Database file '{DB_FILE}' does not exist")

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # JSON에서는 키가 문자열로 저장되므로 int로 변환
            return {int(k): v for k, v in data.items()}
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON format in '{DB_FILE}'")
        print(f"Error details: {e}")
        raise
    except Exception as e:
        print(f"ERROR: Failed to load database from '{DB_FILE}'")
        print(f"Error details: {e}")
        raise

# JSON 파일에 DB 저장
def save_database():
    """데이터베이스를 JSON 파일에 저장"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        # int 키를 str로 변환하여 JSON에 저장
        data = {str(k): v for k, v in database.items()}
        json.dump(data, f, ensure_ascii=False, indent=2)

# 서버 시작 시 DB 로드
database = load_database()


@app.get("/")
async def root():
    """서버 상태 확인"""
    return {
        "status": "running",
        "message": "Server is ready",
        "endpoint": "/api/data/{id}"
    }


@app.get("/api/data/{id}")
async def get_data_by_id(id: int):
    """
    ID로 문자열 데이터 조회 (SQL SELECT data FROM table WHERE id=? 대체)
    클라이언트에서 int형 id를 GET 요청하면 해당 id의 string 데이터를 JSON으로 반환

    응답 예시 (JSON):
    {
        "success": true,
        "id": 1,
        "data": "첫 번째 데이터입니다"
    }
    """
    if id not in database:
        raise HTTPException(status_code=404, detail=f"Data with id {id} not found")

    # JSON 형식으로 자동 변환되어 반환됨
    return {
        "success": True,
        "id": id,
        "data": database[id]
    }


@app.get("/api/data")
async def get_all_data():
    """
    모든 문자열 데이터 조회 (SQL SELECT * FROM table 대체)
    모든 데이터를 JSON 배열 형식으로 반환
    """
    data_list = [{"id": k, "data": v} for k, v in database.items()]
    # JSON 형식으로 자동 변환되어 반환됨
    return {
        "success": True,
        "data": data_list,
        "count": len(data_list)
    }


@app.post("/api/query")
async def query_data(id: int):
    """
    POST 요청으로 ID를 받아 데이터 조회
    클라이언트에서 POST로 id를 보내면 해당 데이터를 JSON으로 반환
    """
    if id not in database:
        raise HTTPException(status_code=404, detail=f"Data with id {id} not found")

    return {
        "success": True,
        "id": id,
        "data": database[id]
    }


@app.post("/api/data")
async def add_data(id: int, data: str):
    """
    새로운 문자열 데이터 추가 (SQL INSERT 대체)
    추가 결과를 JSON 형식으로 반환
    데이터는 database.json 파일에 영구 저장됩니다
    """
    if id in database:
        raise HTTPException(status_code=400, detail=f"Data with id {id} already exists")

    database[id] = data
    save_database()  # JSON 파일에 저장

    # JSON 형식으로 자동 변환되어 반환됨
    return {
        "success": True,
        "id": id,
        "data": data,
        "message": "Data added successfully"
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0으로 설정하여 외부 PC에서 접근 가능하게 함
    print("Server starting on http://0.0.0.0:8000")
    print("External access: http://<your-ip>:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
