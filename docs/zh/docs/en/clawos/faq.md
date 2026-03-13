# FAQs

## Will OpenClaw lose its memory if an instance has issues?

**No**

Whether you restart OpenClaw, pause the instance (feature coming soon), or release the instance, the memory will not be lost.

This is because all data in `~/.openclaw` is persistently stored in the d.run storage system.

## Is my OpenClaw secure?

**Yes**

DaoCloud’s ClawOS is an enterprise-grade “lobster farming platform” designed for security:

- Uses container technology as the security sandbox for each OpenClaw instance  
- Based on Kubernetes to ensure data security across compute, network, and storage layers  
- Data and conversations are powered by the d.run large-model service platform, ensuring sensitive data protection  

## Can I upload files for OpenClaw to analyze?

**Of course**

You can do this in the following ways:

1. Send files to OpenClaw through Feishu chat for processing  
2. Upload and manage files through the d.run file management interface  

![Upload File](./images/upload-file.png)

## OpenClaw instance creation failed

Please confirm:

1. Real-name verification has been completed  
2. Your account balance is greater than the price of the selected resources  

## Feishu integration not working

A single Feishu application can only be connected to **one OpenClaw instance** at a time.

If you have multiple OpenClaw instances, each instance must use a **separate App ID and App Secret** .
