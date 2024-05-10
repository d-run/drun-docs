# 接入模型镜像

## 支持的模型

当前模型中心支持在 [HuggingFace Transformers](https://huggingface.co/models) 中的各种生成式 Transformer 模型。
以下是目前支持的模型架构列表。

.. list-table::
  :widths: 25 25 50 5
  :header-rows: 1

  * - Architecture
    - Models
    - Example HuggingFace Models
    - :ref:`LoRA <lora>`
  * - :code:`AquilaForCausalLM`
    - Aquila
    - :code:`BAAI/Aquila-7B`, :code:`BAAI/AquilaChat-7B`, etc.
    - ✅︎
  * - :code:`BaiChuanForCausalLM`
    - Baichuan
    - :code:`baichuan-inc/Baichuan2-13B-Chat`, :code:`baichuan-inc/Baichuan-7B`, etc.
    - ✅︎
  * - :code:`ChatGLMModel`
    - ChatGLM
    - :code:`THUDM/chatglm2-6b`, :code:`THUDM/chatglm3-6b`, etc.
    - ✅︎
  * - :code:`CohereForCausalLM`
    - Command-R
    - :code:`CohereForAI/c4ai-command-r-v01`, etc.
    -
  * - :code:`DbrxForCausalLM`
    - DBRX
    - :code:`databricks/dbrx-base`, :code:`databricks/dbrx-instruct`, etc.
    -
  * - :code:`DeciLMForCausalLM`
    - DeciLM
    - :code:`Deci/DeciLM-7B`, :code:`Deci/DeciLM-7B-instruct`, etc.
    -
  * - :code:`BloomForCausalLM`
    - BLOOM, BLOOMZ, BLOOMChat
    - :code:`bigscience/bloom`, :code:`bigscience/bloomz`, etc.
    -
  * - :code:`FalconForCausalLM`
    - Falcon
    - :code:`tiiuae/falcon-7b`, :code:`tiiuae/falcon-40b`, :code:`tiiuae/falcon-rw-7b`, etc.
    -
  * - :code:`GemmaForCausalLM`
    - Gemma
    - :code:`google/gemma-2b`, :code:`google/gemma-7b`, etc.
    - ✅︎
  * - :code:`GPT2LMHeadModel`
    - GPT-2
    - :code:`gpt2`, :code:`gpt2-xl`, etc.
    -
  * - :code:`GPTBigCodeForCausalLM`
    - StarCoder, SantaCoder, WizardCoder
    - :code:`bigcode/starcoder`, :code:`bigcode/gpt_bigcode-santacoder`, :code:`WizardLM/WizardCoder-15B-V1.0`, etc.
    -
  * - :code:`GPTJForCausalLM`
    - GPT-J
    - :code:`EleutherAI/gpt-j-6b`, :code:`nomic-ai/gpt4all-j`, etc.
    -
  * - :code:`GPTNeoXForCausalLM`
    - GPT-NeoX, Pythia, OpenAssistant, Dolly V2, StableLM
    - :code:`EleutherAI/gpt-neox-20b`, :code:`EleutherAI/pythia-12b`, :code:`OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5`, :code:`databricks/dolly-v2-12b`, :code:`stabilityai/stablelm-tuned-alpha-7b`, etc.
    -
  * - :code:`InternLMForCausalLM`
    - InternLM
    - :code:`internlm/internlm-7b`, :code:`internlm/internlm-chat-7b`, etc.
    - ✅︎
  * - :code:`InternLM2ForCausalLM`
    - InternLM2
    - :code:`internlm/internlm2-7b`, :code:`internlm/internlm2-chat-7b`, etc.
    -
  * - :code:`JAISLMHeadModel`
    - Jais
    - :code:`core42/jais-13b`, :code:`core42/jais-13b-chat`, :code:`core42/jais-30b-v3`, :code:`core42/jais-30b-chat-v3`, etc.
    -
  * - :code:`LlamaForCausalLM`
    - LLaMA, Llama 2, Meta Llama 3, Vicuna, Alpaca, Yi
    - :code:`meta-llama/Meta-Llama-3-8B-Instruct`, :code:`meta-llama/Meta-Llama-3-70B-Instruct`, :code:`meta-llama/Llama-2-13b-hf`, :code:`meta-llama/Llama-2-70b-hf`, :code:`openlm-research/open_llama_13b`, :code:`lmsys/vicuna-13b-v1.3`, :code:`01-ai/Yi-6B`, :code:`01-ai/Yi-34B`, etc.
    - ✅︎
  * - :code:`MiniCPMForCausalLM`
    - MiniCPM
    - :code:`openbmb/MiniCPM-2B-sft-bf16`, :code:`openbmb/MiniCPM-2B-dpo-bf16`, etc.
    -
  * - :code:`MistralForCausalLM`
    - Mistral, Mistral-Instruct
    - :code:`mistralai/Mistral-7B-v0.1`, :code:`mistralai/Mistral-7B-Instruct-v0.1`, etc.
    - ✅︎
  * - :code:`MixtralForCausalLM`
    - Mixtral-8x7B, Mixtral-8x7B-Instruct
    - :code:`mistralai/Mixtral-8x7B-v0.1`, :code:`mistralai/Mixtral-8x7B-Instruct-v0.1`, :code:`mistral-community/Mixtral-8x22B-v0.1`, etc.
    - ✅︎
  * - :code:`MPTForCausalLM`
    - MPT, MPT-Instruct, MPT-Chat, MPT-StoryWriter
    - :code:`mosaicml/mpt-7b`, :code:`mosaicml/mpt-7b-storywriter`, :code:`mosaicml/mpt-30b`, etc.
    -
  * - :code:`OLMoForCausalLM`
    - OLMo
    - :code:`allenai/OLMo-1B-hf`, :code:`allenai/OLMo-7B-hf`, etc.
    -
  * - :code:`OPTForCausalLM`
    - OPT, OPT-IML
    - :code:`facebook/opt-66b`, :code:`facebook/opt-iml-max-30b`, etc.
    -
  * - :code:`OrionForCausalLM`
    - Orion
    - :code:`OrionStarAI/Orion-14B-Base`, :code:`OrionStarAI/Orion-14B-Chat`, etc.
    -
  * - :code:`PhiForCausalLM`
    - Phi
    - :code:`microsoft/phi-1_5`, :code:`microsoft/phi-2`, etc.
    -
  * - :code:`Phi3ForCausalLM`
    - Phi-3
    - :code:`microsoft/Phi-3-mini-4k-instruct`, :code:`microsoft/Phi-3-mini-128k-instruct`, etc.
    -
  * - :code:`QWenLMHeadModel`
    - Qwen
    - :code:`Qwen/Qwen-7B`, :code:`Qwen/Qwen-7B-Chat`, etc.
    -
  * - :code:`Qwen2ForCausalLM`
    - Qwen2
    - :code:`Qwen/Qwen2-beta-7B`, :code:`Qwen/Qwen2-beta-7B-Chat`, etc.
    - ✅︎
  * - :code:`Qwen2MoeForCausalLM`
    - Qwen2MoE
    - :code:`Qwen/Qwen1.5-MoE-A2.7B`, :code:`Qwen/Qwen1.5-MoE-A2.7B-Chat`, etc.
    -
  * - :code:`StableLmForCausalLM`
    - StableLM
    - :code:`stabilityai/stablelm-3b-4e1t/` , :code:`stabilityai/stablelm-base-alpha-7b-v2`, etc.
    -

## 如何为模型构建镜像

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
