# 为什么 Kubernetes 是生成式 AI 的理想平台

> 英文原版来自 [run.ai/blog](https://www.run.ai/blog/why-kubernetes-is-the-platform-for-genai)

Kubernetes 不再只是一个运行工作负载的工具，比如 Web 应用程序和微服务；它现在是支持大型人工智能 (AI) 和机器学习 (ML) 工作负载（如大型语言模型 (LLM)）端到端生命周期的理想平台。

在 2021 年，[Run:ai 的一份报告](https://pages.run.ai/ai-infrastructure-survey-report-2021) 发现 42% 的受访者表示他们使用 Kubernetes 进行 AI/ML 工作流。而去年，[Red Hat](https://www.altoros.com/blog/machine-learning-constitutes-65-percent-of-kubernetes-workloads) 发现这个数字已经增加到 65%，预计今年会更高。

这种广泛的采用跨越了多个行业：从像 [OpenAI](https://kubernetes.io/case-studies/openai/) 这样的创新前沿公司，到像 [CoreWeave](https://www.coreweave.com/blog/serverless-kubernetes-what-it-is-and-how-it-works) 这样的 AI 云提供商，再到像 [Shell](https://www.altoros.com/blog/shell-builds-10000-ai-models-on-kubernetes-in-less-than-a-day/) 和 [Spotify](https://www.youtube.com/watch?v=KUyEuY5ZSqI) 这样的知名品牌。这些组织都依赖 K8s 来支持他们的 AI/ML 分布式工作负载。

在这篇文章中，我们将探讨 Kubernetes 如何在每个生命周期阶段独特地支持 AI/ML 研究和工程。

## 引言

Kubernetes 最为人所知的是在分布式计算环境中作为一个高度有效的容器编排和管理平台。它最初由 Google 开发为一个开源项目，以管理他们的内部应用程序。从那时起，它已成为在各种环境中部署、扩展和管理容器化应用程序的事实标准。

但最近，Kubernetes 被证明在一组新的用例中极为有用：它被那些希望高效开发、训练和部署大型语言模型 (LLM) 的组织所利用。它在整个 LLM 生命周期中的全面支持提供了许多优势，消除了在不同技术栈中集成复杂框架的需要，并且可以在 LLM 生命周期的每个阶段使用，从预训练到部署，再到实验和应用构建。

## 各阶段的优势

### 模型预训练

![模型预训练](./images/genai01.png)

在模型预训练阶段，Kubernetes 通过提供无与伦比的可扩展性和弹性提供了一个强大的基础。这种根据资源需求自动扩展和缩减的能力是其最大的优势之一，尤其是对于需要大量计算能力的 AI/ML 工作负载。K8s 通过自动化 pod 的生命周期来实现这一点；如果一个 pod 出现错误，它将被自动终止并重启。换句话说，它是自愈的。

Kubernetes 还通过轻松添加或减少 pod 和节点来实现动态扩展，以满足不断变化的工作负载需求。其声明式基础设施方法允许用户传达他们的需求，简化了管理过程。这些是使用其他工具（如 Slurm）时无法获得的强大开发功能。这意味着您可以拥有更高的吞吐量，更高效地训练模型，而无需手动处理基础设施限制。

像 Jupyter 笔记本和 VS Code 这样的工具对于 LLM 的实验和提示工程是必要的，而 K8s 的网络抽象使数据科学家可以非常轻松地创建开发环境，配备与这些工具的连接。此外，端口转发和配置管理是自动化的，这简化了最终用户的工作空间配置和集群管理员的环境和网络管理。

### 模型微调

![模型微调](./images/genai02.png)

虽然 K8s 拥有开发 LLM 所需的所有工具，但如今许多企业并不是从头开始构建它们，而是采用现有模型并根据其特定上下文进行定制和微调。在这种情况下，当您想要对现有模型进行微调时，K8s 也是理想的选择，因为它非常动态。与 Slurm 不同，K8s 可以同时处理多个工作负载，这使得训练过程更加高效。另一个优势是围绕与 K8s 集成的丰富工具生态系统，用于训练模型。Kubeflow（带有 Pytorch、Tensorflow 和 MPI 的操作符）、KubeRay Operator 和 MLflow 是一些例子。

### 模型部署

![模型部署](./images/genai03.png)

在部署 LLM 本身或推理的模型服务时，Kubernetes 提供了一个简化的过程：您只需要给数据科学家提供一个端点。网络栈简化了将模型发布到外部世界，使其易于使用。K8s 提供了一个全面的工具集和一个丰富的生态系统，用于模型部署，包括负载均衡器、入口控制器、网络策略等。这促进了 LLM 端点的无缝部署及其与服务和应用程序的集成。

基础设施抽象进一步简化了部署过程，确保了可扩展性和自动扩展能力。K8s 抽象了所有底层基础设施，简化为管理容器的通用 API，因此无论工作负载运行在哪里，您都可以使用相同的工具和过程。这极大地简化了生产环境的管理和监控。

### 提示工程

![提示工程](./images/genai04.png)

优势不仅仅止于此。一旦您部署了您的 LLM 模型，Kubernetes 在构建应用程序或让用户实验模型时提供了增强的用户体验。例如，在像 Gradio 或 Streamlit 这样的平台上托管应用程序在 Kubernetes 上几乎是轻而易举的，因为有一整套工具专门用于此。这简化了部署过程，而服务端点和自动扩展功能确保了平滑且可扩展的实验。

### 安全性

在每个阶段，Kubernetes 都具有强大的安全性来确保您的数据和知识产权的安全。例如，基于角色的访问控制 (RBAC) 使您可以进行细粒度的访问控制，授予用户或服务帐户适当的权限；Pod 安全上下文允许您在 pod 级别设置安全属性，减少集群内的攻击面。这些功能确保了在整个 AI/ML 生命周期中，容器、模型和数据集的安全环境。阅读更多关于在 Kubernetes 上安全 AI/ML 环境的内容 [这里](https://www.run.ai/guides/kubernetes-architecture/securing-your-ai-ml-kubernetes-environment)。

## 真实世界的成功案例

这不仅仅是理论上的——最具创新性的前沿公司正在 Kubernetes 上运行其整个 LLM 生命周期，包括在大规模运营的领先技术公司（例如 OpenAI）以及新的 AI 云提供商（Core Weave、Lambda cloud）。

例如，[OpenAI 的集群由超过 7500 个节点组成](https://openai.com/research/scaling-kubernetes-to-7500-nodes)，支持其大型语言模型和分布式机器学习工作负载。尽管有像 Slurm 这样的替代方案，K8s 为他们提供了更有利的开发者体验和云原生集成。它还提供了部署容器、管理异构节点和处理动态基础设施元素的灵活性和简便性。

!!! 引用 "OpenAI 基础设施负责人 Christopher Berner"

    研究团队现在可以利用我们在 Kubernetes 之上构建的框架，这些框架使得启动实验、将其扩展 10 倍或 50 倍变得容易，并且管理起来几乎不费力气。

在 Azure 的不同数据中心上运行 Kubernetes，OpenAI 受益于集群范围内的 MPI 通信器，能够在节点之间进行并行作业和批处理操作。Kubernetes 作为一个批处理调度系统，其自动扩展器确保了动态扩展，减少了空闲节点成本，同时保持低延迟。而且它非常快。研究人员在分布式训练系统上工作时，能够在几天内而不是几个月内启动和扩展实验。

通过采用 Kubernetes，OpenAI 享受到了增强的可移植性，使研究实验在集群之间轻松移动。Kubernetes 提供的一致 API 简化了这一过程。此外，OpenAI 可以结合使用他们自己的数据中心和 Azure，从而节省成本并提高可用性。

但您不必是与 OpenAI 规模相同的公司才能受益：Kubernetes 已成为构建、训练和部署语言模型的主导平台，彻底改变了 AI 领域（您可以从 [这个图表](https://mattturck.com/landscape/mad2023.pdf) 看出它所产生的巨大影响）。在 Kubernetes 上托管 AI/ML 工作负载具有多个优势：可扩展性、灵活性、网络抽象以及在实验时更好的用户体验。借助 Kubernetes，您可以轻松构建、训练和部署您的 AI/ML 工作负载，使用最适合您需求的最佳工具和技术。
