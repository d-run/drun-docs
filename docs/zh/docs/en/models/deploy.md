---
hide:
  - toc
---

# Model Deployment

You can deploy models from the **Model Store** or **Model Services**. The parameters are explained as follows:

- Select the model to deploy (e.g., Qwen2-0.5B-Instruct), ensuring the chosen model meets your business needs and task scenarios.
- Model service name must meet the following requirements:
    - Length limit: 2-64 characters
    - Character limit: Only lowercase letters, numbers, and hyphens (-) are supported, and it must start and end with a lowercase letter or number.
    - Example: text-gen-service or model-01
- Region
    - Select the region for service deployment (e.g., "Shanghai Area 2").
    - The region selection should be based on business coverage and latency requirements.
- Number of instances
    - Configure the number of instances to deploy. Default value: 1
    - Instance explanation: The more instances, the stronger the service's concurrency capability, but costs will increase accordingly.
- Billing method. d.run offers two billing modes:

    1. Pay-as-you-go:
        - Real-time billing based on usage, suitable for short-term use or dynamic demand users.
        - Cost formula: Number of instances × hourly cost.
        - Example: 1 instance × 3 Yuan/hour = 3 Yuan/hour.

    2. Annual or monthly subscription (not currently supported):
        - Purchase service instances in advance at a relatively discounted price, suitable for long-term users.
        - After choosing this mode, the system will prompt the corresponding annual or monthly fee.

- View configuration costs:
    - The bottom of the page will automatically display the calculation formula for configuration costs and the estimated costs.
    - Example:
        - Configuration cost: 3 Yuan/hour
        - Calculation formula: 1 (number of instances) × 3 Yuan/hour.
