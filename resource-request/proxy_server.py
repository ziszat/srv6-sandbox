from flask import Flask, request, jsonify
from deploy_app import deploy_application_to_k8s

app = Flask(__name__)


@app.route("/deploy", methods=["POST"])
def deploy():
    try:
        # 从客户端请求中获取数据
        data = request.get_json()
        app_name = data.get("app_name")
        namespace = data.get("namespace")
        image = data.get("image")
        cpu = data.get("cpu")
        memory = data.get("memory")
        replicas = data.get("replicas")

        # 调用部署函数，传入资源限制参数
        result = deploy_application_to_k8s(
            app_name, namespace, image, cpu, memory, replicas
        )

        return jsonify({"message": "Deployment successful", "result": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # 代理服务器在 5000 端口上运行
    app.run(host="0.0.0.0", port=5000)
