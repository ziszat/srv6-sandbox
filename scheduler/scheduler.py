import requests
import numpy as np

MASTER_IP = {
    "hosta": "localhost",
    "hostb": "localhost",
}

MASTER_PORT = {
    "hosta": 30091,
    "hostb": 30092,
}

masters = ["hosta", "hostb"]

def query_prometheus(prometheus_ip, port, query):
    url = f"http://{prometheus_ip}:{port}/api/v1/query"
    response = requests.get(url, params={"query": query})
    if response.status_code == 200:
        return response.json().get("data", {}).get("result", [])
    else:
        print(f"Error querying Prometheus: {response.status_code}")
        return []


def get_free_resources(prometheus_ip, port):
    # Query for CPU, Memory, and Storage
    cpu_query = '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
    mem_query = "node_memory_MemAvailable_bytes"
    storage_query = 'node_filesystem_avail_bytes{mountpoint="/"}'

    cpu_usage = query_prometheus(prometheus_ip, port, cpu_query)
    memory_available = query_prometheus(prometheus_ip, port, mem_query)
    storage_available = query_prometheus(prometheus_ip, port, storage_query)

    return {
        "cpu_usage": cpu_usage,
        "memory_available": memory_available,
        "storage_available": storage_available,
    }


def get_resource(prometheus_ips, ports):
    resources = []
    for i in range(len(ports)):
        resources.append(get_free_resources(prometheus_ips[i], ports[i]))
    return resources


# 提取并聚合数据
def aggregate_resource_data(resources):
    aggregated_data = []
    for res in resources:
        # 取每个集群中节点的 CPU、内存、存储的平均值
        avg_cpu = np.mean([float(node["value"][1]) for node in res["cpu_usage"]])
        avg_memory = np.mean(
            [float(node["value"][1]) for node in res["memory_available"]]
        )
        avg_storage = np.mean(
            [float(node["value"][1]) for node in res["storage_available"]]
        )

        # 将每个集群的数据聚合为一行，表示为 [cpu, memory, storage]
        aggregated_data.append([avg_cpu, avg_memory, avg_storage])
    return np.array(aggregated_data)


# 归一化处理
def normalize(data):
    min_vals = data.min(axis=0)
    max_vals = data.max(axis=0)
    norm_data = (data - min_vals) / (max_vals - min_vals)
    return norm_data


# 计算熵
def calculate_entropy(norm_data):
    epsilon = 1e-10  # 防止 log(0)
    p = norm_data / norm_data.sum(axis=0)
    entropy = -np.sum(p * np.log(p + epsilon), axis=0) / np.log(len(norm_data))
    return entropy


# 计算权重
def calculate_weights(entropy):
    return (1 - entropy) / (len(entropy) - np.sum(entropy))


# 计算综合评分
def calculate_scores(norm_data, weights):
    p = norm_data / norm_data.sum(axis=0)
    return np.dot(p, weights)


# 选择最优集群
def select_best_cluster(scores):
    return masters[np.argmax(scores)]  # 返回最佳集群的索引 (+1 是为了从 1 开始)


prometheus_ips = []
ports = []
for master in masters:
    ports.append(MASTER_PORT[master])
    prometheus_ips.append(MASTER_IP[master])

resources = get_resource(prometheus_ips, ports)
# print(resources)


# resources = get_resource(prometheus_ip, ports)

# resources = [
#     {
#         "cpu_usage": [
#             {"instance": "master", "value": [1697458245.123, "20.5"]},
#             {"instance": "node1", "value": [1697458245.456, "35.7"]},
#         ],
#         "memory_available": [
#             {"instance": "master", "value": [1697458245.123, "6457433088"]},
#             {"instance": "node1", "value": [1697458245.456, "4315213824"]},
#         ],
#         "storage_available": [
#             {"instance": "master", "value": [1697458245.123, "254612832768"]},
#             {"instance": "node1", "value": [1697458245.456, "128712832768"]},
#         ],
#     },
#     {
#         "cpu_usage": [
#             {"instance": "master", "value": [1697458300.123, "45.2"]},
#             {"instance": "node1", "value": [1697458300.456, "10.3"]},
#         ],
#         "memory_available": [
#             {"instance": "master", "value": [1697458300.123, "5438213120"]},
#             {"instance": "node1", "value": [1697458300.456, "7895213824"]},
#         ],
#         "storage_available": [
#             {"instance": "master", "value": [1697458300.123, "512432768000"]},
#             {"instance": "node1", "value": [1697458300.456, "612832768000"]},
#         ],
#     },
#     {
#         "cpu_usage": [
#             {"instance": "master", "value": [1697458355.123, "15.7"]},
#             {"instance": "node1", "value": [1697458355.456, "25.4"]},
#             {"instance": "node2", "value": [1697458355.789, "30.2"]},
#         ],
#         "memory_available": [
#             {"instance": "master", "value": [1697458355.123, "9876543216"]},
#             {"instance": "node1", "value": [1697458355.456, "7654321984"]},
#             {"instance": "node2", "value": [1697458355.789, "6543210987"]},
#         ],
#         "storage_available": [
#             {"instance": "master", "value": [1697458355.123, "300000000000"]},
#             {"instance": "node1", "value": [1697458355.456, "200000000000"]},
#             {"instance": "node2", "value": [1697458355.789, "150000000000"]},
#         ],
#     },
# ]

# 对resources进行数据聚合处理
aggregated_resources = aggregate_resource_data(resources)
print("Aggregated Data (CPU, Memory, Storage):")
print(aggregated_resources)

# 归一化处理
norm_resources = normalize(aggregated_resources)
print("\nNormalized Data:")
print(norm_resources)

# 计算熵
entropy = calculate_entropy(norm_resources)
print("\nEntropy:")
print(entropy)

# 计算权重
weights = calculate_weights(entropy)
print("\nWeights:")
print(weights)

# 计算每个集群的综合评分
scores = calculate_scores(norm_resources, weights)
print("\nScores:")
print(scores)

# 选择最优集群
best_cluster = select_best_cluster(scores)
print(f"\nBest Cluster Master: {best_cluster}")
print(f"Cluster Master IP: {MASTER_IP[best_cluster]}")
