---
translated: true
---

# Using d.run in Bob Translate

This guide explains how to call model services from d.run within Bob Translate.

[Bob](https://bobtranslate.com/) is a macOS platform translation and OCR software that allows you to translate and perform OCR directly within any application. It's quick, efficient, and easy to use!

![Bob Translate](../images/bobtranslate.png)

## Installing Bob Translate

You can download and install Bob Translate from the [Mac App Store](https://apps.apple.com/cn/app/bob-%E7%BF%BB%E8%AF%91%E5%92%8C-ocr-%E5%B7%A5%E5%85%B7/id1630034110).

## Configuring Bob Translate

Open the settings page in Bob Translate, add a translation service, and select the service type as `OpenAI`.

![Bob Translate](../images/bobtranslate-2.png)

Add your API Key and API Host obtained from d.run:

- **API Key**: Enter your API Key
- **API Host**:
  - For MaaS: Use `https://chat.d.run`
  - For independently deployed model services, refer to the model instance details, typically `https://<region>.d.run`
- **Custom Model**: Specify as `public/deepseek-r1`

![Bob Translate](../images/bobtranslate-3.png)

## Demo of Bob Translate Usage

![Bob Translate](../images/bobtranslate-4.png)