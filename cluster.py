from sklearn.cluster import KMeans
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List



# 벡터 저장 및 누적 관리용 (메모리 임시 저장)
user_vectors = {}

def add_user_vector(user_id: int, survey_id: int, vector: list[float]):
    print(f"[LOG] 벡터 저장: userId={user_id}, surveyId={survey_id}, vector={vector}")
    key = (user_id, survey_id)
    user_vectors[key] = vector
    return len(user_vectors)

def get_all_vectors():
    return list(user_vectors.values())

def clear_vectors():
    user_vectors.clear()

def cluster_users(users: list[list[float]], n_clusters: int = 4):
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(users)
    centers = kmeans.cluster_centers_
    return {
        "labels": labels.tolist(),
        "centroids": centers.tolist()
    }


 