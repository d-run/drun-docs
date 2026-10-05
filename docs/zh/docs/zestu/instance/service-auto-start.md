# 容器实例内服务开机自启

在每一个算力云的容器实例中，都有一个 s6 守护进程，他会在开机时，将指定的服务自动拉起。
如果用户需要开启自启服务，只需要向 s6 中注册自己的自定义服务。

## 前提条件

- 登录 [d.run 账号](../../index.md)
- 已通过算力云[创建容器实例](../instance.md)，且容器实例状态为 **运行中**

## 注册自定义服务

在 `/etc/s6/` 目录下创建一个目录 <Your_service_name>，然后在这个目录下创建一个固定名称 `run` 的 Bash 脚本. 然后在 `run` 文件中填写服务启动命令。

`run` 必须具有执行权限。启动命令应通过 `exec` 在前台运行服务，避免服务进入后台后，s6 无法跟踪服务进程并反复重启。

!!! note
  
    注册自定义镜像后，需要关机保存镜像，这样才能将配置进行持久化。下次开机后，注册的自定义服务就会自动的启动了。

示例一：以 Nginx 举例

先确认实例已安装 Nginx。对于 Debian/Ubuntu 镜像，可以在实例终端中安装：

```bash
apt-get update && apt-get install -y nginx
```

如果 Nginx 已在后台运行，先执行 `nginx -s quit` 停止它，再交给 s6 启动。

```bash
mkdir -p /etc/s6/nginx    # 注册自定义服务
cat <<'EOF' > /etc/s6/nginx/run  # 注册自定义服务的启动脚本
#!/bin/bash

echo "Starting Nginx..."

exec nginx -g 'daemon off;'    # 在前台启动 nginx
EOF
chmod +x /etc/s6/nginx/run
```

示例二：以 Python HTTP 服务举例

此示例需要已安装 Python 3，使用其内置 HTTP 服务提供 `/root/data` 目录中的文件，无需额外创建 Python 脚本。

```bash
mkdir -p /root/data
mkdir -p /etc/s6/python_http    # 注册自定义服务
cat <<'EOF' > /etc/s6/python_http/run  # 注册自定义服务的启动脚本
#!/bin/bash

echo "Starting python http..."

exec python3 -m http.server 8000 --directory /root/data
EOF
chmod +x /etc/s6/python_http/run
```

保存镜像并重新启动实例后，在实例终端中运行 `curl http://127.0.0.1:8000/`，确认 Python HTTP 服务已启动。
