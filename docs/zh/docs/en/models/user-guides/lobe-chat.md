---
translated: true
---

# Using Lobe Chat Translator

[Lobe Chat](https://lobehub.com/en) is an open-source modern AI chat framework.
It supports multiple AI providers (OpenAI/Claude 3/Gemini/Ollama/Qwen/DeepSeek), knowledge bases (file uploads/knowledge management/RAG), and multi-modality (visual/TTS/plugins/art). Deploy your private ChatGPT/Claude application for free with one click.

![Lobe Chat](../images/lobe-chat.png)

## Install Lobe Chat

For detailed installation instructions, please refer to the
[official documentation of Lobe Chat](https://lobehub.com/en/docs/self-hosting/start).
Lobe Chat offers various deployment and installation methods.

This guide uses Docker as an example, primarily introducing how to use d.run's model service.

```bash

# LobeChat supports configuring API Key and API Host directly during deployment

$ docker run -d -p 3210:3210 \
    -e OPENAI_API_KEY=sk-xxxx \  # Enter your API Key
    -e OPENAI_PROXY_URL=https://chat.d.run/v1 \  # Enter your API Host
    -e ENABLED_OLLAMA=0 \
    -e ACCESS_CODE=drun \
    --name lobe-chat \
    lobehub/lobe-chat:latest
```

## Configure Lobe Chat

Lobe Chat also allows users to add model service provider configurations after deployment.

![Lobe Chat](../images/lobe-chat-2.png)

Enter the API Key and API Host obtained from d.run.

- API Key: Enter your API Key
- API Host:
    - For MaaS, use `https://chat.d.run`
    - For independently deployed models, check the model instance details, typically `https://<region>.d.run`
- Configure custom models: e.g., `public/deepseek-r1`

## Lobe Chat Usage Demo

![Lobe Chat](../images/lobe-chat-3.png)
