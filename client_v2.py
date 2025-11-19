import requests
import json

# 서버 주소
SERVER_URL = "http://localhost:8000"


def get_schema():
    """서버에서 지원하는 데이터 구조 조회"""
    try:
        response = requests.get(f"{SERVER_URL}/api/schema")
        response.raise_for_status()
        print("=== 서버 스키마 정보 ===")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        print()
    except requests.exceptions.RequestException as e:
        print(f"에러: {e}")


def get_data_get(user_id):
    """
    서버에서 id에 해당하는 데이터 조회 (GET 방식)

    Args:
        user_id: 조회할 사용자 ID
    """
    try:
        response = requests.get(
            f"{SERVER_URL}/api/get-data",
            params={"id": user_id},
            headers={"Content-Type": "application/json"}
        )

        print(f"요청: GET /api/get-data?id={user_id}")
        print(f"상태 코드: {response.status_code}")
        print(f"응답:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        print()

    except requests.exceptions.RequestException as e:
        print(f"에러: {e}")


def get_data_post(user_id):
    """
    서버에서 id에 해당하는 데이터 조회 (POST 방식)

    Args:
        user_id: 조회할 사용자 ID
    """
    try:
        payload = {"id": user_id}
        response = requests.post(
            f"{SERVER_URL}/api/get-data",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        print(f"요청: POST /api/get-data")
        print(f"페이로드: {json.dumps(payload, ensure_ascii=False)}")
        print(f"상태 코드: {response.status_code}")
        print(f"응답:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        print()

    except requests.exceptions.RequestException as e:
        print(f"에러: {e}")


def health_check():
    """서버 상태 확인"""
    try:
        response = requests.get(f"{SERVER_URL}/health")
        response.raise_for_status()
        print("=== 서버 상태 확인 ===")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        print()
    except requests.exceptions.RequestException as e:
        print(f"에러: {e}")


if __name__ == "__main__":
    print("Python 클라이언트 테스트\n")

    # 서버 상태 확인
    health_check()

    # 서버 스키마 조회
    get_schema()

    # GET 방식 데이터 조회 테스트
    print("=== GET 방식 데이터 조회 테스트 ===\n")

    # 성공하는 경우
    get_data_get(1)
    get_data_get(3)

    # 실패하는 경우 (존재하지 않는 ID)
    get_data_get(999)

    # POST 방식 데이터 조회 테스트
    print("\n=== POST 방식 데이터 조회 테스트 ===\n")

    # 성공하는 경우
    get_data_post(1)
    get_data_post(5)

    # 실패하는 경우 (존재하지 않는 ID)
    get_data_post(999)

    # 잘못된 형식
    print("=== 잘못된 요청 테스트 ===")
    try:
        response = requests.post(
            f"{SERVER_URL}/api/get-data",
            json={"wrong_field": 123},
            headers={"Content-Type": "application/json"}
        )
        print(f"상태 코드: {response.status_code}")
        print(f"응답:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"에러: {e}")
