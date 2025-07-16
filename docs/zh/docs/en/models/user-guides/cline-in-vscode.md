---
translated: true
---

# Using d.run in VSCode and Cline

[Cline](https://cline.bot/) is a VSCode plugin that enables you to use d.run model services within VSCode.

## Installing Cline

Search for and install the Cline plugin in VSCode.

![Cline](../images/cline-in-vscode.png)

You can also download and use RooCode, which is a branch of Cline.

> Note: Cline was originally known as Claude Dev. RooCode (RooCline) is based on this branch.

If you're unable to directly download the plugin due to network restrictions, consider downloading the `.vsix` file from the VSCode Extension Marketplace and installing it via `Install from VSIX`.

- [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
- [RooCode](https://marketplace.visualstudio.com/items?itemName=RooVeterinaryInc.roo-cline): A branch of Cline

## Configuring Cline

Open the Cline configuration page:

![Cline](../images/cline-in-vscode-2.png)

- **API Provider**: Select "OpenAI Compatible"
- **Base URL**: Enter `https://chat.d.run/v1`
- **API Key**: Input your API key
- **Model ID**: Enter your model ID
    - Obtainable from d.run's Model Square, with MaaS models prefixed as public/deeepseek-r1
    - For independently deployed models, retrieve it from the model service list

![Cline](../images/cline-in-vscode-3.png)

## Cline Usage Demo

![Cline](../images/cline-in-vscode-4.png)