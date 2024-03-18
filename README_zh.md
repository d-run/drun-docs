# DaoCloud d.run 文档站

[English](./README.md) | 中文

d.run 是一个全方位的人工智能生成和增强平台，可以帮助您优化您的大语言模型，并利用您的知识库。
通过整合 AI 生成引擎和各种插件，比如云原生 AI 引擎 baize、DataTunerX、DaoCloud AIGC 知识库和 infmonkeys 等插件，
d.run 可以用来创建、训练和推断各种人工智能产品。这个 repo 包含了 d.run 网站和文档的源文件。

## 提交 PR

这个网站使用 Pull Request（PR）来修改、翻译和管理所有页面。

1. 点击 `Fork` 创建一个分支
2. 运行 `git clone` 将这个分支克隆到您的计算机上
3. 在本地编辑一个或多个页面并预览
4. 运行 git 命令，如 `git add`、`git commit` 和 `git push`，提交您的更改
5. 在这个仓库中打开一个 PR
6. 在审查后成功合并，谢谢。

## 本地预览

这部分描述了您如何在提交之前预览您的更改。

### 使用 Docker

1. 安装并运行 [Docker](https://www.docker.com/)。
2. 运行 `make serve` 并预览您的更改。

### 使用 Git 仓库

查看 [MkDocs 安装文档](https://squidfunk.github.io/mkdocs-material/getting-started/)。

1. 安装 Poetry 和 Python 3.9+
    1. 配置 Poetry：`poetry config virtualenvs.in-project true`
    2. 启用 venv：`poetry env use 3.9`
2. 安装依赖：`poetry install`
3. 在本地仓库文件夹中运行 `poetry run mkdocs serve -f mkdocs.yml`
4. 在 <http://0.0.0.0:8000/> 预览

## 命名规范

这部分列出了一些文件或文件夹名称的约定供您参考：

- **只包含** 英文小写字母和连字符 (`-`)
- **不要** 包含以下任何字符：
    - 中文字符
    - 空格
    - 特殊字符如 `*`、`?`、`\`、`/`、`:`、`#`、`%`、`~`、`{`、`}`
- 用连字符 (`-`) 连接单词
- 保持简短：最多 5 个英文单词，避免重复，使用缩写
- 描述性：易于理解并反映文档主题

| 不可用名称                        | 可用名称          | 原因                                      |
| ---------------------------------- | ---------------- | ---------------------------------------- |
| ConfigName                         | config-name      | 使用小写字母和连字符            |
| create secret                      | create-secret    | 名称中不要有空格 |
| quick-start-install-online-install | online-install   | 保持简短                               |
| c-ws                               | create-workspace | 描述性                           |
| update_image                       | update-image     | 用连字符连接单词               |

## 写作提示

- 项目符号缩进 4 个空格
- 在中英文字符之间留一个空格
- 在段落、图片、标题或列表之前后留一行空白
- 在标题结尾不添加任何标点符号
- 注意链接，避免任何空链接或失效链接
- 提供一致的体验，探索本页面中的所有页面

## 感谢所有贡献者 ❤

<a href="https://github.com/ray-knowledge/drun-doc/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ray-knowledge/drun-doc" />
</a>
