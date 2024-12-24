import os
import re

# 图片目录
image_dir = 'docs/zh/docs/dmc/images'  # 确保路径正确
# Markdown 文件目录
markdown_dir = 'docs/zh/docs/dmc'

# 收集所有图片文件
images = {f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))}

# 收集在 Markdown 文件中引用的图片
referenced_images = set()

# 使用 os.walk 遍历 Markdown 文件目录及其所有子文件夹
for root, _, files in os.walk(markdown_dir):
    for file in files:
        if file.endswith('.md'):
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                content = f.read()
                # 使用正则表达式查找所有可能的图片引用
                # 修改正则表达式以匹配 "../images/" 前缀
                matches = re.findall(r'!\[.*?\]\(\.\./images/(.*?\.(?:jpg|png))\)', content)
                # 提取文件名部分并添加到 referenced_images
                referenced_images.update(matches)

# 找到未被引用的图片
unused_images = images - referenced_images

print("未被引用的图片文件:", unused_images)
