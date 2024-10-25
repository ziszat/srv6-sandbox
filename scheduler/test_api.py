import requests
import numpy as np

MASTER_IP = {
    "hosta": "10.0.0.2",
    "hostb": "10.0.1.2",
    "hostc": "10.0.x.2",
}

MASTER_PORT = {
    "hosta": 30090,
    "hostb": 9090,
    "hostc": 9090
}

masters = ["hosta"]

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


def get_resource(prometheus_ip, port):
    resources = []
    for _, port in enumerate(ports):
        resources.append(get_free_resources(prometheus_ip, port))
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


prometheus_ip = "localhost"
ports = []
for master in masters:
    ports.append(MASTER_PORT[master])

resources = get_resource(prometheus_ip, ports)