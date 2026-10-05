# Auto-Start Services in Container Instances

Each container instance in Compute Cloud includes an **s6 supervisor daemon** that automatically starts designated services at boot time.  
To enable auto-start for your custom service, simply register it with **s6**.

## Prerequisites

- Logged in to your d.run account  
- A container instance has been [created via Compute Cloud](../instance.md), and its status is **Running**

## Register a Custom Service

Create a directory under `/etc/s6/` with the name of your service, and inside it, create a Bash script named `run`.  
Place the service startup command inside the `run` script.

The `run` script must be executable. Use `exec` to run the service in the foreground so s6 can track its process. A service that daemonizes can cause s6 to repeatedly restart it.

!!! note

    After registering a custom service, you must **shut down and save** the container image.  
    This ensures the configuration is persisted and the service will auto-start on the next boot.

### Example 1: Auto-start Nginx

Make sure Nginx is installed in the instance. For Debian/Ubuntu images, install it from the instance terminal:

```bash
apt-get update && apt-get install -y nginx
```

If Nginx is already running in the background, stop it with `nginx -s quit` before letting s6 start it.

```bash
mkdir -p /etc/s6/nginx  # Register a custom service
cat <<'EOF' > /etc/s6/nginx/run  # Create the service start script
#!/bin/bash

echo "Starting Nginx..."

exec nginx -g 'daemon off;'  # Start nginx in the foreground
EOF
chmod +x /etc/s6/nginx/run
```

### Example 2: Auto-start a Python HTTP Service

This example requires Python 3. It uses Python's built-in HTTP server to serve files from `/root/data`, without an additional Python script.

```bash
mkdir -p /root/data
mkdir -p /etc/s6/python_http  # Register a custom service
cat <<'EOF' > /etc/s6/python_http/run  # Create the service start script
#!/bin/bash

echo "Starting python http..."

exec python3 -m http.server 8000 --directory /root/data
EOF
chmod +x /etc/s6/python_http/run
```

After saving the image and restarting the instance, run `curl http://127.0.0.1:8000/` in the instance terminal to confirm that the Python HTTP service has started.
