# Quick Start

This guide will help you quickly create and use an OpenClaw instance.

## Prerequisites

- A d.run platform account  
- Completed real-name verification  
- Sufficient account balance or vouchers  

## Create an OpenClaw Instance

1. Select the **ClawOS** module and click the **Create** button on the right.

2. Set an English **Name** for the OpenClaw instance and click **Confirm** in the lower-right corner.

3. (Optional) d.run OpenClaw supports seamless Feishu integration. When creating an instance, enable **Integrate Feishu** and enter the Feishu configuration information.

> For details on how to obtain the Feishu configuration and complete the integration, refer to the [Feishu Integration](./feishu-integration.md) document.

4. Wait for the instance creation to complete.

## Access OpenClaw

When the instance status shows **Running**:

1. Click **Access Tools → OpenClaw** on the right
2. Open the OpenClaw management page

!!! note

    Due to network conditions, it may take 1–2 minutes before the page becomes accessible.

## Start Using OpenClaw

Click **Proceed to the website** and start chatting in the conversation window.

## Debug OpenClaw in the Backend

d.run provides multiple ways to operate the backend. You can access it via **SSH** or **JupyterLab** in the web interface.

=== "Method 1: SSH Login"

    Use SSH to directly enter the OpenClaw secure sandbox.

=== "Method 2: Web Access"

    Access the backend through the web interface.

### Command Line Operations

Before operating the OpenClaw CLI, switch to the `node` user:

```bash
su node  # switch to the node user
````

View installed skills:

```bash
openclaw skills list
```

## OpenClaw FAQ

See the [FAQ](./faq.md) document.
