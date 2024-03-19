---
hide:
  - toc
  - navigation
---

# d.run 让算力更自由

!!! tip

    d.run 整合云原生能力，兼容和微调各类大模型，以知识库为入口构建智能应用体系!

d.run 是 DaoCloud 自研的 AIGC 综合性算力运营平台，包含以下模块：

- [智能应用](./dak/intro/index.md)：由 DaoCloud Knowledge 知识库承载，负责大模型场景的应用落地。
- [模型中心](./dmc/intro/index.md)：这是管理各种流行大模型的门户，您可以在这里添加、创建、部署本地和在线模型。
- [模型开发](./baize/intro/index.md)：由 DCE 5.0 中的[智能算力](https://docs.daocloud.io/baize/intro/index.html)模块来承载，负责模型开发的相关业务。
- [模型微调](./dtx/intro/index.md)：由 [DataTunerX](https://github.com/DataTunerX/datatunerx) 承载，负责大模型数据的微调业务。
- 算力容器：由 DCE 5.0 中的[容器管理](https://docs.daocloud.io/kpanda/intro/index.html)承载，负责算力底座的接入，管理 GPU、CPU、内存等算力资源，智能化调度 Pod、Job 等工作负载。
- 全局管理：由 DCE 5.0 中的[全局管理](https://docs.daocloud.io/ghippo/intro/index.html)承载，负责用户访问控制、权限管理、审计日志以及 d.run 个性化设置等。

![login](./images/drun-login.jpg)

**d.run 的整体架构规划如下：**

![architecture](./images/architecture.png)
