from sklearn.cluster import KMeans
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List



# 벡터 저장 및 누적 관리용 (메모리 임시 저장)
user_vectors = {}

def add_user_vector(user_id: int, survey_id: int, vector: list[float]):
    print("\n[LOG] 벡터 저장:")
    print(f"  userId = {user_id}")
    print(f"  surveyId = {survey_id}")
    print(f"  vector = {vector}\n")
    key = (user_id, survey_id)
    user_vectors[key] = vector
    return len(user_vectors)

def get_all_vectors():
    return list(user_vectors.values())

def clear_vectors():
    user_vectors.clear()

# 성향 정보
property_pairs = [
    {"pos": {"key": "P_1", "name": "즉시 전력형"}, "neg": {"key": "P_2", "name": "성장 가능형"}},
    {"pos": {"key": "P_3", "name": "직면형"}, "neg": {"key": "P_4", "name": "숙고형"}},
    {"pos": {"key": "P_5", "name": "혁신적 성향"}, "neg": {"key": "P_6", "name": "전통적 성향"}},
    {"pos": {"key": "P_7", "name": "객관적 자료형"}, "neg": {"key": "P_8", "name": "주관적 인상형"}},
]

def describe_centroid(centroid):
    # 각 차원의 절대값과 인덱스 추출
    abs_with_idx = sorted([(abs(v), i, v) for i, v in enumerate(centroid)], reverse=True)
    desc = []
    for _, i, v in abs_with_idx[:2]:
        if v > 0:
            desc.append(f"{property_pairs[i]['pos']['name']} 성향이 강함 (값: {v:.2f})")
        else:
            desc.append(f"{property_pairs[i]['neg']['name']} 성향이 강함 (값: {v:.2f})")
    return '\n'.join(desc)

def cluster_users(users: list[list[float]], n_clusters: int = 4):
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(users)
    centers = kmeans.cluster_centers_
    descriptions = [describe_centroid(c) for c in centers]
    # 군집 결과 로그 가독성 개선
    print("\n[LOG] 군집화 결과:")
    for idx, desc in enumerate(descriptions):
        print(f"\n[군집 {idx+1}]\n{desc}")
    print("")
    return {
        "labels": labels.tolist(),
        "centroids": centers.tolist(),
        "descriptions": descriptions
    }


