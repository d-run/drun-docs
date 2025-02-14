---
status: new
translated: true
---

# Model Invocation

The `d.run` platform offers two deployment options for large language models, allowing you to choose based on your specific needs:

- **MaaS by Token**: Utilizes token-based billing, sharing resources, and enables model invocation without requiring instance deployment
- **Model Service**: Provides dedicated instances with per-instance billing, offering unlimited API call access

## Supported Models and Deployment Options

| Model Name                    | MaaS by Token | Model Service |
| ----------------------------- | ------------- | ------------- |
| 🔥 DeepSeek-R1                | ✅            |               |
| 🔥 DeepSeek-V3                | ✅            |               |
| Phi-4                         |               | ✅            |
| Phi-3.5-mini-instruct         |               | ✅            |
| Qwen2-0.5B-Instruct           |               | ✅            |
| Qwen2.5-7B-Instruct           | ✅            | ✅            |
| Qwen2.5-14B-Instruct          |               | ✅            |
| Qwen2.5-Coder-32B-Instruct    |               | ✅            |
| Qwen2.5-72B-Instruct-AWQ      | ✅            | ✅            |
| baichuan2-13b-Chat            |               | ✅            |
| Llama-3.2-11B-Vision-Instruct | ✅            | ✅            |
| glm-4-9b-chat                 | ✅            | ✅            |

## Model Endpoints

A model endpoint is a URL or API address that allows users to access and send requests for model inference.

| Invocation Method | Endpoint            |
| ----------------- | ------------------- |
| MaaS by Token     | `chat.d.run`        |
| Model Service     | `<region>-02.d.run` |

## API Invocation Examples

### Invoking via MaaS by Token

To invoke models using the MaaS by Token method, follow these steps:

1. **Obtain API Key**: Log in to your user console and create a new API Key
2. **Set Endpoint**: Replace the SDK endpoint with `chat.d.run`
3. **Invoke Model**: Use the official model name along with the new API Key for invocation

**Example Code (Python)**:

```python
import openai

openai.api_key = "your-api-key"  # Replace with your API Key
openai.api_base = "https://chat.d.run"

response = openai.Completion.create(
  model="public/deepseek-r1",
  prompt="What is your name?"
)

print(response.choices[0].text)
```

### Invoking via Model Service

To invoke models using the Model Service method, follow these steps:

1. **Obtain API Key**: Log in to your user console and create a new API Key
2. **Set Endpoint**: Replace the SDK endpoint with `<region>-02.d.run`
3. **Invoke Model**: Use the official model name along with the new API Key for invocation

**Example Code (Python)**:

```python
import openai

openai.api_key = "your-api-key"  # Replace with your API Key
openai.api_base = "<region>-02.d.run"

response = openai.Completion.create(
  model="u-1100a15812cc/qwen2",
  prompt="What is your name?"
)

print(response.choices[0].text)
```

## Support and Feedback

For any questions or feedback, please contact our [Technical Support Team](../contact/index.md).
