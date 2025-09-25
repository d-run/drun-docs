# 配置 SSH 公钥

本文说明如何配置 SSH 公钥。

<a id="check-ssh"></a>

## 查看已存在的 SSH 公钥

在生成新的 SSH 公钥前，请先确认是否需要使用本地已生成的 SSH 公钥，SSH 公钥对一般存放在本地用户的根目录下。
Linux、Mac 请直接使用以下命令查看已存在的公钥，Windows 用户在 WSL（需要 Windows 10 或以上）或 Git Bash 下使用以下命令查看已生成的公钥。

- **ED25519 算法：**

    ```bash
    cat ~/.ssh/id_ed25519.pub
    ```

- **RSA 算法：**

    ```bash
    cat ~/.ssh/id_rsa.pub
    ```

如果返回一长串以 ssh-ed25519 或 ssh-rsa 开头的字符串，说明已存在本地公钥，
您无需[生成 SSH 公钥](#generate-ssh)，直接[拷贝 SSH 公钥](#copy-ssh)。

<a id="generate-ssh"></a>

## 生成 SSH 公钥

若[查看已存在的 SSH 公钥](#check-ssh)时未返回指定的内容字符串，表示本地暂无可用 SSH 公钥，需要生成新的 SSH 公钥，请按如下步骤操作：

1. 访问终端（Windows 请使用 [WSL](https://docs.microsoft.com/zh-cn/windows/wsl/install)
   或 [Git Bash](https://gitforwindows.org/)），运行 `ssh-keygen -t`。
  
2. 输入密钥算法类型和可选的注释。
  
    注释会出现在 .pub 文件中，一般可使用邮箱作为注释内容。
    
    - 基于 `ED25519` 算法，生成密钥对命令如下：
    
        ```bash
        ssh-keygen -t ed25519 -C "<注释内容>"
        ```
    
    - 基于 `RSA` 算法，生成密钥对命令如下：
    
        ```bash
        ssh-keygen -t rsa -C "<注释内容>"
        ```

3. 点击回车，选择 SSH 公钥生成路径。

    以 ED25519 算法为例，默认路径如下：

    ```console
    Generating public/private ed25519 key pair.
    Enter file in which to save the key (/home/user/.ssh/id_ed25519):
    ```

    密钥默认生成路径：`/home/user/.ssh/id_ed25519`，公钥与之对应为：`/home/user/.ssh/id_ed25519.pub`。

4. 设置一个密钥口令。

    ```console
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    ```

    口令默认为空，您可以选择使用口令保护私钥文件。
    如果您不想在每次使用 SSH 协议访问仓库时，都要输入用于保护私钥文件的口令，可以在创建密钥时，输入空口令。

5. 点击回车，完成密钥对的创建。

<a id="copy-ssh"></a>

## 拷贝公钥

除了在命令行打印出已生成的公钥信息手动复制外，可以使用命令拷贝公钥到粘贴板下，请参考操作系统使用以下命令进行拷贝。

- Windows（在 [WSL](https://docs.microsoft.com/en-us/windows/wsl/install)
  或 [Git Bash](https://gitforwindows.org/) 下）：

    ```bash
    cat ~/.ssh/id_ed25519.pub | clip
    ```

- Mac：

    ```bash
    tr -d '\n'< ~/.ssh/id_ed25519.pub | pbcopy
    ```

- GNU/Linux（需要 xclip）：

    ```bash
    xclip -sel clip < ~/.ssh/id_ed25519.pub
    ```

<a id="add-ssh"></a>

## 添加公钥

1. 登录 UI 页面，在页面右上角选择 **个人中心** -> **SSH 公钥** -> **导入 SSH 公钥**

    ![导入 SSH 公钥](./images/import-ssh.png)

2. 添加生成的 SSH 公钥信息。
  
    - 名称
    - SSH 公钥内容
    - 有效期：永久、自定义
