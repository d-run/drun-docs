---
hide:
  - toc
---

# Release Notes

This page outlines key feature updates for **d.run** .

## 2025-05-30

### Compute Cloud v0.6.0

#### 🚀 New Features

* **[Container Instances]** Added monitoring support for domestic GPUs (Metax, Enflame, Biren).
* **[Container Instances]** Enabled container instances to use custom images.
* **[Container Instances]** Added a prompt for VRAM requirements of the image version when creating container instances.
* **[Container Registry]** Introduced a container registry module to support image lifecycle management.
* **[Container Registry]** Enabled manual saving of container instance images.
* **[Container Registry]** Added support for changing the container registry password.
* **[File Storage]** After 15 days of overdue payment, file storage will be automatically downsized to the free 20GB tier and users will be notified via SMS.
* **[Compute Cloud Admin View]** Added support for linking the `gateway protocol`, `networkSupported`, and `SERVICE_PROTOCOL` parameters—only one of these needs to be configured.

#### ⚡ Enhancements & Optimizations

* **[Container Instances]** Improved delay in container instance status display after shutdown and system disk saving.
* **[File Storage]** Reduced display delay after successful file storage scaling operations.

#### 🐛 Bug Fixes

* **[Container Instances]** Fixed an issue where data was lost when restarting a container instance after enabling scheduled shutdown and saving the system disk.
* **[Container Instances]** Fixed display issues on the welcome page.
* **[File Storage]** Fixed an issue where expansion orders were still generated after a failed expansion of Suoyuan (Enflame) file storage.

## 2025-05-06

### LLM Studio v0.5.0

- [Model Gallery] Added support for "Deep Thinking" in text models  
- [Model Gallery] Enabled message copying and regeneration for text models  
- [Model Gallery] Image-to-text models can now generate multiple images simultaneously  
- [Model Gallery] Image-to-text models now support custom positive/negative prompts and image sizes  
- [Served Models] Fully compatible with the standard OpenAI SDK  
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

- [Model Gallery] Card view for model list for better visualization  
- [Model Gallery] Detailed model descriptions and API call examples  
- [Model Gallery] Quick deployment and testing of text models  
- [Model Gallery] Search models by name, provider, and type  
- [Model Gallery] Try multimodal models  
- [Model Gallery] Try image-to-text models  
- [Served Models] View list of deployed model services  
- [Served Models] Variety of models available for deployment  
- [Served Models] Instance scaling support  
- [Served Models] Postpaid billing (pay-as-you-go) with cost transparency  
- [Served Models] Region selection supported for deployment  
- [Served Models] Configure number of instances for horizontal scaling  
- [Served Models] In-browser experience of deployed models  
- [Served Models] API examples in multiple languages (curl, Python, Node.js)  
- [Playground] One-click testing to quickly verify service availability  
- [Playground] Text generation models support parameters like `system prompt`, `temperature`, and `top_p`  
- [Playground] Compare different models of the same type  
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
