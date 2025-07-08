from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from typing import List

from cluster import cluster_users




app = FastAPI()

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

@app.post("/receive/vector/test")
async def receive_vector(data: VectorRequest):
    print(f"받아온 vector 값: {data.vector}")
    # 군집화에 활용
    return {"status": "ok"}