from sklearn.cluster import KMeans
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

def cluster_users(users: list[list[float]], n_clusters: int = 4):
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(users)
    centers = kmeans.cluster_centers_
    return {
        "labels": labels.tolist(),
        "centroids": centers.tolist()
    }


    
class VectorRequest(BaseModel):
    userId: int
    surveyId: int
    vector: List[float]

@app.post("/receive/vector/test")
async def receive_vector(data: VectorRequest):
    print(f"Received vector: {data.vector}")
    # 군집화에 활용
    return {"status": "ok"}