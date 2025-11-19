from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# 가상의 DB (딕셔너리로 구현)
mock_db = {
    1: "Alice",
    2: "Bob",
    3: "Charlie",
    4: "Diana",
    5: "Eve"
}


# POST 요청을 위한 데이터 모델
class DataRequest(BaseModel):
    id: int


class DataResponse(BaseModel):
    success: bool
    id: Optional[int] = None
    data: Optional[str] = None
    error: Optional[str] = None


@app.get("/health")
async def health_check():
    """
    서버 상태 확인
    """
    return {"status": "ok"}


@app.get("/api/schema")
async def get_schema():
    """
    서버에서 제공 가능한 데이터 구조를 반환
    """
    return {
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
        "available_ids": list(mock_db.keys())
    }


@app.get("/api/get-data")
async def get_data_get(id: int = Query(..., description="조회할 사용자 ID")) -> DataResponse:
    """
    GET 방식으로 id를 받아서 DB에서 데이터를 조회하고 JSON으로 반환

    GET 요청 형식:
    /api/get-data?id=1

    응답 형식:
    {
        "success": true,
        "id": 1,
        "data": "Alice"
    }
    """
    if id in mock_db:
        return DataResponse(
            success=True,
            id=id,
            data=mock_db[id]
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"id {id}에 해당하는 데이터가 없습니다"
        )


@app.post("/api/get-data")
async def get_data_post(request: DataRequest) -> DataResponse:
    """
    POST 방식으로 id를 받아서 DB에서 데이터를 조회하고 JSON으로 반환

    POST 요청 형식:
    {
        "id": 1
    }

    응답 형식:
    {
        "success": true,
        "id": 1,
        "data": "Alice"
    }
    """
    if request.id in mock_db:
        return DataResponse(
            success=True,
            id=request.id,
            data=mock_db[request.id]
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"id {request.id}에 해당하는 데이터가 없습니다"
        )


if __name__ == "__main__":
    import uvicorn
    print("서버가 http://localhost:8000 에서 실행 중입니다...")
    print("\n사용 가능한 엔드포인트:")
    print("- GET  /health           : 서버 상태 확인")
    print("- GET  /api/schema       : 데이터 구조 조회")
    print("- GET  /api/get-data     : id로 데이터 조회 (GET 방식)")
    print("- POST /api/get-data     : id로 데이터 조회 (POST 방식)")
    print("- GET  /docs             : API 문서 (Swagger UI)")
    print("- GET  /redoc            : API 문서 (ReDoc)")
    print()
    uvicorn.run(app, host="0.0.0.0", port=8000)
