---
hide:
  - toc
---

# Release Notes

This page outlines key feature updates for **d.run** .

## 2025-05-06

### LLM Studio v0.5.0

- [Model Store] Added support for "Deep Thinking" in text models  
- [Model Store] Enabled message copying and regeneration for text models  
- [Model Store] Image-to-text models can now generate multiple images simultaneously  
- [Model Store] Image-to-text models now support custom positive/negative prompts and image sizes  
- [Model Service] Fully compatible with the standard OpenAI SDK  
- [API Keys] Usage statistics can now be filtered by API key, model type, and invocation time  
- [API Keys] Quickly view total calls, total input tokens, and total output tokens  
- [API Keys] Compare usage across different models  

## 2025-01-22

### Compute Cloud v0.1.0

- [Compute Market] Quickly purchase various types of GPU resources from the marketplace  
- [Container Instance] Lifecycle management (create/delete/start/stop) supported  
- [Container Instance] Optional Jupyter installation during creation, with quick access via Jupyter  
- [Container Instance] Optional VSCode installation during creation, with quick access via VSCode  
- [Container Instance] Support mounting file storage when creating instances  
- [Container Instance] Login and access via SSH with username and password  
- [Container Instance] Password-free SSH login via public key supported  
- [Container Instance] Pay-as-you-go billing available for container instances  
- [Container Instance] Create instances using built-in images  
- [Container Instance] Open instance ports via UI  
- [File Storage] Initialize file storage in different regions  
- [File Storage] Each region provides 20GB of free storage  
- [File Storage] Upload, download, and delete files via the UI  

### LLM Studio v0.1.0

- [Model Store] Card view for model list for better visualization  
- [Model Store] Detailed model descriptions and API call examples  
- [Model Store] Quick deployment and testing of text models  
- [Model Store] Search models by name, provider, and type  
- [Model Store] Try multimodal models  
- [Model Store] Try image-to-text models  
- [Model Service] View list of deployed model services  
- [Model Service] Variety of models available for deployment  
- [Model Service] Instance scaling support  
- [Model Service] Postpaid billing (pay-as-you-go) with cost transparency  
- [Model Service] Region selection supported for deployment  
- [Model Service] Configure number of instances for horizontal scaling  
- [Model Service] In-browser experience of deployed models  
- [Model Service] API examples in multiple languages (curl, Python, Node.js)  
- [Use Model] One-click testing to quickly verify service availability  
- [Use Model] Text generation models support parameters like `system prompt`, `temperature`, and `top_p`  
- [Use Model] Compare different models of the same type  
- [API Keys] View API key list  
- [API Keys] One-click copy of full API key  
- [API Keys] Delete specific keys (irreversible)  
- [API Keys] Generate new API keys with custom names  

### Billing Center v0.1.0

- [Wallet] Recharge with Alipay  
- [Wallet] View current cash balance  
- [Orders] View all account transactions (recharge, consumption, refunds) on a timeline  
- [Orders] View order details including status, time, and amount  
- [Bills] View charges and billing records for all created resources  

### Personal Center v0.1.0

- Login/Registration – Sign up using mobile number and verification code  
- Login/Registration – Login with either username/email + password or phone + code  
- Password Recovery – Reset password using mobile number and verification code  
