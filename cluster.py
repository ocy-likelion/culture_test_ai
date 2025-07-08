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


 