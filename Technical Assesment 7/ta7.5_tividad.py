# TA 7.5 - QNA

data_points = [2, 4, 10, 12, 3, 20, 30, 11, 25]

mean_1 = 4
mean_2 = 11

# puts each point in the cluster of the closest mean
# prints a table like the one in the problem (D1 = distance to M1, D2 = distance to M2)
def assign_clusters(points, first_mean, second_mean):
    cluster_1 = []
    cluster_2 = []

    print("Datapoint   D1    D2    Cluster")
    for point in points:
        distance_1 = abs(point - first_mean)
        distance_2 = abs(point - second_mean)

        if distance_1 <= distance_2:
            cluster_name = "C1"
            cluster_1.append(point)
        else:
            cluster_name = "C2"
            cluster_2.append(point)

        # round so we don't get long decimals like 15.600000000000001
        print(str(point).ljust(12) + str(round(distance_1, 2)).ljust(7)
              + str(round(distance_2, 2)).ljust(7) + cluster_name)

    return cluster_1, cluster_2

# mean = sum of all the points divided by how many points there are
def get_mean(cluster):
    total = 0
    for point in cluster:
        total = total + point
    return total / len(cluster)

print("ITERATION 1")
print("M1 = " + str(mean_1) + ", M2 = " + str(mean_2))
cluster_1, cluster_2 = assign_clusters(data_points, mean_1, mean_2)
print("C1 = " + str(cluster_1))
print("C2 = " + str(cluster_2))
print("")

for iteration_number in [2, 3]:
    # new means come from the clusters of the previous iteration
    mean_1 = get_mean(cluster_1)
    mean_2 = get_mean(cluster_2)

    print("ITERATION " + str(iteration_number))
    print("M1 = " + str(mean_1) + ", M2 = " + str(mean_2))
    cluster_1, cluster_2 = assign_clusters(data_points, mean_1, mean_2)
    print("C1 = " + str(cluster_1))
    print("C2 = " + str(cluster_2))
    print("")