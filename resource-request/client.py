import requests

# 代理服务器的地址（hosta 的 IP 地址和端口）
PROXY_SERVER_URL = "http://10.0.0.2:5000/deploy"


def send_deploy_request(app_name, namespace, image, cpu, memory, replicas):
    # 数据封装，包括额外的配置参数：CPU 和内存限制
    data = {
        "app_name": app_name,
        "namespace": namespace,
        "image": image,
        "cpu": cpu,
        "memory": memory,
        "replicas": replicas,
    }

    try:
        response = requests.post(PROXY_SERVER_URL, json=data)

        if response.status_code == 200:
            print(f"Deployment request sent successfully: {response.json()}")
        else:
            print(f"Failed to send request: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error while sending request: {e}")


if __name__ == "__main__":
    # 用户输入部署请求时可以指定应用的资源需求
    app_name = "nginx-app"
    namespace = "default"
    image = "nginx:latest"
    cpu = "500m"  # CPU 请求，例如 500m
    memory = "256Mi"  # 内存请求，例如 256Mi
    replicas = 2  # Pod 副本数量

    # 发送请求
    send_deploy_request(app_name, namespace, image, cpu, memory, replicas)
