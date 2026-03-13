# OpenClaw Agent: From “Can Chat” to “Can Get Work Done”

## What Is OpenClaw

**OpenClaw** is a next-generation open-source AI agent runtime that represents a major leap in AI capability. Instead of merely answering questions passively, it can actively plan tasks, call tools, and execute actions autonomously—completing complex end-to-end work like a real digital employee.

| Capability Dimension | Traditional AI Assistant | OpenClaw Agent |
|---|---|---|
| Interaction Mode | Passive Q&A, single response | Active planning, multi-step autonomous execution |
| Capability Boundary | Text output only | Tool usage, OS operations, code execution |
| Applicable Scenarios | Information lookup, simple generation | End-to-end automated workflows |

**OpenClaw** provides five native capability layers:

- **User Access Layer:** Supports chat conversations, CLI command line, IDE plugins, IM tools such as Feishu / WeChat / DingTalk, and Web APIs  
- **Agent Core Engine:** Task planning, context management, workflow engine, sub-agent orchestration, multi-agent architecture  
- **Tool Execution Layer:** File system access, terminal commands, browser control, API calls, custom skills, and third-party tool integration  
- **Memory & Knowledge Layer:** Short-term session memory, long-term vector storage, knowledge base retrieval, cross-session context persistence  
- **Model Integration Layer:** Compatible with Claude, GPT, local open-source models, enterprise private models, and the OpenAI API protocol  

## Using OpenClaw on d.run

**ClawOS v0.1** is now available on **d.run**, providing an enterprise-grade hosted runtime platform for OpenClaw. There is no need to configure environments or manually connect models. Your AI digital employee can be ready to work within **five minutes**.

For detailed instructions, see the [Quick Start](./quickstart.md) guide.

### Feishu Integration

**ClawOS v0.1** natively supports seamless **Feishu** integration. When creating an instance, simply enable the **Integrate Feishu** option and provide your Feishu application's **App ID** and **App Secret**.

Once configured, OpenClaw can directly send and receive messages, process files, and reply in group chats within Feishu—without switching interfaces.

For detailed setup instructions, see the [Feishu Integration](./feishu-integration.md) guide.

## Typical Use Cases

### HR Resume Screening at Scale

When facing dozens of PDF resumes with different formats, OpenClaw can automatically read them, extract key technical skills, score and rank candidates based on job requirements, and output a structured evaluation report. What previously took half a day can now be completed in minutes.

!!! note

    Resumes contain sensitive personal information (PII). A private deployment of d.run ensures that data never leaves the internal network and prevents resumes from being sent to external public cloud APIs.

### Software Development Assistant

After connecting to GitHub and configuring a multi-agent architecture (Main Agent + Research + Reviewer + Codex), OpenClaw can dive into source code repositories to find bugs, submit pull requests, enforce CI rules, and create a fully personalized automated development orchestrator.

### Batch Document Review

Encapsulate a full workflow—**read documents → extract key data → validate rules → generate approval feedback**—into a custom Skill using `createSkill`. Next time, you can process dozens of quarterly reports in bulk and export a summarized CSV with a single click, eliminating repetitive work.

## Product Advantages

| Advantage | Description |
| --- | --- |
| One-click activation, ready to use | Administrators do not need to manually configure environments, connect models, or set permissions. The system automatically creates sandboxes and injects tokens, allowing business users to start immediately without IT involvement. |
| Secure sandbox isolation | Each OpenClaw instance runs independently in a containerized security sandbox using DaoCloud’s proprietary **zestU** kernel-level isolation technology. Even if an instance is compromised or fails, the impact remains strictly contained within the sandbox and cannot penetrate the internal network or modify host files. |
| Persistent data, memory never lost | The entire `~/.openclaw` directory is persistently stored in the d.run storage system. Whether OpenClaw is restarted, paused, or the instance is released, conversation history, configurations, and memory remain intact. |
| Secure and controllable model access | All model calls go through the d.run AI gateway and security policies instead of directly connecting to the public internet. Your data and conversations are processed entirely within the d.run platform’s model services, ensuring protection of sensitive information. |
| Fully accessible backend | d.run provides two ways to access the OpenClaw backend: [SSH login and JupyterLab](quickstart.md#_4). Both support full CLI operations for advanced users who need debugging or customization capabilities. |

## Features

| Feature | Current Status |
|---|---|
| [One-click OpenClaw instance creation](./quickstart.md#openclaw) | Available |
| [Seamless Feishu integration](./feishu-integration.md) | Available |
| Secure container sandbox isolation | Available |
| Persistent data storage | Available |
| [SSH / JupyterLab backend access](./quickstart.md#__tabbed_1_1) | Available |
| File management and uploads | Available |
| Token usage analytics and cost control | Coming soon |
| More large-model support | Coming soon |
| Unified instance management (admin view) | Planned |
| Audit tracking and operation replay | Planned |
