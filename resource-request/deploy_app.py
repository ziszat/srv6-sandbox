from kubernetes import client, config


def deploy_application_to_k8s(app_name, namespace, image, cpu, memory, replicas):
    # 从本地 kubeconfig 文件加载集群配置（或者在集群内使用 config.load_incluster_config()）
    config.load_kube_config()

    # 创建 API 实例
    api_instance = client.AppsV1Api()

    # 定义 deployment 规范，包含资源限制
    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=app_name),
        spec=client.V1DeploymentSpec(
            replicas=replicas,  # Pod 副本数量
            selector={"matchLabels": {"app": app_name}},
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": app_name}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name=app_name,
                            image=image,
                            resources=client.V1ResourceRequirements(
                                requests={"cpu": cpu, "memory": memory},
                                limits={"cpu": cpu, "memory": memory},
                            ),
                            ports=[client.V1ContainerPort(container_port=80)],
                        )
                    ]
                ),
            ),
        ),
    )

    # 在指定命名空间下创建 deployment
    api_response = api_instance.create_namespaced_deployment(
        namespace=namespace, body=deployment
    )

    return api_response.to_dict()
