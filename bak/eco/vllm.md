# vLLM

这是一款针对大语言模型设计的高效推理引擎。

使用此推理引擎的大致步骤为：

* [在数据集上运行离线批量推理](#_1)
* [为大型语言模型构建 API 服务器](#openai)
* [启动兼容 OpenAI 的 API 服务器](#openai-chat-api-vllm)

!!! note

    默认情况下，vLLM 从 `HuggingFace <https://huggingface.co/>`_ 下载模型。
    如果你想在以下示例中使用 `ModelScope <https://www.modelscope.cn>`_ 的模型，请设置环境变量：

    ```bash
    export VLLM_USE_MODELSCOPE=True
    ```

## 离线批量推理

首先展示一个使用 vLLM 在数据集上进行离线批量推理的示例。换句话说，我们使用 vLLM 为一系列输入提示生成文本。

从 vLLM 导入 ``LLM`` 和 ``SamplingParams``。``LLM`` 类是使用 vLLM 引擎进行离线推理的主要类。``SamplingParams`` 类指定采样过程的参数。

```python
from vllm import LLM, SamplingParams
```

定义输入提示列表和生成的采样参数。采样温度设置为 0.8，核采样概率设置为 0.95。有关采样参数的更多信息，请参阅 `类定义 <https://github.com/vllm-project/vllm/blob/main/vllm/sampling_params.py>`_。

```python
prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
```

使用 ``LLM`` 类和 `OPT-125M 模型 <https://arxiv.org/abs/2205.01068>`_ 初始化 vLLM 的离线推理引擎。支持的模型列表可以在 :ref:`supported models <supported_models>` 中找到。

```python
llm = LLM(model="facebook/opt-125m")
```

调用 `llm.generate` 生成输出。它将输入提示添加到 vLLM 引擎的等待队列中，并执行 vLLM 引擎以高吞吐量生成输出。输出作为 `RequestOutput` 对象列表返回，其中包括所有输出的 tokens。

```python
outputs = llm.generate(prompts, sampling_params)
# 打印输出。
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

该代码示例也可以在 `examples/offline_inference.py <https://github.com/vllm-project/vllm/blob/main/examples/offline_inference.py>`_ 中找到。

## 兼容 OpenAI 的服务器

vLLM 可以部署为实现 OpenAI API 协议的服务器。这允许 vLLM 作为使用 OpenAI API 的应用程序的替代品使用。
默认情况下，它在 `http://localhost:8000` 启动服务器。你可以使用 `--host` 和 `--port` 参数指定地址。服务器目前一次托管一个模型（如下命令中的 OPT-125M），并实现 `列出模型 <https://platform.openai.com/docs/api-reference/models/list>`_、`创建聊天完成 <https://platform.openai.com/docs/api-reference/chat/completions/create>`_ 和 `创建完成 <https://platform.openai.com/docs/api-reference/completions/create>`_ 端点。我们正在积极添加更多端点的支持。

启动服务器：

```bash
python -m vllm.entrypoints.openai.api_server \
    --model facebook/opt-125
```

默认情况下，服务器使用存储在分词器中的预定义聊天模板。你可以使用 ``--chat-template`` 参数覆盖此模板：

```bash
python -m vllm.entrypoints.openai.api_server \
    --model facebook/opt-125m \
    --chat-template ./examples/template_chatml.jinja
```

该服务器可以以与 OpenAI API 相同的格式进行查询。例如，列出模型：

```bash
curl http://localhost:8000/v1/models
```

你可以传入参数 ``--api-key`` 或环境变量 ``VLLM_API_KEY`` 以启用服务器检查头中的 API 密钥。

使用 OpenAI 完成 API 和 vLLM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

使用输入提示查询模型：

```bash
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "facebook/opt-125m",
        "prompt": "San Francisco is a",
        "max_tokens": 7,
        "temperature": 0
    }'
```

由于该服务器兼容 OpenAI API，你可以将其用作任何使用 OpenAI API 的应用程序的替代品。例如，另一种查询服务器的方法是通过 ``openai`` python 包：

```python
from openai import OpenAI

# 修改 OpenAI 的 API 密钥和 API 基础 URL 以使用 vLLM 的 API 服务器。
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)
completion = client.completions.create(model="facebook/opt-125m",
                                    prompt="San Francisco is a")
print("Completion result:", completion)
```

有关更详细的客户端示例，请参阅 `examples/openai_completion_client.py <https://github.com/vllm-project/vllm/blob/main/examples/openai_completion_client.py>`_。

## 使用 OpenAI Chat API 和 vLLM

vLLM 服务器设计为支持 OpenAI Chat API，允许你与模型进行动态对话。聊天界面是一种更具互动性的方法与模型进行交流，允许进行可以存储在聊天历史中的来回交流。这对于需要上下文或更详细解释的任务非常有用。

使用 OpenAI Chat API 查询模型：

你可以使用 `创建聊天完成 <https://platform.openai.com/docs/api-reference/chat/completions/create>`_ 端点以聊天界面的方式与模型进行交流：

```bash
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
         "model": "facebook/opt-125m",
         "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    }'
```

Python 客户端示例：

使用 `openai` python 包，你也可以以聊天的方式与模型进行交流：

```python
from openai import OpenAI
# 设置 OpenAI 的 API 密钥和 API 基础 URL 以使用 vLLM 的 API 服务器。
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

chat_response = client.chat.completions.create(
    model="facebook/opt-125m",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ]
)
print("Chat response:", chat_response)
```

有关Chat API 的更多详细示例和高级功能，你可以参考 OpenAI 官方文档。

## 参考

- [vLLM 仓库](https://github.com/vllm-project/vllm)
- [vLLM 文档](https://docs.vllm.ai/en/latest/)
