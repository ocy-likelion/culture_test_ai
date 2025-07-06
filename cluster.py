from sklearn.cluster import KMeans

def cluster_users(users: list[list[float]], n_clusters: int = 4):
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(users)
    centers = kmeans.cluster_centers_
    return {
        "labels": labels.tolist(),
        "centroids": centers.tolist()
    }
