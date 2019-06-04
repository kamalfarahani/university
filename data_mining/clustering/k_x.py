import matplotlib.pyplot as plt
import pandas as pd

from functools import reduce, partial
from math import sqrt
from typing import List, Tuple, Callable
from utils import min_index, get_cmap
from point import Point, euclidean_distance, manhattan_distance, mean_of_points, median_of_points, medoid_of_points


Metric = Callable[[Point, Point], float]
CentroidCalcMethod = Callable[[List[Point]], Point]

strictFilter = lambda f, l: list(filter(f,l))
strictMap = lambda f, l: list(map(f, l))
strictZip = lambda it1, it2: list(zip(it1, it2))
strictZipWith = lambda f, it1, it2: [f(a, b) for (a, b) in strictZip(it1, it2)]


def k_x_clustring(
    k: int, 
    points: List[Point],
    metric: Callable[[Point, Point], int],
    cent_calc_method: CentroidCalcMethod, 
    centroids:  List[Point] = None,
    max_iter: int = 500,
    current_iter = 0,
    tolerance = 0.00001) -> Tuple[List[Tuple[Point, int]], List[Point]]:

    if centroids == None:
        centroids = points[:k]
    
    # Currying
    get_nearest_centroid: Callable[[Point], Point] = partial(find_nearest_centroid, centroids, metric)
    
    points_and_clusters: List[Tuple[Point, int]] = strictZip(
        points, strictMap(
            centroids.index, 
            strictMap(get_nearest_centroid, points)))
    
    new_centroids: List[Point] = calculate_new_centroids(cent_calc_method, k, points_and_clusters)
    if current_iter >= max_iter or get_max_centroid_diffrence_norm(centroids, new_centroids) < tolerance:
        return (points_and_clusters, centroids)
    
    return k_x_clustring(
        k, points, metric, cent_calc_method, new_centroids, max_iter, current_iter + 1, tolerance)


def k_means(k, points, max_iter=500, tolerance=0.00001):
    return k_x_clustring(
        k, points, euclidean_distance, mean_of_points, max_iter=max_iter, tolerance=tolerance)


def k_medians(k, points, max_iter=500, tolerance=0.00001):
    return k_x_clustring(
        k, points, manhattan_distance, median_of_points, max_iter=max_iter, tolerance=tolerance)


def k_medoids(k, points, max_iter=500, tolerance=0.00001):
    return k_x_clustring(
        k, points, euclidean_distance, medoid_of_points, max_iter=max_iter, tolerance=tolerance)

def get_max_centroid_diffrence_norm(
    currentCents: List[Point], 
    newCents: List[Point]) -> float:

    return max(strictZipWith(
        lambda cent1, cent2: (cent1 - cent2).norm(), 
        currentCents, 
        newCents))
    

def calculate_new_centroids(
    cent_calc_method: CentroidCalcMethod,
    k: int,
    points_and_clusters: List[Tuple[Point, int]]) -> List[Point]:

    clusters: List[List[Point]] = [
        get_cluster_points(i, points_and_clusters) for i in range(k)
    ]

    new_centroids: List[Point] = strictMap(cent_calc_method, clusters)
    
    return new_centroids


def get_cluster_points(
    cluster_number: int,
    points_and_clusters: List[Tuple[Point, int]]) -> List[Point]:
    
    return strictMap(lambda item: item[0],
        strictFilter(lambda item: item[1] == cluster_number, points_and_clusters))


def mean_of_cluster(cluster: List[Point]) -> Point:
    return mean_of_points(cluster)


def find_nearest_centroid(centroids, metric, point: Point) -> Point:
    get_distance_from_point = partial(metric, point)
    index = min_index(
        strictMap(get_distance_from_point, centroids))

    return centroids[index]


def get_data() -> List[Point]:
    path = input('Please input the data path: ')
    first_attr = input('Please input first attribute name: ')
    second_attr = input('Please input second attribute name: ')
    k = int(input('Enter number of clusters: '))

    data_frame = pd.read_csv(path)
    data = [
        data_frame[first_attr].values.tolist(), 
        data_frame[second_attr].values.tolist()
	]

    return (data, k)

def data_to_points(data) -> List[Point]:
    return strictMap(
        lambda item: Point(item[0], item[1]),
        strictZip(data[0], data[1]))


def plot_clusters(clusters: List[List[Point]], cents: List[Point]):
    cmap = get_cmap(10)
    for cluster_number, cluster in enumerate(clusters) :
        for point in cluster:
            plt.scatter(
                x = point.x, y = point.y, c = cmap(cluster_number))
        
        current_cent = cents[cluster_number]
        plt.scatter(
                x = current_cent.x, y = current_cent.y, c = 'black')
    
    plt.show()


def main():
    d, k = get_data()
    points = data_to_points(d)
    method = input('Enter clustring method: ')
    method_to_func = {
        'k-means': k_means,
        'k-medians': k_medians,
        'k-medoids': k_medoids
    }

    result, cents = method_to_func[method](k, points)
    clusters = [get_cluster_points(i, result) for i in range(k)]
    
    plot_clusters(clusters, cents)


if __name__ == '__main__':
    main()
