---
translated: true
---

# Using d.run in Cherry Studio

[🍒 Cherry Studio](https://cherry-ai.com/) is a desktop client for LLMs, supporting integration with multiple LLM providers including OpenAI, GPT-3, and d.run.

![Cherry Studio](../images/cherry-studio.jpg)

## Installing Cherry Studio

You can download the installation package from the [Cherry Studio official website](https://cherry-ai.com/).

Versions are available for MacOS, Windows, and Linux.

## Configuring Cherry Studio

Open the Cherry Studio configuration page and add a model provider, such as naming it `d.run` with the provider type set to `OpenAI`.

![Cherry Studio](../images/cherry-studio-2.png)

Enter your API Key and API Host obtained from d.run:

- API Key: Enter your API Key
- API Host:
    - For MaaS, use `https://chat.d.run`
    - For independently deployed models, refer to the model instance details, typically `https://<region>.d.run`

### Managing Available Models

Cherry Studio automatically detects available models. You can enable the models you need from the model list.

![Cherry Studio](../images/cherry-studio-4.png)

## Cherry Studio Usage Demo

![Cherry Studio](../images/cherry-studio-5.png)