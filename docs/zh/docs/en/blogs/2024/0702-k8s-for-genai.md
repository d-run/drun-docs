# Why K8s and Generative AI Go Hand in Hand

> The original English version is from [run.ai/blog](https://www.run.ai/blog/why-kubernetes-is-the-platform-for-genai)

Kubernetes (K8s) is no longer just a tool for running workloads (such as web applications and microservices); for large AI (Artificial Intelligence) and ML (Machine Learning) workloads like large language models (LLM), K8s is the ideal platform for end-to-end lifecycle management.

In 2021, [a report by Run:ai](https://pages.run.ai/ai-infrastructure-survey-report-2021) found that 42% of respondents indicated they had used K8s for AI/ML workflows. Last year, [Red Hat](https://www.altoros.com/blog/machine-learning-constitutes-65-percent-of-kubernetes-workloads) found that this proportion had increased to 65%, with expectations for even higher numbers this year.

This widespread application spans various industries: from cutting-edge innovative companies like [OpenAI](https://kubernetes.io/case-studies/openai/), to AI cloud service providers like [CoreWeave](https://www.coreweave.com/blog/serverless-kubernetes-what-it-is-and-how-it-works), and well-known brands like [Shell](https://www.altoros.com/blog/shell-builds-10000-ai-models-on-kubernetes-in-less-than-a-day/) and [Spotify](https://www.youtube.com/watch?v=KUyEuY5ZSqI). All these organizations rely on K8s to support their AI/ML distributed workloads.

In this article, we will explore why K8s provides unique support in every lifecycle stage of AI/ML research and engineering.

## Introduction

It is well known that K8s is an efficient container orchestration and management platform in distributed computing environments. It was originally developed by Google as an open-source project to manage its massive internal applications. After becoming open source, it has become the practical standard for deploying, scaling, and managing containerized applications in various environments.

Recently, K8s has been confirmed to be very useful for some emerging use cases: organizations seeking efficient development, training, and deployment of LLMs have begun to leverage this tool. It offers numerous advantages for comprehensive support throughout the entire lifecycle of LLMs, eliminating the need to integrate complex frameworks across different technology stacks. From model pre-training to model deployment, to fine-tuning experiments and application building, K8s can be utilized at every stage of the LLM lifecycle.

## Advantages at Each Stage

### Model Pre-training

![Model Pre-training](../images/gen01.png)

During the model pre-training phase, K8s provides a solid foundation for model training with its unparalleled scalability and resilience. One of K8s's biggest advantages is its ability to automatically scale resources based on demand, which is a critical feature for AI/ML workloads facing enormous computational needs. K8s achieves this by automating the lifecycle management of Pods; if a Pod encounters an error, it will be automatically terminated and restarted. In other words, Pods have self-healing capabilities.

K8s also allows for easy addition or removal of Pods and nodes on demand, enabling dynamic scaling to meet evolving workload requirements. Its declarative infrastructure approach facilitates users in communicating their needs, thereby simplifying management processes. These are powerful development features that cannot be obtained using other tools like Slurm. This means you can achieve higher output and train models more efficiently, without worrying about the limitations of the underlying infrastructure.

Tools like Jupyter Notebooks and VS Code are essential for LLM experiments and prompt engineering, and K8s's network abstraction allows data scientists to easily create development environments and integrate with these tools. Additionally, port forwarding and configuration management occur automatically, simplifying the configuration of end-user workspaces and the environment and network management for cluster administrators.

### Model Fine-tuning

![Model Fine-tuning](../images/gen02.png)

Although K8s has all the tools needed for developing LLMs, many companies today do not start from scratch to build large language models; they often choose existing models and then customize and fine-tune them based on their specific environments. This scenario of fine-tuning existing models is also very suitable for K8s due to its dynamic adaptability. Unlike Slurm, K8s can handle multiple workloads in parallel, making the training process more efficient. Another advantage lies in the rich tool ecosystem that K8s builds for model training, which includes Kubeflow (Operators designed for Pytorch, Tensorflow, and MPI), KubeRay Operator, and MLflow.

### Model Deployment

![Model Deployment](../images/gen03.png)

When it comes to LLM model deployment or model inference services, K8s provides a simplified process: you simply present an endpoint to data scientists. The network stack simplifies the process of releasing models to the outside world, easily pushing the models to the consumer side. K8s offers a comprehensive toolkit and a rich ecosystem for model deployment, including load balancing, Ingress controllers, and network policies. This aids in the seamless deployment of LLM endpoints and their integration with services and applications.

Infrastructure abstraction further simplifies the deployment process, ensuring scalability and automatic scaling capabilities. K8s abstracts all underlying infrastructure into a universal API for managing various containerized applications. Therefore, no matter where the workload runs, you can use the same tools and processes. This greatly simplifies the management and monitoring of production environments.

### Prompt Engineering

![Prompt Engineering](../images/gen04.png)

The advantages do not stop there. After deploying LLM models, K8s can enhance user experience when developing applications or engaging users in model experiments. For example, hosting applications on platforms like Gradio or Streamlit using K8s is almost effortless, as the K8s community has a complete toolkit specifically for cross-platform application hosting. This simplifies the deployment process, while service endpoints and automatic scaling capabilities ensure smooth and scalable experiments.

### Security

At every stage, K8s provides robust security to ensure the safety of your data and intellectual property. For example, role-based access control (RBAC) enables fine-grained access control, granting appropriate permissions to users or service accounts; Pod security contexts allow you to set security attributes at the Pod level, thereby reducing the attack surface within the cluster. These features ensure the environmental security of containers, models, and datasets throughout the entire AI/ML lifecycle.

## Real Success Stories

These advantages are not just theoretical; many of today's most innovative cutting-edge companies are running and managing the entire lifecycle of LLMs on K8s, including leading tech companies operating large-scale clusters (such as OpenAI) and emerging AI cloud service providers (Core Weave, Lambda Cloud Services).

For example, [OpenAI's cluster consists of over 7,500 nodes](https://openai.com/research/scaling-kubernetes-to-7500-nodes), supporting its large language models and distributed machine learning workloads. Despite alternatives like Slurm, K8s provides OpenAI engineers with a superior development experience and a cloud-native integrated environment. With K8s, they can also easily and flexibly deploy containers, manage heterogeneous nodes, and handle dynamic infrastructure components.

!!! quote "Christopher Berner, Infrastructure Lead at OpenAI says"

    The research team can now leverage the framework we built on K8s to easily initiate model experiments and scale experiments by 10x or 50x without spending too much effort on management.

OpenAI runs K8s across multiple data centers in Azure, benefiting from a cluster-wide MPI communication domain that supports cross-node parallel jobs and batch operations. As a batch scheduling system, K8s' autoscaler ensures dynamic scaling, reducing idle node costs while maintaining low latency. Moreover, K8s is incredibly fast, allowing those researching distributed training systems to initiate and scale experiments in days rather than months.

By adopting K8s, OpenAI has found that model portability is excellent, allowing model experiments to be easily migrated between clusters. K8s provides a consistent API that simplifies this migration process. Additionally, while leveraging Azure's infrastructure, OpenAI can also fully utilize its own data centers, saving costs while enhancing availability.

Of course, it is not only large companies like OpenAI that can benefit: K8s has become a mainstream platform for building, training, and deploying language models, completely revolutionizing the [AI landscape](https://mattturck.com/landscape/mad2023.pdf). Hosting AI/ML workloads on K8s offers multiple advantages: scalability, flexibility, network abstraction, and a better user experience during experimentation. With K8s, you can use the best tools and technologies to meet your needs, easily building, training, and deploying AI/ML workloads.
