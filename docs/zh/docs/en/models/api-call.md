# Model Invocation

d.run offers two ways to host large language models. You can choose based on your needs:

* **MaaS by Token**: Billed by token usage. Resources are shared, and users can call models without deploying their own instances.
* **Dedicated Model Service**: Users get exclusive instances, billed by instance, with no limit on API call volume.

## Currently Supported Models and Hosting Options

| Model Name                    | MaaS by Token | Dedicated Service |
| ----------------------------- | ------------- | ----------------- |
| 🔥 DeepSeek-R1                | ✅             |                   |
| 🔥 DeepSeek-V3                | ✅             |                   |
| Phi-4                         |               | ✅                 |
| Phi-3.5-mini-instruct         |               | ✅                 |
| Qwen2-0.5B-Instruct           |               | ✅                 |
| Qwen2.5-7B-Instruct           | ✅             | ✅                 |
| Qwen2.5-14B-Instruct          |               | ✅                 |
| Qwen2.5-Coder-32B-Instruct    |               | ✅                 |
| Qwen2.5-72B-Instruct-AWQ      | ✅             | ✅                 |
| baichuan2-13b-Chat            |               | ✅                 |
| Llama-3.2-11B-Vision-Instruct | ✅             | ✅                 |
| glm-4-9b-chat                 | ✅             | ✅                 |

## Model Endpoint

A model endpoint is a URL or API address users can send requests to in order to run inference.

| Access Method     | Endpoint             |
| ----------------- | -------------------- |
| MaaS by Token     | `https://chat.d.run` |
| Dedicated Service | `<region>.d.run`     |

## Example API Usage

### Using MaaS by Token

To call a model via MaaS by Token, follow these steps:

1. **Get an API Key**: Log in to the user console and [create a new API key](./apikey.md)
2. **Set the Endpoint**: Set your SDK's endpoint to `https://chat.d.run`
3. **Call the Model**: Use the official model name along with your API key

**Example Code (Python):**

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

### Using a Dedicated Model Instance

To call a model hosted on your own instance, follow these steps:

1. **Deploy a Model Instance**: Deploy in a specified region, e.g., `sh-02`
2. **Get an API Key**: Log in to the user console and create a new API key
3. **Set the Endpoint**: Set your SDK's endpoint to `<region>.d.run`, e.g., `sh-02.d.run`
4. **Call the Model**: Use the official model name and your API key

**Example Code (Python):**

```python
import openai

openai.api_key = "your-api-key"  # Replace with your API Key
openai.api_base = "https://sh-02.d.run"  # Replace with your instance's region

response = openai.Completion.create(
  model="u-1100a15812cc/qwen2",  # Replace with your model's full name
  prompt="What is your name?"
)

print(response.choices[0].text)
```

## Frequently Asked Questions

### Q1: How should I choose the invocation method?

* **MaaS by Token**: Best for lightweight or infrequent use cases.
* **Dedicated Instance**: Ideal for high-performance and high-frequency usage.

### Q2: How do I view my API Key?

Log in to the user console and go to the API Key management page. See [API Key Management](apikey.md) for more details.

### Q3: How do I find the model name?

* For MaaS by Token, model names follow the format `public/<model_name>`, such as `public/deepseek-r1`, which can be found on the model details page.
* For dedicated services, model names follow the format `<username>/<model_name>`, such as `u-1100a15812cc/qwen2`, and can be copied directly from your model list.

### Q4: How is pricing calculated for dedicated model instances?

Pricing is based on region, instance type, and usage time. For details, refer to the instance pricing page in your user console.

## Support & Feedback

For any questions or feedback, please contact our [technical support team](../contact/index.md).
