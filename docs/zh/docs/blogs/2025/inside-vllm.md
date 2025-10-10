# vLLM 内参：深度剖析高吞吐量大语言模型推理系统

> 英文原稿转载自 [www.aleksagordic.com](https://www.aleksagordic.com/blog/vllm)

**从分页注意力、连续批处理、前缀缓存、投机解码等技术，到多 GPU、多节点的大规模动态部署**

2025 年 8 月 29 日

本文将循序渐进地介绍构成现代高吞吐量大语言模型推理系统的所有核心组件和高级特性。
特别是将深入剖析 vLLM [[1]](https://www.aleksagordic.com/blog/vllm#ref-1) 的工作原理。

本文是系列文章的第一篇。本文采用倒金字塔方法，从宏观入手，然后逐层深入细节，
以便你能在不被琐碎细节淹没的情况下，对整个系统形成精确的高层次心智模型。

后续博文将深入探讨各个具体的子系统。

本文结构分为五个部分：

1. [大语言模型引擎和引擎核心](https://www.aleksagordic.com/blog/vllm#cpt1)：vLLM 基础知识（调度、分页注意力、连续批处理等）
2. [高级特性](https://www.aleksagordic.com/blog/vllm#cpt2)：分块预填充、前缀缓存、引导解码与投机解码、P/D 分离
3. [扩容](https://www.aleksagordic.com/blog/vllm#cpt3)：从单 GPU 到多 GPU
4. [分层部署](https://www.aleksagordic.com/blog/vllm#cpt4)：分布式/并发 Web 框架
5. [基准测试与自动调优](https://www.aleksagordic.com/blog/vllm#cpt5)：测量延迟和吞吐量

!!! note

    - 本文的数据分析基于 [commit 42172ad](https://github.com/vllm-project/vllm/tree/42172ad)（2025 年 8 月 9 日）。
    - 目标受众：对最先进大语言模型引擎工作原理感到好奇的所有人，以及有兴趣为 vLLM、SGLang 等项目做贡献的那些人。
    - 本文将重点介绍 [V1 引擎](https://docs.vllm.ai/en/latest/usage/v1_guide.html)。
      本文也探究了 V0（[现已弃用](https://github.com/vllm-project/vllm/issues/18571)），
      这对于理解 vLLM 项目的演进过程很有价值，因为其中的许多概念是贯穿始终的。
    - 第一节讲述大语言模型引擎/引擎核心，可能有点枯燥，不过其余的章节提供了大量的示例和插图。😊

## 大语言模型引擎和引擎核心

大语言模型引擎是 vLLM 的基础构建模块。仅凭其自身，它已经能够实现高吞吐量推理——但仅限于离线场景。
你还不能通过网络将其作为服务提供给客户。

我们将使用以下离线推理示例作为运行示例（以下代码改编自 [basic.py](https://github.com/vllm-project/vllm/blob/main/examples/offline_inference/basic/basic.py)）。

```python
from vllm import LLM, SamplingParams

prompts = [
    "Hello, my name is",
    "The president of the United States is",
]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

def main():
    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    outputs = llm.generate(prompts, sampling_params)

if __name__ == "__main__":
    main()
```

!!! note "环境变量:"

    - VLLM_USE_V1="1" # 使用的是引擎 V1
    - VLLM_ENABLE_V1_MULTIPROCESSING="0" # 在单进程中运行

上述配置是：

- 离线的（没有 Web/分布式系统的框架）
- 同步的（所有执行发生在单个阻塞进程中）
- 单 GPU（没有数据/模型/流水线/专家并行；DP/TP/PP/EP = 1）
- 使用标准 Transformer [[2]](https://www.aleksagordic.com/blog/vllm#ref-2)（支持 Jamba 等混合模型需要更复杂的混合 KV-cache 内存分配器）

从这里开始，我们将逐步构建一个在线、异步、多 GPU、多节点的推理系统——但仍然部署标准的 Transformer。

在此示例中，我们做两件事：

1. 实例化一个引擎
2. 调用 `generate` 从给定的提示词中采样

让我们从分析构造函数开始。

## 大语言模型引擎构造函数

引擎的主要组件包括：

- vLLM 配置（包含模型、缓存、并行机制等的所有配置参数）
- 处理器（通过验证、分词和处理，将原始输入转化成 `EngineCoreRequests`）
- 引擎核心客户端（在本文的示例中使用 `InprocClient`，基本上等同于 `EngineCore`；本文将逐步构建到 `DPLBAsyncMPClient`，以支持大规模部署）
- 输出处理器（将原始 `EngineCoreOutputs` 转化成用户可见的 `RequestOutput`）

!!! note

    随着 V0 引擎被弃用，许多类名和细节发生了变化。本文将强调核心理念，而非吹毛求疵。本文将抽象掉部分但不是全部细节。

引擎核心本身由几个子组件组成：

- 模型执行器（驱动模型的前向计算，目前我们使用 `UniProcExecutor`，它在单 GPU 上有一个 `Worker` 进程）。我们将逐步构建到支持多 GPU 的 `MultiProcExecutor`
- 结构化输出管理器（用于引导解码——稍后讲解）
- 调度器（决定哪些请求进入下一步引擎计算），调度器进一步包含：

    1. 策略设置：可以是 **FCFS**（先到先服务）或 **priority**（优先级高的请求优先服务）
    2. `waiting` 和 `running` 队列
    3. KV-cache 管理器：分页注意力的核心 [[3]](https://www.aleksagordic.com/blog/vllm#ref-3)

KV-cache 管理器维护一个 `free_block_queue`。这是所有可用 KV-cache 块形成的池（通常有几十万块，具体取决于显存大小和块大小）。在分页注意力期间，这些块作为索引结构，将 Token 映射到其计算的各个 KV-cache 块上。

![大语言模型引擎构造函数](https://www.aleksagordic.com/blog/vllm/engine_constructor.png)

<div style="text-align: center;">
图 1. 本节描述的核心组件及其关系
</div>

!!! tip

    标准 Transformer 层（非 MLA [[4]](https://www.aleksagordic.com/blog/vllm#ref-4)）的块大小计算公式为：

    2 (key/value) * `block_size`（默认=16） * `num_kv_heads` * `head_size` * `dtype_num_bytes`（例如 bf16 为 2）

在模型执行器构建过程中，会创建一个 `Worker` 对象，并执行三个关键过程。
（后续在 `MultiProcExecutor` 中，这些过程将在不同 GPU 上的每个 Worker 进程中独立运行。）

1. 初始化设备：

    - 为 Worker 分配 CUDA 设备（例如 "cuda:0"）并检查模型的数据类型是否受支持（例如 bf16）
    - 根据请求的 `gpu_memory_utilization`（例如 0.8 是总显存的 80%）验证是否有足够的显存
    - 设置分布式配置（DP/TP/PP/EP 等）
    - 实例化一个 `model_runner`（持有采样器、KV-cache 以及前向计算缓冲区，如 `input_ids`、`positions` 等）
    - 实例化一个 `InputBatch` 对象（持有 CPU 端前向计算缓冲区、KV-cache 索引的块表、采样元数据等）

2. 加载模型：

    - 实例化模型架构
    - 加载模型权重
    - 调用 model.eval()（PyTorch 的推理模式）
    - 可选：对模型调用 torch.compile()

3. 初始化 KV-cache：

    - 获取每层的 KV-cache 规格。历史上这总是 `FullAttentionSpec`（同质 Transformer），但对于混合模型（滑动窗口、Transformer/SSM 类 Jamba）会更复杂（参见 Jenga [[5]](https://www.aleksagordic.com/blog/vllm#ref-5)）
    - 执行一次虚拟/分析前向计算并获取 GPU 内存快照，以计算可用显存中能容纳多少 KV-cache 块
    - 分配、调整形状并绑定 KV-cache 张量到注意力层
    - 准备注意力元数据（例如将后端设置为 FlashAttention），以供前向计算时内核使用
    - 除非提供 `--enforce-eager`，否则对每个预热批次大小执行一次虚拟运行并捕获 CUDA 图。CUDA 图将整个 GPU 工作序列记录为 DAG。在后续前向计算中，我们直接启动/重放预先构建的图，从而减少内核启动开销并改善延迟

这里我抽象掉了许多底层细节——但这些是核心部分，因为在接下来的章节中我会反复引用它们。

现在我们已经初始化了引擎，让我们继续看 `generate` 函数。

## `generate` 函数

第一步是验证并将请求送入引擎。对于每个提示词，我们：

1. 创建唯一请求 ID 并记录到达时间
2. 调用输入预处理器，将提示词分词并返回一个字典，包含 `prompt`、`prompt_token_ids` 和 `type`（text、tokens、embeds 等）
3. 将这些信息打包进 `EngineCoreRequest`，添加优先级、采样参数和其他元数据
4. 将请求传入引擎核心，它会将请求包装为 `Request` 对象并将状态设置为 `WAITING`。然后该请求被加入调度器的 `waiting` 队列（如果是先来先服务（FCFS），则追加；如果是按优先级，则使用堆插入（heap-push）。）

此时，引擎已被喂入数据，执行可以开始。在同步引擎示例中，这些初始提示词是唯一处理的请求——没有机制在运行中注入新请求。相比之下，异步引擎支持此功能（即 **连续批处理** [[6]](https://www.aleksagordic.com/blog/vllm#ref-6)）：每步结束后，会同时考虑新旧请求。

!!! tip

    由于前向计算将批次展平为单个序列，且自定义内核高效处理它，即使在同步引擎中也能从根本上支持连续批处理。

接下来，只要有请求需要处理，引擎就会反复调用 `step()` 函数。每一步包含三个阶段：

1. 调度：选择本步要运行的请求（解码和/或（分块）预填充）
2. 前向计算：运行模型并采样 Token
3. 后处理：将采样的 Token ID 添加到每个 `Request`，反分词，并检查停止条件。如果请求完成，清理（例如将 KV-cache 块返回 `free_block_queue`）并提前返回输出

!!! note "停止条件为："

    - 请求超过长度限制（`max_model_length` 或其自身的 `max_tokens`）
    - 采样 Token 为 EOS ID（除非启用 `ignore_eos` -> 用于基准测试时强制生成一定数量的输出 Token）
    - 采样 Token 匹配采样参数中指定的任意 `stop_token_ids`
    - 输出中出现停止字符串——我们会截断输出直到第一个停止字符串出现，并在引擎中终止请求（注意 `stop_token_ids` 会出现在输出中，但停止字符串不会）

![引擎循环](https://www.aleksagordic.com/blog/vllm/engine_loop.png)

<div style="text-align: center;">
图 2. 引擎循环
</div>

!!! tip

    在流式模式下，我们会在生成中间 Token 时发送它们，但这里暂且忽略。

接下来，我们将更详细地探讨调度。

## 调度器

推理引擎主要处理两类工作负载：

1. **预填充请求** - 对所有提示词 Token 执行一次前向计算。这类请求通常是 **计算受限** 的（阈值取决于硬件和提示词长度）。在末尾，我们从最后一个 Token 的概率分布中采样一个 Token。
2. **解码请求** - 仅对最近的 Token 执行前向计算。之前的所有 KV 向量已经缓存。这类请求是 **内存带宽受限** 的，因为我们仍然需要加载所有大语言模型权重（以及 KV-cache）才能计算一个 Token。

!!! tip

    在 [基准测试章节](https://www.aleksagordic.com/blog/vllm#cpt5) 中，我们将分析 GPU 性能的所谓 roofline 模型，这将详细说明预填充/解码的性能特征。

V1 调度器可以在同一步中混合处理两类请求，这得益于更智能的设计选择。相比之下，V0 引擎一次只能处理预填充或解码请求。

调度器优先处理解码请求——即那些已在 `running` 队列中的请求。对于每个请求，它会：

1. 计算需要生成的新 Token 数量（不总是 1，受投机解码和异步调度影响——稍后讲解）。
2. 调用 KV-cache 管理器的 `allocate_slots` 函数（详情见下文）。
3. 通过减去步骤 1 的 Token 数量更新 Token 预算。

之后，它处理来自 `waiting` 队列的预填充请求：

1. 获取已计算块的数量（如果禁用前缀缓存则返回 0——稍后讲解）。
2. 调用 KV-cache 管理器的 `allocate_slots` 函数。
3. 将请求从 waiting 弹出并移动到 running，设置状态为 `RUNNING`。
4. 更新 Token 预算。

接下来看看 `allocate_slots` 的工作：

1. **计算块数** - 确定需要分配多少新的 KV-cache 块（`n`）。每块默认存储 16 个 Token。例如，一个预填充请求有 17 个新 Token，则需要 `ceil(17/16) = 2` 块。
2. **检查可用性** - 如果管理器的池中没有足够的块，则提前退出。根据请求类型（解码或预填充），引擎可能尝试重新计算抢占（V0 支持交换抢占），通过调用 `kv_cache_manager.free` 将低优先级请求的 KV 块释放回块池，或者跳过调度继续执行。
3. **分配块** - 通过 KV-cache 管理器的协调器，从块池（前文提到的 `free_block_queue` 双向链表）获取前 `n` 块。存入 `req_to_blocks` 字典，将每个 `request_id` 映射到其 KV-cache 块列表。

![KV-cache 块](https://www.aleksagordic.com/blog/vllm/kv_cache_blocks.png)

<div style="text-align: center;">
图 3. KV-cache 块列表
</div>

现在，我们可以进行前向计算了！

## 执行前向计算

我们调用模型执行器的 `execute_model`，它委托给 `Worker`，再由 `Worker` 委托给 `model_runner`。

主要步骤如下：

1. **更新状态** - 从 `input_batch` 中修剪完成的请求；更新前向计算相关的杂项元数据（例如每个请求将用于索引分页 KV-cache 内存的 KV-cache 块）。
2. **准备输入** - 将缓冲区从 CPU → GPU；计算位置；构建 `slot_mapping`（示例中详细说明）；构建注意力元数据。
3. **前向计算** - 使用自定义分页注意力内核运行模型。所有序列被展平并连接为一个长的“超序列”。位置索引和注意力掩码确保每个序列只关注自己的 Token，从而支持连续批处理而无需右侧填充。
4. **收集最后 Token 状态** - 提取每个序列最终位置的隐藏状态并计算 logits（原始得分）。
5. **采样** - 根据采样配置（贪心、temperature、top-p、top-k 等）从计算得到的 logits 中采样 Token。

前向计算步骤有两种执行模式：

1. **Eager 模式** - 启用 eager 执行时运行标准 PyTorch 前向计算。
2. **“Captured” 模式** - 如果未强制 eager 执行，则执行/重放预先捕获的 CUDA 图（记住我们在引擎构建期间的初始化 KV-cache 步骤中捕获过这些图）。

下面的示例可以清楚地展示连续批处理和分页注意力：

![前向计算 - 连续批处理 & 分页注意力](https://www.aleksagordic.com/blog/vllm/fwd_pass.png)

<div style="text-align: center;">
图 4. 前向计算：连续批处理与分页注意力
</div>

## 高级功能 — 扩展核心引擎逻辑

在基础引擎流程建立之后，我们现在可以看看高级功能。

我们已经讨论了抢占、分页注意力和连续批处理。

接下来，我们将深入探讨：

1. 分块预填充
2. 前缀缓存
3. 引导解码（通过语法约束的有限状态机）
4. 投机解码
5. P/D 分离（预填充/解码）

## 分块预填充

分块预填充是处理长提示词的一种技术，它通过将预填充步骤拆分为更小的块来执行。若不使用此方法，可能会出现单个非常长的请求独占一次引擎步骤，从而阻止其他预填充请求运行。这会延迟所有其他请求并增加它们的延迟。

例如，每个块包含 `n` (=8) 个 Token，用小写字母表示并以 "-" 分隔。一个长提示词 `P` 可以表示为 `x-y-z`，其中 `z` 是不完整的块（例如 2 个 Token）。执行完整的 `P`预填充将需要 ≥ 3 个引擎步骤（如果某步未被调度执行，则可能更多），并且仅在最后的分块预填充步骤中，我们才会采样一个新的 Token。

下面是该示例的可视化表示：

![分块预填充- pt 1](https://www.aleksagordic.com/blog/vllm/chunked_pt1.png)

实现方法很简单：限制每步的新 Token 数量。如果请求的数量超过 `long_prefill_token_threshold`，则重置为该阈值。底层索引逻辑（前文描述）会处理剩余部分。

在 vLLM V1 中，可以通过将 `long_prefill_token_threshold` 设置为正整数来启用分块预填充。（技术上，即使未设置该值，如果提示词长度超过 Token 预算，也会截断并执行分块预填充。）

## 前缀缓存

为了说明前缀缓存的工作原理，我们可以对原始代码示例进行一些调整：

```python
from vllm import LLM, SamplingParams

long_prefix = "<a piece of text that is encoded into more than block_size tokens>"

prompts = [
    "Hello, my name is",
    "The president of the United States is",
]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

def main():
    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    outputs = llm.generate(long_prefix + prompts[0], sampling_params)
    outputs = llm.generate(long_prefix + prompts[1], sampling_params)

if __name__ == "__main__":
    main()
```

前缀缓存可以避免重新计算多个提示词在开头共享的 Token——因此称为 **前缀** 。

关键在于 `long_prefix`：它被定义为任何比 KV-cache 块长的前缀（默认每块 16 个 Token）。为了简化示例，我们假设 `long_prefix` 的长度正好为 `n x block_size`（其中 `n ≥ 1`）。

!!! tip

    即它与块边界完全对齐——否则我们必须重新计算 `long_prefix_len % block_size` 个 Token，因为无法缓存不完整的块。

如果不使用前缀缓存，每次处理带有相同 `long_prefix` 的新请求时，都需要重新计算所有 `n x block_size` 个 Token。

使用前缀缓存，这些 Token 只计算一次（其 KV 存储在分页 KV-cache 内存中），然后重复使用，因此只需处理新的提示词 Token。这会加速预填充请求（但对解码没有帮助）。

在 vLLM 中这是如何实现的？

在第一次 `generate` 调用中，在调度阶段，`kv_cache_manager.get_computed_blocks` 内部，引擎会调用 `hash_request_tokens`：

1. 该函数将 `long_prefix + prompts[0]` 拆分为 16-token 的块。
2. 对每个完整块，计算一个哈希（使用内置哈希或 SHA-256，SHA-256 更慢但冲突更少）。哈希结合前一个块的哈希、当前 Token 和可选元数据。

    !!! tip

        可选元数据包括：MM hash、LoRA ID、cache salt（注入到第一个块的哈希中，确保只有具有该 cache salt 的请求才能重用这些块）。

3. 每个结果存储为一个 `BlockHash` 对象，包含哈希值和其 Token ID。返回块哈希列表。

该列表存储在 `self.req_to_block_hashes[request_id]` 中。

接下来，引擎调用 `find_longest_cache_hit` 检查这些哈希是否已存在于 `cached_block_hash_to_block` 中。对于第一次请求，没有命中。

![前缀缓存逻辑 - pt 1](https://www.aleksagordic.com/blog/vllm/prefix_pt1.png)

然后我们调用 `allocate_slots`，它进一步调用 `coordinator.cache_blocks`，将新的 `BlockHash` 条目与分配的 KV 块关联，并记录到 `cached_block_hash_to_block` 中。

随后，前向计算会在分页 KV-cache 内存中填充与上述 KV-cache 块对应的 KV。

!!! tip

    多次引擎步骤后，会分配更多 KV-cache 块，但对于本示例无关紧要，因为前缀在 `long_prefix` 后立即分叉。

![前缀缓存逻辑 - pt 2](https://www.aleksagordic.com/blog/vllm/prefix_pt2.png)

在第二次带相同前缀的 `generate` 调用中，步骤 1-3 重复执行，但这次 `find_longest_cache_hit` 通过线性搜索找到所有 `n` 块的匹配。引擎可以直接重用这些 KV 块。

![前缀缓存逻辑 - pt 3](https://www.aleksagordic.com/blog/vllm/prefix_pt3.png)

如果原始请求仍然存在，这些块的引用计数会增加（例如为 2）。在本例中，第一个请求已经完成，因此这些块已释放回池，其引用计数恢复为 0。由于我们可以从 `cached_block_hash_to_block` 中检索它们，说明它们有效（KV-cache 管理器的逻辑确保了这一点），因此我们再次将它们从 `free_block_queue` 中移除。

!!! note "高级说明:"

    KV-cache 块只有在即将从 `free_block_queue` 重新分配时才会失效（从左侧弹出），且我们发现该块仍有关联哈希并存在于 `cached_block_hash_to_block` 中。此时，我们清除该块的哈希并从 `cached_block_hash_to_block` 中移除其条目，确保它不能通过前缀缓存重用（至少对旧前缀无效）。

这就是前缀缓存的核心：不要重复计算已经见过的前缀——直接重用它们的 KV-cache！

!!! tip

    如果你理解了这个示例，你也就理解了分页注意力的工作原理。

前缀缓存默认启用。若要禁用：`enable_prefix_caching = False`。

## 引导解码（有限状态机）

引导解码是一种技术，在每个解码步骤中，logits 会受到基于语法的有限状态机约束。这确保了只有符合语法的 Token 才能被采样。

这是一个强大的设置：你可以强制执行从正则语法（Chomsky 类型-3，例如任意正则表达式模式）到上下文无关语法（类型-2，覆盖大多数编程语言）的约束。

为了让它不那么抽象，我们从最简单的示例开始，基于之前的代码：

```python
from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

prompts = [
    "This sucks",
    "The weather is beautiful",
]

guided_decoding_params = GuidedDecodingParams(choice=["Positive", "Negative"])
sampling_params = SamplingParams(guided_decoding=guided_decoding_params)

def main():
    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    outputs = llm.generate(prompts, sampling_params)

if __name__ == "__main__":
    main()
```

在我给出的玩具示例中（假设字符级分词）：在预填充阶段，FSM 会屏蔽 logits，使得只有 "P" 或 "N" 是可行的。如果采样到 "P"，FSM 会移动到 "Positive" 分支；下一步只允许 "o"，依此类推。

![FSM](https://www.aleksagordic.com/blog/vllm/fsm.png)

<div style="text-align: center;">
图 5. 玩具示例 FSM
</div>

在 vLLM 中的实现方式：

1. 在大语言模型引擎构建时，创建一个 `StructuredOutputManager`；它可以访问分词器，并维护 `_grammar_bitmask` 张量。
2. 添加请求时，其状态被设置为 `WAITING_FOR_FSM`，并由 `grammar_init` 选择后端编译器（例如 `xgrammar` [[7]](https://www.aleksagordic.com/blog/vllm#ref-7)；注意后端为第三方代码）。
3. 该请求的语法会异步编译。
4. 在调度阶段，如果异步编译完成，状态切换为 `WAITING`，并将 `request_id` 添加到 `structured_output_request_ids`；否则，它被放入 `skipped_waiting_requests`，在下一步引擎循环中重试。
5. 调度循环结束后（仍在调度阶段），如果有 FSM 请求，`StructuredOutputManager` 会请求后端准备/更新 `_grammar_bitmask`。
6. 前向计算生成 logits 后，xgr_torch_compile 的函数会将 bitmask 扩展到词表大小（因为使用 32 位整数，扩展比例为 32 倍），并将不允许的 logits 设置为 –∞。
7. 采样下一个 Token 后，通过 `accept_tokens` 推进请求的 FSM。在图示中，FSM 状态移动到下一节点。

步骤 6 需要进一步说明。

如果 `vocab_size = 32`，`_grammar_bitmask` 是一个整数；其二进制表示编码了允许的 Token（"1"）与不允许的 Token（"0"）。例如，"101…001" 展开为长度为 32 的数组 `[1, 0, 1, …, 0, 0, 1]`；位置为 0 的 logits 会被设置为 –∞。对于更大的词表，会使用多个 32 位整数并进行扩展/拼接。后端（如 `xgrammar`）负责根据当前 FSM 状态生成这些位模式。

!!! note

    大部分复杂性隐藏在第三方库（如 xgrammar）中。

这里是一个更简单的示例，`vocab_size = 8` 且使用 8 位整数（适合喜欢可视化的朋友）：

![FSM](https://www.aleksagordic.com/blog/vllm/fsm2.png)

<div style="text-align: center;">
图 6. 玩具示例
</div>

可以通过传入所需的 `guided_decoding` 配置在 vLLM 中启用此功能。

## 投机解码

在自回归生成中，每生成一个新 Token 都需要对大语言模型执行一次前向计算。这非常昂贵——每一步都要重新加载并应用所有模型权重，仅为了计算一个 Token！（假设批次大小 = 1，一般为 `B`）

投机解码 [[8]](https://www.aleksagordic.com/blog/vllm#ref-8) 通过引入一个较小的草稿模型来加速。草稿模型廉价地提出 `k` 个 Token 候选。但我们最终并不希望从小模型中采样——它只是用来猜测候选续写。大模型仍然决定哪些 Token 有效。

步骤如下：

1. **草稿（Draft）:** 在当前上下文上运行小模型，提出 `k` 个 Token。

2. **验证（Verify）:** 在上下文 + `k` 个草稿 Token 上运行大模型一次。这会生成这 `k` 个位置加上一个额外位置的概率（所以得到 `k+1` 个候选）。

3. **接受/拒绝:** 从左到右处理 `k` 个草稿 Token：

    - 如果大模型对该 Token 的概率 ≥ 草稿模型的概率，则接受
    - 否则，以概率 `p_large(token)/p_draft(token)` 接受
    - 在第一次拒绝处停止，或者接受全部 `k` 个草稿 Token

        - 如果全部 `k` 个 Token 都被接受，则还可以“免费”采样额外的第 `(k+1)` 个 Token（大模型已经计算了该分布）。
        - 如果出现拒绝，则在该位置创建新的重新平衡分布 (`p_large - p_draft`，最小值截断为 0，并归一化)，并从中采样最后一个 Token。

**为什么可行:** 虽然使用小模型提出候选，但接受/拒绝规则保证在期望上序列分布与逐 Token 从大模型采样完全一致。这意味着投机解码在统计上等价于标准自回归解码——但潜在速度更快，因为一次大模型前向计算最多可生成 `k+1` 个 Token。

!!! note

    推荐查看 [gpt-fast](https://github.com/meta-pytorch/gpt-fast) 了解简单实现，以及 [原论文](https://arxiv.org/abs/2302.01318) 获取数学细节及与全模型采样等价的证明。

vLLM V1 不支持使用 LLM 草稿模型方法，而是实现了更快但准确性略低的候选方案：n-gram、EAGLE [[9]](https://www.aleksagordic.com/blog/vllm#ref-9) 和 Medusa [[10]](https://www.aleksagordic.com/blog/vllm#ref-10)。

各方案简述：

1. **n-gram:** 取最后 `prompt_lookup_max` 个 Token；在序列中找到之前匹配；如果找到，提出该匹配后的 `k` 个 Token；否则缩小窗口并重试，直到 `prompt_lookup_min`。

    !!! tip

        当前实现返回 **第一次匹配** 后的 `k` 个 Token。是否可以引入新近性偏置并反向搜索（即最后一次匹配）会更自然？

2. **EAGLE:** 对大模型执行“模型手术”——保留 embeddings 和 LM head，将 Transformer 堆替换为轻量 MLP；微调它作为廉价草稿。
3. **Medusa:** 在大模型上训练辅助线性 head（LM head 前的 embeddings）以并行预测下 `k` 个 Token；利用这些 head 比运行独立小模型更高效地提出 Token。

下面是如何在 vLLM 中使用 `ngram` 方法调用投机解码：

```python
from vllm import LLM, SamplingParams

prompts = [
    "Hello, my name is",
    "The president of the United States is",
]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

speculative_config={
    "method": "ngram",
    "prompt_lookup_max": 5,
    "prompt_lookup_min": 3,
    "num_speculative_tokens": 3,
}

def main():
    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", speculative_config=speculative_config)

    outputs = llm.generate(prompts, sampling_params)

if __name__ == "__main__":
    main()
```

在 vLLM 中，这一流程是如何实现的？

**设置（在引擎构建阶段）:** 

1. 初始化设备：创建一个 `drafter`（草稿模型，例如 `NgramProposer`）和一个 `rejection_sampler`（部分实现基于 Triton）。
2. 加载模型：加载草稿模型权重（对于 n-gram 无操作）。

**之后在 `generate` 函数中**（假设我们得到一个全新的请求）：

1. 使用大模型执行常规预填充步骤。
2. 前向计算和标准采样后，调用 `propose_draft_token_ids(k)` 从草稿模型采样 `k` 个草稿 Token。
3. 将这些 Token 存储在 `request.spec_token_ids`（更新请求元数据）。
4. 在下一次引擎步骤中，当请求处于 running 队列时，将 `len(request.spec_token_ids)` 添加到“新 Token”计数，以便 `allocate_slots` 为前向计算保留足够的 KV 块。
5. 将 `spec_token_ids` 拷贝到 `input_batch.token_ids_cpu` 中，形成（上下文 + 草稿）Token。
6. 通过 `_calc_spec_decode_metadata` 计算元数据（这会拷贝 `input_batch.token_ids_cpu` 中的 Token，准备 logits 等），然后对草稿 Token 运行大模型前向计算。
7. 不再从 logits 常规采样，而是使用 `rejection_sampler` 左到右进行接受/拒绝，生成 `output_token_ids`。
8. 重复步骤 2-7，直到满足停止条件。

理解这一流程的最佳方式是启动调试器，逐步跟踪代码。但本节希望给你一个直观的感觉：

![Drafting stage](https://www.aleksagordic.com/blog/vllm/specdec_pt1.png)

![Verify stage & rejection sampling stage](https://www.aleksagordic.com/blog/vllm/specdec_pt2.png)

## P/D 分离

上文提到了 P/D 分离的动机。

预填充和解码的性能特性非常不同（计算受限 vs. 内存带宽受限），因此将它们分离执行是合理的设计。这能更紧密地控制延迟，
包括 `TFTT`（time-to-first-token，第一个 Token 的时间）和 `ITL`（inter-token latency，即 Token 间延迟）。
更多内容见[基准测试](https://www.aleksagordic.com/blog/vllm#cpt5) 章节。

实际操作中，我们运行 `N` 个 vLLM预填充实例和 `M` 个 vLLM 解码实例，根据实时请求负载自动伸缩。预填充工作线程将 KV 写入专用 KV-cache 服务；解码工作线程从中读取。这将长时间、突发的预填充与稳定、延迟敏感的解码隔离开来。

在 vLLM 中是如何实现的？

为便于说明，下面示例依赖 `SharedStorageConnector`，这是一个用于调试的 Connector 实现，用于演示 KV 交换机制。

!!! tip

    Connector 是 vLLM 对实例间 KV 交换的抽象。Connector 接口尚不稳定，近期计划会有改进，其中一些可能涉及破坏性更改。

我们启动 2 个 vLLM 实例（GPU 0 用于预填充，GPU 1 用于解码），然后在它们之间传输 KV-cache：

```python
import os
import time
from multiprocessing import Event, Process
import multiprocessing as mp

from vllm import LLM, SamplingParams
from vllm.config import KVTransferConfig

prompts = [
    "Hello, my name is",
    "The president of the United States is",
]

def run_prefill(prefill_done):
  os.environ["CUDA_VISIBLE_DEVICES"] = "0"

  sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=1)

  ktc=KVTransferConfig(
      kv_connector="SharedStorageConnector",
      kv_role="kv_both",
      kv_connector_extra_config={"shared_storage_path": "local_storage"},
  )

  llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", kv_transfer_config=ktc)
  llm.generate(prompts, sampling_params)

  prefill_done.set()  # notify decode instance that KV cache is ready

  # To keep the prefill node running in case the decode node is not done;
  # otherwise, the script might exit prematurely, causing incomplete decoding.
  try:
      while True:
          time.sleep(1)
  except KeyboardInterrupt:
      print("Script stopped by user.")

def run_decode(prefill_done):
  os.environ["CUDA_VISIBLE_DEVICES"] = "1"

  sampling_params = SamplingParams(temperature=0, top_p=0.95)

  ktc=KVTransferConfig(
      kv_connector="SharedStorageConnector",
      kv_role="kv_both",
      kv_connector_extra_config={"shared_storage_path": "local_storage"},
  )

  llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", kv_transfer_config=ktc)

  prefill_done.wait()  # block waiting for KV cache from prefill instance

  # Internally it'll first fetch KV cache before starting the decoding loop
  outputs = llm.generate(prompts, sampling_params)

if __name__ == "__main__":
  prefill_done = Event()
  prefill_process = Process(target=run_prefill, args=(prefill_done,))
  decode_process = Process(target=run_decode, args=(prefill_done,))

  prefill_process.start()
  decode_process.start()

  decode_process.join()
  prefill_process.terminate()
```

!!! note

    我还尝试过 `LMCache` [[11]](https://www.aleksagordic.com/blog/vllm#ref-11)，这是最快的生产就绪 Connector（使用 NVIDIA 的 NIXL 作为后端），但它仍处于前沿状态，我遇到了一些 bug。由于其复杂性大多存在于外部仓库中，因此 `SharedStorageConnector` 更适合作为讲解示例。

在 vLLM 中的步骤如下：

1. **实例化** — 在引擎构建阶段，Connector 在两个地方创建：

    - 在 Worker 的初始化设备流程中（位于初始化 Worker 分布式环境函数下），角色为 "worker"。
    - 在 Scheduler 构造函数中，角色为 "Scheduler"。

2. **缓存查询** — 当 Scheduler 处理 `waiting` 队列中的预填充请求（本地前缀缓存检查后），调用 Connector 的 `get_num_new_matched_tokens`。该函数检查 KV-cache 服务器中是否有外部缓存的 Token。预填充始终返回 0；解码可能命中缓存。结果会在调用 `allocate_slots` 前加入本地计数。

3. **状态更新** — Scheduler 调用 `connector.update_state_after_alloc`，记录有缓存的请求（对于预填充为不执行任何操作）。

4. **元数据构建** — 调度结束时，Scheduler 调用 `meta = connector.build_connector_meta`

    - 预填充将所有 `is_store=True` 的请求添加进来（用于上传 KV）。
    - 解码将 `is_store=False` 的请求添加进来（用于获取 KV）。

5. **上下文管理器** — 在前向计算之前，引擎进入 KV-connector 上下文管理器：

    - 进入时：调用 `kv_connector.start_load_kv`。对于解码，这会从外部服务器加载 KV 并注入分页内存；对于预填充，则为不执行任何操作。
    - 退出时：调用 `kv_connector.wait_for_save`。对于预填充，会阻塞直到 KV 上传到外部服务器；对于解码，则为不执行任何操作。

下面是一个可视化示例：

![P/D 分离](https://www.aleksagordic.com/blog/vllm/pd.png)

<div style="text-align: center;">
图 7. P/D 分离
</div>

!!! note "附加说明:"

    - 对于 `SharedStorageConnector`，“外部服务器”仅为本地文件系统。
    - 根据配置，KV 传输也可以按层进行（在每个 attention 层前/后）。
    - 解码只在请求的第一步加载外部 KV；之后在本地计算/存储。

## 从 UniprocExecutor 到 MultiProcExecutor

在掌握了核心技术之后，我们可以讨论扩展方案。

假设你的模型权重已经无法放入单个 GPU 的显存。

第一个方案是在同一节点的多块 GPU 上进行张量并行（tensor parallelism, TP，例如 `TP=8`）来切分模型。如果模型仍然无法容纳，下一步就是跨节点的流水线并行（pipeline parallelism, PP）。

!!! note

    - 节点内带宽远高于节点间带宽，这也是为什么通常优先选择张量并行（TP）而非流水线并行（PP）。（同时，PP 传输的数据量也少于 TP。）
    - 我不讨论 expert parallelism (EP)，因为我们关注的是标准 Transformer 而非 MoE，也不讨论 sequence parallelism，因为 TP 和 PP 在实践中最常用。

在这个阶段，我们需要多个 GPU 进程（Worker）以及一个协调层来管理它们。这正是 `MultiProcExecutor` 提供的功能。

![MultiProcExecutor](https://www.aleksagordic.com/blog/vllm/multiprocexecutor.png)

<div style="text-align: center;">
图 8. TP=8 设置下的 MultiProcExecutor（驱动 Worker 为 rank 0）
</div>

在 vLLM 中的实现方式：

1. `MultiProcExecutor` 初始化一个 `rpc_broadcast_mq` 消息队列（底层基于共享内存实现）。
2. 构造函数遍历 `world_size`（例如 `TP=8 ⇒ world_size=8`），并通过 `WorkerProc.make_worker_process` 为每个 rank 启动守护进程。
3. 对每个 Worker，父进程首先创建 reader 和 writer 管道。
4. 新进程运行 `WorkerProc.worker_main`，实例化 Worker（经历与 `UniprocExecutor` 相同的“init device”、“load model”等流程）。
5. 每个 Worker 判断自己是否为 driver（TP 组中的 rank 0）或普通 Worker。每个 Worker 设置两个队列：

    - `rpc_broadcast_mq`（与父进程共享）用于接收工作任务。
    - `worker_response_mq` 用于发送结果回父进程。

6. 初始化期间，每个子进程通过管道将其 `worker_response_mq` handle 发送给父进程。收到所有 handle 后，父进程解除阻塞——完成协调。
7. Worker 进入忙循环，阻塞于 `rpc_broadcast_mq.dequeue`。当有工作到来时执行任务（类似 `UniprocExecutor`，但现在是 TP/PP 分区的任务）。结果通过 `worker_response_mq.enqueue` 返回。
8. 运行时，当请求到来时，`MultiProcExecutor` 将其入队到所有子 Worker 的 `rpc_broadcast_mq`（非阻塞）。然后等待指定输出 rank 的 `worker_response_mq.dequeue` 收集最终结果。

从引擎的角度来看，一切接口不变——所有多进程复杂性都通过调用模型执行器的 `execute_model` 被抽象掉。

- 对于 `UniProcExecutor`：`execute_model` 直接调用 Worker 的 execute_model
- 对于 `MultiProcExecutor`：`execute_model` 间接通过 `rpc_broadcast_mq` 调用每个 Worker 的 execute_model

至此，我们可以使用同一个引擎接口运行尽可能大的模型。

下一步是横向扩展：启用数据并行（`DP > 1`），在各节点上复制模型，引入轻量级 DP 协调层，对副本进行负载均衡，并在前端部署一个或多个 API 服务器以处理入站流量。

## 分布式系统部署 vLLM

部署基础设施有多种方式，为了具体说明，这里给出一个示例：假设我们有两台 H100 节点，并希望在它们上运行四个 vLLM 引擎。

如果模型需要 `TP=4`，我们可以将节点配置如下：

![2 台 8xH100 节点的服务器配置](https://www.aleksagordic.com/blog/vllm/server_setup.png)

<div style="text-align: center;">
图 9. 2 台 8xH100 节点的服务器配置（1 台 headless，1 台 API 服务器）
</div>

在第一台节点上，以 headless 模式运行引擎（无 API 服务器），并使用以下参数：

```python
vllm serve <model-name>
  --tensor-parallel-size 4
  --data-parallel-size 4
  --data-parallel-size-local 2
  --data-parallel-start-rank 0
  --data-parallel-address <master-ip>
  --data-parallel-rpc-port 13345
  --headless
```

并在另一台节点上运行同样的命令，但进行以下调整：

- 去掉 `--headless`
- 修改 DP 起始 rank

```python
vllm serve <model-name>
  --tensor-parallel-size 4
  --data-parallel-size 4
  --data-parallel-size-local 2
  --data-parallel-start-rank 2
  --data-parallel-address <master-ip>
  --data-parallel-rpc-port 13345
```

!!! note

    这假设网络已配置好，所有节点都可以访问指定的 IP 和端口。

vLLM 中的实现方式：

## 在 headless 服务器节点

在 headless 节点上，`CoreEngineProcManager` 启动 2 个进程（根据 `--data-parallel-size-local`），每个进程运行 `EngineCoreProc.run_engine_core`。每个函数会创建一个 `DPEngineCoreProc`（引擎核心），然后进入其忙循环。

`DPEngineCoreProc` 初始化其父类 `EngineCoreProc`（`EngineCore` 的子类），具体流程如下：

1. 创建 `input_queue` 和 `output_queue`（`queue.Queue`）。
2. 使用 `DEALER` ZMQ socket（异步消息库）与另一节点的前端进行初始握手，并接收协调地址信息。
3. 初始化 DP 组（例如使用 NCCL 后端）。
4. 使用 `MultiProcExecutor` 初始化 `EngineCore`（如前所述，4 GPUs 的 TP=4）。
5. 创建 `ready_event`（`threading.Event`）。
6. 启动输入守护线程（`threading.Thread`）运行 `process_input_sockets(..., ready_event)`。同样启动输出线程。
7. 在主线程中等待 `ready_event`，直到所有 4 个进程的输入线程（跨 2 个节点）完成协调握手，最终执行 `ready_event.set()`。
8. 一旦解除阻塞，向前端发送 "ready" 消息，并附带元数据（例如分页 KV 缓存中可用的 `num_gpu_blocks`）。
9. 主线程、输入线程和输出线程进入各自的忙循环。

TL;DR：最终我们有 4 个子进程（每个 DP 副本一个），每个子进程运行主线程、输入线程和输出线程。它们与 DP 协调器和前端完成协调握手，然后每个进程的三条线程进入稳定的忙循环状态。

![分布式系统中运行 4 个 DPEngineCoreProc 的 4 个 DP 副本](https://www.aleksagordic.com/blog/vllm/dpenginecoreproc.png)

<div style="text-align: center;">
图 10. 分布式系统中运行 4 个 DP 副本的 4 个 DPEngineCoreProc
</div>

**当前稳定状态:** 

- **输入线程** — 阻塞在输入套接字，直到 API 服务器路由请求；收到请求后，解码有效载荷，通过 `input_queue.put_nowait(...)` 入队工作项，然后返回阻塞。
- **主线程** — 从 `input_queue.get(...)` 唤醒，将请求送入引擎；`MultiProcExecutor` 执行前向计算并将结果入队到 `output_queue`。
- **输出线程** — 从 `output_queue.get(...)` 唤醒，将结果发送回 API 服务器，然后继续阻塞。

**附加机制:** 

- **DP wave counter** — 系统跟踪 “waves”；当所有引擎空闲时，它们静止，当新工作到来时计数器递增（用于协调/指标）。
- **控制消息** — API 服务器可以发送不仅限于推理请求的消息（例如中止请求或其他 RPC）。
- **锁步的 Dummy 步骤** — 如果任何 DP 副本有工作，所有副本执行前向步骤；没有请求的副本执行 dummy 步骤以参与必要的同步点（避免阻塞活动副本）。

!!! tip

    锁步说明：实际上只有 MoE 模型需要，专家层组成 EP 或 TP 组，而 attention 层仍为 DP。目前 DP 总是这样执行——这是因为内置的非 MoE DP 用例有限，你可以直接运行多个独立 vLLM 并在它们之间做负载均衡。
    
接下来，我们来看第二部分：API 服务器节点会发生什么？

## 在 API 服务器节点

我们实例化一个 `AsyncLLM` 对象（LLM 引擎的 asyncio 包装器）。内部会创建一个 `DPLBAsyncMPClient`（数据并行、负载均衡、异步、多进程客户端）。

在 `MPClient` 的父类中，`launch_core_engines` 函数会执行：

1. 创建启动握手使用的 ZMQ 地址（如 headless 节点所见）。
2. 启动一个 `DPCoordinator` 进程。
3. 创建一个 `CoreEngineProcManager`（与 headless 节点相同）。

在 `AsyncMPClient`（`MPClient` 的子类）中，我们：

1. 创建 `outputs_queue`（`asyncio.Queue`）。
2. 创建一个 asyncio 任务 `process_outputs_socket`，通过输出 socket 与所有 4 个 `DPEngineCoreProc` 的输出线程通信，并将数据写入 `outputs_queue`。
3. 随后，`AsyncLLM` 创建另一个 asyncio 任务 `output_handler` 从队列读取数据，并最终发送到 `create_completion` 函数。

在 `DPAsyncMPClient` 中，我们创建 asyncio 任务 `run_engine_stats_update_task` 与 DP 协调器通信。

DP 协调器在前端（API 服务器）和后端（引擎核心）之间进行中介。它会：

- 定期向前端的 `run_engine_stats_update_task` 发送负载均衡信息（队列大小、等待/运行请求）。
- 处理前端的 `SCALE_ELASTIC_EP` 命令，通过动态调整引擎数量（仅 Ray 后端可用）。
- 向后端发送 `START_DP_WAVE` 事件（前端触发时），并报告波状态更新。

总结一下，前端（`AsyncLLM`）运行多个 asyncio 任务（注意：并发，而非并行）：

- 一类任务处理输入请求，通过 `generate` 路径（每个新客户端请求生成一个新的 asyncio 任务）。
- 两个任务（`process_outputs_socket`、`output_handler`）处理底层引擎的输出消息。
- 一个任务（`run_engine_stats_update_task`）与 DP 协调器保持通信：发送波触发、轮询负载均衡状态、处理动态扩缩容请求。

最后，主服务器进程创建 FastAPI 应用并挂载接口，例如 `OpenAIServingCompletion` 和 `OpenAIServingChat`，暴露 `/completion`、`/chat/completion` 等接口。整个栈通过 Uvicorn 提供服务。

将所有流程整合在一起，这就是完整的请求生命周期！

你可以从终端发送请求：

```bash
curl -X POST http://localhost:8000/v1/completions -H "Content-Type: application/json" -d '{
  "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
  "prompt": "The capital of France is",
  "max_tokens": 50,
  "temperature": 0.7
}'
```

接下来会发生什么：

1. 请求到达 API 服务器上 `OpenAIServingCompletion` 的 `create_completion` 路由。
2. 函数异步对 prompt 进行分词，并准备元数据（请求 ID、采样参数、时间戳等）。
3. 然后调用 `AsyncLLM.generate`，它遵循与同步引擎相同的流程，最终调用 `DPAsyncMPClient.add_request_async`。
4. 该方法会调用 `get_core_engine_for_request`，根据 DP 协调器的状态在多个引擎之间进行负载均衡（选择评分最低/负载最小的引擎：`score = len(waiting) * 4 + len(running)`）。
5. `ADD` 请求被发送到所选引擎的 `input_socket`。
6. 在该引擎上：
   
    - **输入线程** — 解阻塞，从输入 socket 解码数据，并将工作项放入主线程的 `input_queue`。
    - **主线程** — 从 `input_queue` 解阻塞，将请求添加到引擎，并重复调用 `engine_core.step()`，将中间结果放入 `output_queue`，直到满足停止条件。
    
        !!! tip

            提醒：`step()` 会调用调度器、模型执行器（可能是 `MultiProcExecutor`！）等。我们前面已经见过这些流程。

    - **输出线程** — 从 `output_queue` 解阻塞，并通过输出 socket 将结果发送回去。
7. 这些结果触发 `AsyncLLM` 的输出 asyncio 任务（`process_outputs_socket` 和 `output_handler`），将 Token 逐步返回到 FastAPI 的 `create_completion` 路由。
8. FastAPI 附加元数据（完成原因、logprobs、使用信息等），并通过 Uvicorn 返回一个 `JSONResponse` 到你的终端！

就这样，你的 completion 返回了——整个分布式机制被隐藏在一个简单的 `curl` 命令背后！:) 真是太有趣了！！！

!!! note "附加说明:"

    - 增加更多 API 服务器时，负载均衡在 OS/socket 层处理。应用层看起来几乎没有变化——复杂性被隐藏了。
    - 使用 Ray 作为 DP 后端时，可以暴露一个 URL 接口（`/scale_elastic_ep`）来自动上下扩缩引擎副本数量。

## 基准测试与自动调优 — 延迟 vs 吞吐量

到目前为止，我们一直在分析“燃料颗粒”——请求在引擎/系统中的内部流动。现在是时候放大视角，看整个系统，并思考：我们如何衡量推理系统的性能？

在最高层面，有两个相互竞争的指标：

1. **延迟（Latency）** — 从请求提交到 Token 返回所花费的时间  
2. **吞吐量（Throughput）** — 系统每秒能生成/处理的 Token 或请求数量

**延迟** 对于交互式应用最重要，因为用户在等待响应。  

**吞吐量** 对于离线工作负载最重要，例如用于训练前/后数据生成、数据清理/处理，以及一般的离线批量推理任务。

在解释为什么延迟与吞吐量相互竞争之前，我们先定义几个常见的推理指标：

| 指标 | 定义 |
| :----------------------------------- | :----------------------------------------------------------- |
| `TTFT` (time to first token) | 从请求提交到接收到第一个输出 Token 的时间 |
| `ITL` (inter-token latency) | 两个连续 Token 之间的时间（例如，从 Token i-1 到 Token i） |
| `TPOT` (time per output token) | 单个请求中所有输出 Token 的平均 ITL |
| `Latency / E2E` (端到端延迟) | 处理请求的总时间，即 TTFT + 所有 ITL 之和，或等价地，从提交请求到接收最后一个输出 Token 的时间 |
| `Throughput` | 系统每秒处理的总 Token（输入、输出或两者），或每秒请求数 |
| `Goodput` | 满足服务级别目标（SLO，如最大 TTFT、TPOT 或端到端延迟）的吞吐量。例如，只有满足这些 SLO 的请求 Token 才计入吞吐量 |

![ttft, itl, e2e latency](https://www.aleksagordic.com/blog/vllm/latency_diagram.png)

<div style="text-align: center;">
图 11. TTFT、ITL 与端到端延迟
</div>

下面是一个简化模型，用于说明这两个指标的竞争关系。

!!! tip

    假设：权重 I/O 主导性能，而不是 KV-cache I/O；即处理的是短序列。

当观察批大小 `B` 对单步解码的影响时，这种权衡就很清晰了：  
- 当 `B ↓` 接近 1 时，ITL 降低：每步工作量减少，Token 之间不会相互“竞争”。  
- 当 `B ↑` 趋近于无穷大时，ITL 上升，因为每步计算更多 FLOPs —— 但吞吐量提高（直到达到峰值性能），因为权重 I/O 被更多 Token 分摊。

屋顶线（roofline）模型有助于理解：  
- 在饱和批量 `B_sat` 以下，步骤时间受 HBM 带宽主导（权重按层流入片上内存），所以步骤延迟几乎平稳 —— 计算 1 个 Token 与 10 个 Token 所需时间相似。  
- 超过 `B_sat` 后，kernel 受计算限制，步骤时间大致随 `B` 增长，每增加一个 Token 都会增加 ITL。

![roofline perf model](https://www.aleksagordic.com/blog/vllm/roofline.png)

<div style="text-align: center;">
图 12. 屋顶线性能模型
</div>

!!! note

    更严格的分析需要考虑 kernel 自动调优：随着 `B` 增大，运行时可能为该形状切换到更高效的 kernel，从而改变实际性能 `P_kernel`。步骤延迟为 `t = FLOPs_step / P_kernel`，其中 `FLOPs_step` 为该步的计算量。可以看到，当 `P_kernel` 达到 `P_peak` 时，每步更多的计算量会直接导致延迟增加。

## 如何在 vLLM 中进行基准测试

vLLM 提供了一个 CLI 命令 `vllm bench {serve,latency,throughput}`，它封装了 `vllm/benchmarks/{server,latency,throughput}.py` 脚本。

这些脚本的作用如下：

- **latency（延迟）** — 使用较短的输入（默认 32 个 Token），生成 128 个输出 Token，使用小批量（默认 8）。脚本会执行多次迭代，并报告批量的端到端延迟。
- **throughput（吞吐量）** — 同时提交固定集合的 prompts（默认 1000 个 ShareGPT 样本，即 `QPS=Inf` 模式），报告整个运行期间的输入/输出/总 Token 数和每秒请求数。
- **serve（服务模拟）** — 启动一个 vLLM 服务，并模拟真实工作负载。请求的到达间隔时间遵循 Poisson 分布（或更通用的 Gamma 分布）。脚本在时间窗口内发送请求，测量前文提到的所有指标，并可选择通过信号量限制服务器最大并发数（例如限制为 64 个并发请求）。

下面是运行延迟测试脚本的示例：

```bash
vllm bench latency
  --model <model-name>
  --input-tokens 32
  --output-tokens 128
  --batch-size 8
```

!!! tip

    用于 CI 的基准测试配置存放在 `.buildkite/nightly-benchmarks/tests` 目录下。

此外，还有一个自动调优脚本，会驱动 `serve` 基准测试来寻找满足目标 SLO（例如 “在保持 p99 e2e < 500 ms 的前提下最大化吞吐量”）的参数设置，并返回建议的配置。

## 尾声

我们从基础引擎核心（`UniprocExecutor`）开始，加入了如推测解码（speculative decoding）和前缀缓存（prefix caching）等高级特性，接着扩展到 `MultiProcExecutor`（TP/PP > 1），最终实现水平扩展，将所有组件封装到异步引擎和分布式服务栈中——最后展示了如何衡量系统性能。

vLLM 还包含一些我未详细展开的专门处理，例如：

- **多样化硬件后端:** TPU、AWS Neuron（Trainium/Inferentia）等
- **架构/技术:** `MLA`、`MoE`、编码器/解码器（如 Whisper）、池化/嵌入式模型、`EPLB`、`m-RoPE`、`LoRA`、`ALiBi`、无注意力变体、滑动窗口注意力、多模态 LLM、状态空间模型（如 Mamba/Mamba-2、Jamba）
- **TP/PP/SP**
- **混合 KV-cache 逻辑**（Jenga）、更复杂的采样方法如束式采样等
- **实验性功能:** 异步调度

好的一点是，这些大多数功能与上文描述的核心流程是正交的——几乎可以把它们当作“插件”来理解（当然实际中有部分耦合）。

我热爱理解系统。话虽如此，在这个高度概览中，细节有所损失。在后续文章中，我会聚焦具体子系统，深入探讨细节。

!!! tip "💡联系我："

    如果你在本文中发现任何错误，请随时联系我——可以通过 [X](https://x.com/gordic_aleksa) 或 [LinkedIn](https://www.linkedin.com/in/aleksagordic/) 给我留言，也可以通过 [匿名反馈](https://docs.google.com/forms/d/1z1fEirrN2xtGxAsJvptpM7yV4ByT5SF25S-XiMPrXNA/edit) 提交。

## 致谢

衷心感谢 [Hyperstack](https://www.hyperstack.cloud/) 在过去一年中提供 H100 GPU 供我进行实验！

感谢 [Nick Hill](https://www.linkedin.com/in/nickhillprofile/)（vLLM 核心贡献者，RedHat）、[Mark Saroufim](https://x.com/marksaroufim)（PyTorch）、[Kyle Krannen](https://www.linkedin.com/in/kyle-kranen/)（NVIDIA, Dynamo）以及 [Ashish Vaswani](https://www.linkedin.com/in/ashish-vaswani-99892181/) 在博客预发布版本中提供反馈！

## 参考文献

1. [vLLM](https://github.com/vllm-project/vllm)
2. ["Attention Is All You Need"](https://arxiv.org/abs/1706.03762)
3. ["Efficient Memory Management for Large Language Model Serving with PagedAttention"](https://arxiv.org/abs/2309.06180)
4. ["DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model"](https://arxiv.org/abs/2405.04434)
5. ["Jenga: Effective Memory Management for Serving LLM with Heterogeneity"](https://arxiv.org/abs/2503.18292)
6. ["Orca: A Distributed Serving System for Transformer-Based Generative Models"](https://www.usenix.org/conference/osdi22/presentation/yu)
7. ["XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models"](https://arxiv.org/abs/2411.15100)
8. ["Accelerating Large Language Model Decoding with Speculative Sampling"](https://arxiv.org/abs/2302.01318)
9. ["EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty"](https://arxiv.org/abs/2401.15077)
10. ["Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads"](https://arxiv.org/abs/2401.10774)
11. [LMCache](https://github.com/LMCache/LMCache)
