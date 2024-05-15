---
hide:
  - toc
---

# JuiceFS

JuiceFS 是一款面向云原生设计的高性能分布式文件系统，在 Apache 2.0 开源协议下发布，有社区版和商业版之分。
提供完备的 POSIX 兼容性，可将几乎所有对象存储接入本地作为海量本地磁盘使用，亦可同时在跨平台、跨地区的不同主机上挂载读写。

JuiceFS 采用「数据」与「元数据」分离存储的架构，从而实现文件系统的分布式设计。
文件数据本身会被切分保存在对象存储（例如 Amazon S3），而元数据则可以保存在 Redis、MySQL、TiKV、SQLite 等多种数据库中，你可以根据场景与性能要求进行选择。

JuiceFS 提供了丰富的 API，适用于各种形式数据的管理、分析、归档、备份，可以在不修改代码的前提下无缝对接大数据、机器学习、人工智能等应用平台，
为其提供海量、弹性、低价的高性能存储。运维人员不用再为可用性、灾难恢复、监控、扩容等工作烦恼，专注于业务开发，提升研发效率。同时运维细节的简化，对 DevOps 极其友好。

<div className="video-container">
  <iframe src="//player.bilibili.com/player.html?aid=931107196&bvid=BV1HK4y197va&cid=350876578&page=1&autoplay=0" width="100%" height="360" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>
</div>

## 应用场景

JuiceFS 为海量数据存储设计，可以作为很多分布式文件系统和网络文件系统的替代，特别是以下场景：

- **大数据分析**：HDFS 兼容；与主流计算引擎（Spark、Presto、Hive 等）无缝衔接；无限扩展的存储空间；运维成本几乎为 0；性能远好于直接对接对象存储。
- **机器学习**：POSIX 兼容，可以支持所有机器学习、深度学习框架；方便的文件共享还能提升团队管理、使用数据效率。
- **Kubernetes**：JuiceFS 支持 Kubernetes CSI；为容器提供解耦的文件存储，令应用服务可以无状态化；方便地在容器间共享数据。
- **共享工作区**：可以在任意主机挂载；没有客户端并发读写限制；POSIX 兼容已有的数据流和脚本操作。
- **数据备份**：在无限平滑扩展的存储空间备份各种数据，结合共享挂载功能，可以将多主机数据汇总至一处，做统一备份。

## 参考

- [JuiceFS 仓库](https://github.com/juicedata/juicefs)
- [JuiceFS 网站](https://juicefs.com/zh-cn/)
