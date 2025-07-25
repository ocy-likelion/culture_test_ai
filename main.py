from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from typing import List

from cluster import cluster_users, add_user_vector, get_all_vectors, clear_vectors

from client import send_result_to_server

import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8090")
ENDPOINT = "/api/v1/cluster/result"
app = FastAPI()

origins = [
    "http://localhost:8090",
    "https://api.heun0.site",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"안녕하십니까, 기업 컬쳐핏 ai 성향 테스트 c팀의 AI쪽을 담당하는 서버입니다"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}
    

@app.get("/hi")
def add():
    return {"helloooooo"}
    

class ClusterRequest(BaseModel):
    users: List[List[float]]
    n_clusters: int = 4

@app.post("/cluster")
def cluster(req: ClusterRequest):
    try:
        result = cluster_users(req.users, req.n_clusters)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    

class VectorRequest(BaseModel):
    userId: int
    surveyId: int
    vector: List[float]


# 벡터 누적 및 군집화 테스트용 엔드포인트
@app.post("/receive/vector/test")
async def receive_vector(data: VectorRequest):
    count = add_user_vector(data.userId, data.surveyId, data.vector)
    print(f"[LOG] 현재 누적 벡터 개수: {count}")
    # 예시: 5개 이상 쌓이면 군집화 실행
    if count >= 10:
        print(f"[LOG] 벡터가 10개 이상 누적되어 군집화 실행! (현재 {count}개)")
        print(f"군집화 중, 잠시만 기다려주세요...")
        vectors = get_all_vectors()
        try:
            result = cluster_users(vectors, n_clusters=4)
            print(f"[LOG] 군집화 결과: {result}")
            clear_vectors()
            return {"status": "clustered", "result": result}
        except Exception as e:
            print(f"[ERROR] 군집화 중 오류 발생: {e}")
            return {"status": "error", "detail": str(e)}
    return {"status": "ok", "current_count": count}


class VectorBatchRequest(BaseModel):
    clusterNum: int
    vectors: List[List[float]]

cluster_status = {
    "last_request_count": 0,
    "last_status": "아직 군집화 요청 없음"
}

@app.post("/receive/vector/batch")
def receive_vector_batch(VectorBatchRequest: VectorBatchRequest):

    cluster_status["last_request_count"] += 1
    cluster_status["last_status"] = f"{cluster_status['last_request_count']}번째 군집화 요청을 받았습니다. 군집화 처리 중..."
    
    print(f"한꺼번에 {len(VectorBatchRequest.vectors)} 개의 벡터 값을 받았습니다")
    for v in VectorBatchRequest.vectors:
        print(v)
    # 받은 벡터들로 바로 군집화 실행
    print(f"이 값들로 {VectorBatchRequest.clusterNum}개의 군집 만들기를 시도 중입니다. 조금만 기다려주세요...")
    print("try 블록 진입 직전")
    try:
        result = cluster_users(VectorBatchRequest.vectors, n_clusters=VectorBatchRequest.clusterNum)
        print(f" {VectorBatchRequest.clusterNum}개의 군집을 만든 결과: {result}")
        print("send_result_to_server 호출 직전")
        send_result_to_server(
            {"status": "clustered", "result": result},
            BACKEND_URL + ENDPOINT
        )
        print("send_result_to_server 호출 직후")

        cluster_status["last_status"] = f"{cluster_status['last_request_count']}번째 군집화 완료"

        return {"status": "clustered"}
        # , "result": result
    except Exception as e:
        print(f"[ERROR] 군집화 중 오류 발생: {e}")

        cluster_status["last_status"] = f"{cluster_status['last_request_count']}번째 군집화 실패: {e}"

        return {"status": "error", "detail": str(e)}


@app.get("/cluster/status")
def get_cluster_status():
    return {"status": cluster_status["last_status"]}