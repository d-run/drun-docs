---
hide:
  - toc
---

# Release Notes

This page outlines key feature updates for d.run.

## 2025-10-30

### Billing Center v0.10.0

#### 🚀 New Features

- **[Wallet]** Supports balance alerts. Users can set a threshold balance and receive notifications when available cash drops below this value.
- **[Quota Management]** Supports cost quotas for sub-accounts, allowing limitation of maximum spendable amounts; supports top-up/deduction for sub-accounts; supports restricting and shutting down services when the quota is exhausted.
- **[Quota Management]** Supports topping up or deducting quota amounts for sub-accounts to adjust available balances.
- **[Quota Management]** Supports controlling whether services should be restricted or shut down when the quota is exhausted.

## 2025-09-29

### Compute Cloud v0.11.0

#### 🚀 New Features

- **[Compute Marketplace]** Supports viewing sub-account lists and resources.
- **[Image Registry]** Added new alert rules for saving images.

#### 🐛 Bug Fixes

- **[Container Instance]** Fixed an issue where inventory was not released after yearly/monthly prepaid instances were automatically shut down upon expiration.
- **[Container Instance]** Supports cardless boot mode (unified configuration, free of charge).
- **[File Storage]** File storage now supports scaling up and down.

### Billing Center v0.9.0

#### 🚀 New Features

- **[Transaction Details]** Supports viewing sub-account consumption records.
- **[Transaction Details]** Supports exporting transaction detail reports.
- **[Order Management]** Supports exporting order record reports.
- **[Bill Management]** Supports exporting billing record reports.
- **[Bill Management]** Supports exporting monthly bill reports.

#### 🐛 Bug Fixes

- **[Bill Management]** Monthly billing timezone changed to UTC+8.

### Large Model Service Platform (WS Mode – Private Cloud) v0.10.0

#### 🚀 New Features

- Supports viewing audit logs.

## 2025-08-30

### Compute Cloud v0.10.0

#### 🚀 New Features

- **[Container Instance]** Supports saving system disks when shutting down an instance.
- **[Container Instance]** Supports manually specifying image addresses during instance creation.
- **[Container Instance]** Clearer SSH passwordless login guidance.
- **[Container Instance]** Supports viewing image descriptions when selecting images, helping users understand which ports the image exposes by default.
- **[Container Instance]** Supports sorting GPU type, VRAM, and quantity when selecting resources to quickly find suitable specifications.
- **[Container Instance]** Supports searching instances by ID.
- **[Access Management]** Supports exposing ports via HTTPS.
- **[Container Instance]** Supports domestic GPUs: Iluvatar (燧原).
- **[Container Instance]** Supports domestic GPUs: Biren (壁仞).
- **[Container Instance]** SSH welcome message language follows the user's language settings in the personal center.
- **[Compute Marketplace]** Supports purchasing yearly/monthly prepaid instances and displaying discounts.

### Personal Center v0.7.0

#### 🚀 New Features

- **[Sub-Account Management]** Supports managing sub-accounts.

## 2025-07-30

### Compute Cloud v0.8.0

#### 🚀 New Features

- **[Container Instance]** Supports purchasing container instances using yearly/monthly prepaid plans.
- **[Container Instance]** Supports lifecycle management (create/delete/start/stop) for prepaid instances.
- **[Container Instance]** Supports expiration reminders for prepaid instances.
- **[Container Instance]** Supports adding custom startup commands.
- **[Container Instance]** Supports mounting data disks.
- **[Container Instance]** Adds event display during instance startup.
- **[File Storage]** Supports folder display.

#### ⚡ Enhancements

- **[Compute Cloud]** Improved compute cloud audit log event entries.
- **[Compute Cloud]** Improved Zestu alert rules.
- **[Container Instance]** Improved event display for abnormal runtime states.
- **[Image Registry]** Improved image name display.
- **[Image Registry]** Improved error messages for failed system disk save attempts during shutdown.

#### 🐛 Bug Fixes

- **[Compute Cloud]** Fixed missing CPU and memory info for existing container instances after upgrade.
- **[Compute Cloud]** Fixed issue where modifying image registry info in admin caused image save failures.

### Large Model Service Platform (WS Mode – Private Cloud) v0.8

#### 🚀 New Features

- **[Admin Console]** Model list display.
- **[Admin Console]** Supports batch importing models from URLs.
- **[Admin Console]** Supports creating models.
- **[Admin Console]** MaaS model list display.
- **[Admin Console]** Supports adding MaaS models.
- **[Admin Console]** Supports adding multiple upstream endpoint configurations.
- **[Admin Console]** Supports rate limiting per API key.
- **[Admin Console]** Supports rate limiting per workspace.
- **[Admin Console]** Supports adding multiple rate-limit rules.
- **[Admin Console]** Supports load balancing (round-robin).
- **[Admin Console]** Model deployment list display.
- **[Admin Console]** Supports adding multiple model configuration sets.
- **[Admin Console]** Supports vLLM model deployment.

## 2025-06-29

### Compute Cloud v0.7.0

#### 🚀 New Features

* [Container Instance] Support remounting file mount paths when changing configurations
* [Compute Cloud] Integrated with audit logging
* [Compute Cloud] Support retrieving operational metrics such as GPU utilization and memory usage for all GPUs under a container
* [Container Registry] Added duplicate username check for container registry accounts

#### ⚡ Enhancements & Optimizations

* [Container Instance] Improved delay in status display after shutting down and saving the system disk
* [Container Instance] Optimized disk limits for container instances
* [Container Instance] Improved image save prompts for scheduled or manual shutdowns
* [File Storage] Enhanced status display during file storage initialization

#### 🐛 Bug Fixes

* [Container Instance] Fixed issues when accessing Muxi container instances via JupyterLab, including terminal errors and missing GPU model info
* [Container Instance] Fixed failure to start container instances created with custom image files
* [File Storage] Fixed partial failures when uploading multiple files
* [Container Registry] Fixed issue of two image versions appearing when manually shutting down and saving a system disk for the first time
* [Container Registry] Fixed failure to save images when a container instance is shut down due to overdue payments

## 2025-05-30

### Compute Cloud v0.6.0

#### 🚀 New Features

* [Container Instances] Added monitoring support for domestic GPUs (Metax, Enflame, Biren).
* [Container Instances] Enabled container instances to use custom images.
* [Container Instances] Added a prompt for VRAM requirements of the image version when creating container instances.
* [Container Registry] Introduced a container registry module to support image lifecycle management.
* [Container Registry] Enabled manual saving of container instance images.
* [Container Registry] Added support for changing the container registry password.
* [File Storage] After 15 days of overdue payment, file storage will be automatically downsized to the free 20GB tier and users will be notified via SMS.
* [Compute Cloud Admin View] Added support for linking the `gateway protocol`, `networkSupported`, and `SERVICE_PROTOCOL` parameters—only one of these needs to be configured.

#### ⚡ Enhancements & Optimizations

* [Container Instances] Improved delay in container instance status display after shutdown and system disk saving.
* [File Storage] Reduced display delay after successful file storage scaling operations.

#### 🐛 Bug Fixes

* [Container Instances] Fixed an issue where data was lost when restarting a container instance after enabling scheduled shutdown and saving the system disk.
* [Container Instances] Fixed display issues on the welcome page.
* [File Storage] Fixed an issue where expansion orders were still generated after a failed expansion of Suoyuan (Enflame) file storage.

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
