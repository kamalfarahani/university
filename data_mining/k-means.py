import matplotlib.pyplot as plt
import pandas as pd

from functools import reduce, partial
from math import sqrt
from typing import List, Tuple, Callable
from point import Point


Metric = Callable[[Point, Point], float]

strictFilter = lambda f, l: list(filter(f,l))
strictMap = lambda f, l: list(map(f, l))
strictZip = lambda it1, it2: list(zip(it1, it2))
strictZipWith = lambda f, it1, it2: strictMap(f , strictZip(it1,it2)) 


def k_means(
    k: int, 
    points: List[Point],
    metric: Callable[[Point, Point], int], 
    centroids:  List[Point] = None,
    max_iter: int = 500,
    current_iter = 0,
    tolerance = 0.00001) -> List[Tuple[Point, int]]:

    if centroids == None:
        centroids = points[:k]
    
    # Currying
    get_nearest_centroid: Callable[[Point], Point] = partial(find_nearest_centroid, centroids, metric)
    
    points_and_clusters: List[Tuple[Point, int]] = strictZip(
        points, strictMap(
            centroids.index, 
            strictMap(get_nearest_centroid, points)))
    
    new_centroids: List[Point] = calculate_new_centroids(k, points_and_clusters)
    if current_iter >= max_iter or get_max_centroid_diffrence_norm(centroids, new_centroids) < tolerance:
        return points_and_clusters
    
    return k_means(k, points, metric, new_centroids, max_iter, current_iter + 1)


def get_max_centroid_diffrence_norm(
    currentCents: List[Point], 
    newCents: List[Point]) -> float:

    return max(strictZipWith(
        lambda two_cents: (two_cents[0] - two_cents[1]).norm(), 
        currentCents, 
        newCents))
    

def calculate_new_centroids(
    k: int, 
    points_and_clusters: List[Tuple[Point, int]]) -> List[Point]:

    clusters: List[List[Point]] = [
        get_cluster_points(i, points_and_clusters) for i in range(k)
    ]

    new_centroids: List[Point] = strictMap(mean_of_cluster, clusters)
    
    return new_centroids

def get_cluster_points(
    cluster_number: int,
    points_and_clusters: List[Tuple[Point, int]]) -> List[Point]:
    
    return strictMap(lambda item: item[0],
        strictFilter(lambda item: item[1] == cluster_number, points_and_clusters))


def mean_of_cluster(cluster: List[Point]) -> Point:
    return reduce(lambda p1, p2: p1 + p2, cluster) / len(cluster)


def find_nearest_centroid(centroids, metric, point: Point) -> Point:
    get_distance_from_point = partial(metric, point)
    index = minIndex(
        strictMap(get_distance_from_point, centroids))

    return centroids[index]


def euclidean_distance(p1: Point, p2: Point) -> float:
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2


def minIndex(l):
    return l.index(min(l))


def get_data() -> List[Point]:
    path = input('Please input the data path: ')
    first_attr = input('Please input first attribute name: ')
    second_attr = input('Please input second attribute name: ')

    data_frame = pd.read_csv(path)
    data = [
        data_frame[first_attr].values.tolist(), 
        data_frame[second_attr].values.tolist()
        ]

    return data

def data_to_points(data) -> List[Point]:
    return strictMap(
        lambda item: Point(item[0], item[1]),
        strictZip(data[0], data[1]))


def plot_clusters(clusters: List[List[Point]]):
    cmap = get_cmap(10)
    for cluster_number, cluster in enumerate(clusters) :
        for point in cluster:
            plt.scatter(
                x = point.x, y = point.y, c = cmap(cluster_number)) 
    
    plt.show()


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def main():
    d = get_data()
    points = data_to_points(d)
    result = k_means(3, points, euclidean_distance)
    clusters = [get_cluster_points(i, result) for i in range(3)]
    
    plot_clusters(clusters)


if __name__ == '__main__':
    main()
