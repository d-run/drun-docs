# 如何构建模型镜像

以下是完整的指导流程，包含拉取模型、构建 Docker 镜像、配置私有仓库，以及将镜像推送到自定义仓库的步骤。

## 1. 拉取 Hugging Face 上的模型

### 1.1 获取模型的 Clone 地址

1. 前往 [Hugging Face](https://huggingface.co)。
2. 找到目标模型，例如 "chatglm3-6b"。
3. 复制模型的 Git URL 以用于克隆，例如：

   ```bash
   https://huggingface.co/THUDM/chatglm3-6b
   ```

### 1.2 Clone 模型

使用以下命令克隆模型（确保已安装 Git 和 Git LFS）：

```bash
git lfs install
git clone https://huggingface.co/THUDM/chatglm3-6b
```

如果克隆失败，请尝试以下步骤：

```bash
# 跳过 smudge - 我们会在后面的步骤中以更快的方式批量下载二进制文件
git lfs install --skip-smudge
# 在这里执行 git clone
git clone https://huggingface.co/THUDM/chatglm3-6b
# 进入克隆的目录（如果是其他模型，注意替换这个目录）
cd chatglm3-6b
# 在新的克隆中获取所有的二进制文件
git lfs pull
# 重新设置 smudge
git lfs install --force
```

## 2. 构建 Docker 镜像

### 2.1 创建 Dockerfile

创建一个名为 `Dockerfile` 的文件，并粘贴以下内容。确保根据实际需求设置 `MODEL_NAME`。

```dockerfile
FROM vllm/vllm-openai:v0.3.3

ARG MODEL_NAME
ENV MODEL_NAME=${MODEL_NAME}

RUN pip install tiktoken

COPY ./${MODEL_NAME} /${MODEL_NAME}

CMD ["--model", "/${MODEL_NAME}", "--trust-remote-code", "--served-model-name", "${MODEL_SERVICE_NAME}"]
```

!!! noty
    请手动替换 Dockerfile 最后一行中的 `MODEL_NAME` 和 `MODEL_SERVICE_NAME`。  
    MODEL_SERVICE_NAME 与模型仓库中填入的名称保持一致:
    ![create-model](../images/create-model.png)
    示例：

    ```dockerfile
    CMD ["--model", "/chatglm3-6b", "--trust-remote-code", "--served-model-name", "new-chatglm3-6b"]
    ```

### 2.2 构建 Docker 镜像

使用正确的 `MODEL_NAME` 和镜像标签构建 Docker 镜像。示例中使用 `vllm-openai-tiktoken-chatglm3-6b-server` 作为镜像名称。

```bash
docker build --build-arg MODEL_NAME=chatglm3-6b -t vllm-openai-tiktoken-chatglm3-6b-server .
```

## 3. 推送镜像到自定义 Docker 仓库

### 3.1 登录到 Docker 仓库

如果要推送到 Docker Hub 或其他私有仓库，请确保已登录到相应的 Docker 仓库。

```bash
docker login
```

对于其他仓库，例如 Google Container Registry 或 Amazon ECR，需要根据其文档指引进行登录和身份验证。

### 3.2 配置镜像标签

在推送镜像之前，将镜像标签配置为目标仓库地址。以下示例使用自定义的私有仓库地址：

```bash
# 假设你的仓库地址是 myregistry.example.com
docker tag vllm-openai-tiktoken-chatglm3-6b-server myregistry.example.com/vllm-openai-tiktoken-chatglm3-6b-server
```

### 3.3 推送镜像到仓库

将镜像推送到目标仓库：

```bash
docker push myregistry.example.com/vllm-openai-tiktoken-chatglm3-6b-server
```

### 3.4 验证推送成功

确认推送成功后，可以在 Docker 仓库的仪表盘上查看已推送的镜像。
