---
hide:
  - toc
---

# Release Notes - 20250122

| Module | Features | Documentation |
| ------ | -------- | ------------- |
| Login & Registration | - Supports phone number registration via SMS verification<br>- Supports login with username/email and password, or phone number and SMS verification<br>- Allows password recovery via phone number and SMS verification | [Register Account](./index.md) |
| Compute Marketplace | Access the compute marketplace to quickly select and purchase a variety of GPU resources | [Learn About the Compute Marketplace](./zestu/index.md) |
| Container Instances | - Manage the lifecycle of container instances (create/delete/start/stop)<br>- Choose to install Jupyter during container creation for quick access via Jupyter<br>- Choose to install VS Code during container creation for quick access via VS Code<br>- Mount file storage when creating container instances<br>- SSH login with username/password for container access<br>- Passwordless SSH access via public key<br>- Pay-as-you-go billing for container instances<br>- Create instances using built-in images<br>- Expose container instance ports through the UI | [Create a Container Instance](./zestu/instance.md) |
| File Storage | - Initialize file storage in different regions<br>- 20GB of free file storage available per region<br>- Upload, download, and delete files easily through the UI | [Initialize File Storage](./zestu/storage.md) |
| Billing Center | - Recharge online via Alipay<br>- View current account balance<br>- Track transactions by date, including recharges, usage, and refunds<br>- View detailed order information, including status, payment time, and amount<br>- View billing records and costs for all created resources | [Wallet](./leopard/index.md) |
| Model Marketplace | - Display model list in a card view for easy browsing<br>- View detailed model information and API examples<br>- Quickly deploy and try out text models<br>- Search for models by name, provider, or type<br>- Explore multimodal models<br>- Try image-to-text models | [Model Marketplace](./models/index.md) |
| Model Services | - View a list of deployed model services<br>- Access a variety of models for quick deployment<br>- Scale model service instances up or down<br>- Pay-per-use billing for model services with clear cost visibility<br>- Deploy by region<br>- Configure instance count for horizontal scaling<br>- Experience deployed model services online<br>- Get API examples in multiple languages (e.g., cURL, Python, Node.js) for deployed models | [Model Services](./models/service.md) |
| Service Experience | - One-click experience feature for quickly testing service availability<br>- For text generation models, configure parameters like system prompt (set system instructions), temperature (control result randomness), and top_p (adjust probability distribution)<br>- Compare different models within the same type | [Experience Models](./models/index.md#_3) |
| API Key Management | - View the list of API Keys<br>- One-click to copy full API Key<br>- Delete a specified API Key (irreversible)<br>- Generate new API Keys with custom names | [Manage API Keys](./models/apikey.md) |
