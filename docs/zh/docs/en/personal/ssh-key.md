# Configure SSH Public Key

This guide explains how to configure an SSH public key.

<a id="check-ssh"></a>

## Check for an Existing SSH Public Key

Before generating a new SSH key, check whether you already have one. SSH key pairs are usually stored in the user's home directory.  
On Linux and macOS, use the following commands to check for an existing public key.  
On Windows, use these commands in WSL (requires Windows 10 or above) or Git Bash.

- **ED25519 algorithm:**

    ```bash
    cat ~/.ssh/id_ed25519.pub
    ```

- **RSA algorithm:**

    ```bash
    cat ~/.ssh/id_rsa.pub
    ```

If a long string beginning with `ssh-ed25519` or `ssh-rsa` is returned, it means a local public key already exists.  
You can skip to [Copy SSH Public Key](#copy-ssh) without generating a new one.

<a id="generate-ssh"></a>

## Generate a New SSH Public Key

If no key was found in [Check for an Existing SSH Public Key](#check-ssh), follow the steps below to generate a new one:

1. Open a terminal (on Windows, use [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) or [Git Bash](https://gitforwindows.org/)), and run `ssh-keygen -t`.

2. Enter the desired key type and an optional comment.  
   The comment appears in the `.pub` file, and it's common to use an email address.

    - To generate a key pair with the `ED25519` algorithm:

        ```bash
        ssh-keygen -t ed25519 -C "<comment>"
        ```

    - To generate a key pair with the `RSA` algorithm:

        ```bash
        ssh-keygen -t rsa -C "<comment>"
        ```

3. Press Enter to choose the file path where the key will be saved.

    For ED25519, the default path looks like this:

    ```console
    Generating public/private ed25519 key pair.
    Enter file in which to save the key (/home/user/.ssh/id_ed25519):
    ```

    Default private key path: `/home/user/.ssh/id_ed25519`  
    Corresponding public key: `/home/user/.ssh/id_ed25519.pub`

4. Set a passphrase:

    ```console
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    ```

    You can choose to leave it empty.  
    If you don’t want to be prompted for a passphrase each time you access a repository over SSH, enter nothing and press Enter.

5. Press Enter to complete the key pair creation.

<a id="copy-ssh"></a>

## Copy Your Public Key

In addition to manually copying the public key from the terminal output, you can use the following commands to copy the public key to your clipboard, depending on your operating system:

- **Windows** (in [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) or [Git Bash](https://gitforwindows.org/)):

    ```bash
    cat ~/.ssh/id_ed25519.pub | clip
    ```

- **macOS** :

    ```bash
    tr -d '\n' < ~/.ssh/id_ed25519.pub | pbcopy
    ```

- **GNU/Linux** (requires `xclip`):

    ```bash
    xclip -sel clip < ~/.ssh/id_ed25519.pub
    ```

<a id="add-ssh"></a>

## Add Your Public Key

1. Log in to the web UI, then navigate to **Personal Center** -> **SSH Public Key** -> **Import SSH Public Key**



2. Add your generated SSH public key details:

    - **Name**
    - **SSH Public Key Content**
    - **Validity Period** : Permanent or Custom
