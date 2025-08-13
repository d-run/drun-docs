# CUDA Core Dump：调试内存访问问题的有效工具

> 英文原稿转载自 [blog.vllm.ai](https://blog.vllm.ai/2025/08/11/cuda-debugging.html)

你是否曾经在开发 CUDA kernel 时，测试经常遇到非法内存访问（简称 IMA），却不知道该如何调试？在开发 vLLM（一个高性能的 LLM 推理引擎）时，我们一次又一次地体会到了这种痛苦。

如果你是曾经遇到过此类问题的开发者，那么这篇博客就是为你准备的！我们将揭示一些在 vLLM 中用于调试复杂问题（如 IMA）的高级调试技巧。

例如，这是一个来自 PyTorch 的错误信息：

```text
RuntimeError: CUDA error: an illegal memory access was encountered
CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1
Compile with `TORCH_USE_CUDA_DSA` to enable device-side assertions.
```

棘手之处在于：CUDA kernel 错误可能在其他 API 调用中被异步报告，因此下面的堆栈跟踪可能是错误的。根据我们的经验，这类异常的 Python 堆栈跟踪基本 **总是错误的，几乎没什么用** 。为了解决这个问题，错误信息建议在运行代码时添加 `CUDA_LAUNCH_BLOCKING=1`。然而，这里仍然有两个问题：

1. 很多人使用 `kernel<<<>>>` 语法启动 CUDA kernel 时，并不会检查 kernel 启动状态，例如[这段代码](https://github.com/pytorch/pytorch/blob/5e320eea665f773b78f6d3bfdbb1898b8e09e051/aten/src/ATen/native/cuda/SortStable.cu#L117)。在这种情况下，即便加了 `CUDA_LAUNCH_BLOCKING=1`，依然无法定位到出错的 kernel。
2. 如果非法内存访问发生在 CUDA graph 中的某个 kernel 内，即使加了 `CUDA_LAUNCH_BLOCKING=1`，我们也只能看到在启动 CUDA graph 时出现了问题，依然无法精准定位到出错的具体 kernel。

要精确定位这类问题，我们需要在非法内存访问发生的那一刻立刻做出响应。当然，这不是用户直接能做到的——它必须由 CUDA 驱动本身提供支持。

[CUDA core dump 功能](https://docs.nvidia.com/cuda/cuda-gdb/index.html#gpu-core-dump-support)正是为此设计的。它允许 CUDA 驱动在发生非法内存访问时转储 GPU 状态，用户之后可以分析该状态，从而找出是哪个 kernel 引发了问题，以及具体的非法访问是什么。

## 什么是 Core Dump？

GPU 本质上是一个高度并行的处理器，其中的许多概念在 CPU 上都有对应。

[Core dump](https://en.wikipedia.org/wiki/Core_dump) 是由 CPU 与操作系统共同提供的功能。当程序在执行过程中崩溃时，操作系统可以记录程序的内存数据、运行状态等信息，以便后续分析与调试。程序崩溃是一个硬件级概念，当 CPU 在执行某条指令时遇到错误，会进入 `trap` 状态，此时操作系统接管程序并执行相应的异常处理过程（默认情况下，这会直接终止程序，但也可以配置生成 core dump 以便分析。例如，通过 `ulimit -c 1` 可启用 core dump 生成，通过 `echo "core.%e.%p" > /proc/sys/kernel/core_pattern` 可指定 core dump 文件路径）。

类似地，GPU 上的 core dump 功能需要 GPU 硬件与 GPU 驱动的协作。当 GPU 上的某个线程在执行中崩溃时，GPU 硬件需要触发异常并将其传递给 GPU 驱动，由驱动立即处理该异常。然而，据[论坛讨论](https://forums.developer.nvidia.com/t/difference-in-error-handling-between-driver-api-and-runtime-api/336389)所述，GPU 驱动在处理异常时的默认行为是将当前 CUDA 上下文标记为不可用，而不是终止程序。

## 如何启用 CUDA Core Dump

启用 CUDA core dump 非常简单，只需设置 `CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1` 环境变量即可。不过，为了更顺畅的使用体验，你还应额外设置几个环境变量：

1. 默认情况下，CUDA core dump 会将转储文件保存在当前目录，并且不会输出文件路径。你可以启用 `CUDA_COREDUMP_SHOW_PROGRESS=1` 环境变量来显示 core dump 过程的进度与细节。最重要的是，它会在过程结束后显示 core dump 文件的路径，方便后续调试与分析。
2. 许多任务运行在容器内，当任务失败时，容器会被销毁，从而无法保留 core dump 文件。在这种情况下，你可以通过 `CUDA_COREDUMP_FILE` 环境变量指定 core dump 文件的路径模板。例如，可以将其保存到持久化存储目录：`CUDA_COREDUMP_FILE="/persistent_dir/cuda_coredump_%h.%p.%t"`，其中 `%h` 表示主机名，`%p` 表示进程 ID，`%t` 表示转储时间戳。
3. 默认情况下，core dump 会保存整个 GPU 上下文。对于像大模型推理这样几乎占满 GPU 显存的程序来说，完整 core dump 会非常庞大（数百 GiB 数据）。你可以通过设置 `CUDA_COREDUMP_GENERATION_FLAGS='skip_nonrelocated_elf_images,skip_global_memory,skip_shared_memory,skip_local_memory'` 跳过保存 GPU 显存、共享内存和本地内存，从而大幅减小 core dump 文件体积。

文档中还提到，将 `skip_abort` 添加到 `CUDA_COREDUMP_GENERATION_FLAGS` 中，可以在 core dump 完成后防止 CPU 进程中止，这样 CPU 进程可以记录自己的错误堆栈，提供更多调试信息。但实验表明，这个功能存在一个严重[缺陷](https://forums.developer.nvidia.com/t/cuda-core-dump-with-skip-abort-will-ignore-an-illegal-memory-access-error/341802/3)，可能导致 GPU 上的非法内存访问错误被忽略。此时，后续代码可能继续运行，但程序的内存数据已经被破坏。对于训练任务来说，这是完全不可接受的；对于推理任务，也是不安全的。因此，这个功能并不可靠，不推荐使用。

另外，文档称启用 `CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1` 不仅会启用 CUDA core dump，还会默认生成 CPU core dump。但实际上，我们发现 CPU core dump 中几乎没有有用信息，而且难以分析。

如果你想进行实时调试，也可以启用 `CUDA_DEVICE_WAITS_ON_EXCEPTION=1` 环境变量。它不会使用 core dump，而是在异常发生时立刻暂停 GPU 执行，并挂起等待用户附加调试器（如 cuda-gdb）检查 GPU 状态，此时完整的 GPU 内存仍然保留。不过，这种方式自动化程度较低，需要更多人工干预。

总结来说，推荐使用以下组合环境变量启用 CUDA core dump：

```
CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1 CUDA_COREDUMP_SHOW_PROGRESS=1 CUDA_COREDUMP_GENERATION_FLAGS='skip_nonrelocated_elf_images,skip_global_memory,skip_shared_memory,skip_local_memory' CUDA_COREDUMP_FILE="/persistent_dir/cuda_coredump_%h.%p.%t"
```

## 使用 CUDA Core Dump 的示例

### 调试不当的 Kernel 启动

```cpp
// test.cu
#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>

// CUDA 错误检测宏
#define cuda_check(call) do { \
    cudaError_t err = call; \
    if (err != cudaSuccess) { \
        printf("CUDA Error at %s:%d - %s: %s\n", __FILE__, __LINE__, #call, cudaGetErrorString(err)); \
        exit(EXIT_FAILURE); \
    } \
} while(0)

// 具有非法内存访问的 Kernel — 访问越界
__global__ void illegalMemoryAccessKernel(int* data, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // 这会导致非法内存访问 — 访问超分配范围
    // 我们分配了 'size' 元素，却访问到 size * 2
    if (idx < size * 2) {  // 访问两倍长度区域
        data[idx - 1000000000] = idx;   // 对 idx == 0 时将引发越界访问
    }
}

// 正常的 Kernel — 访问安全
__global__ void normalKernel(int* data, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx < size) {
        data[idx] = idx;
    }
}

int main() {
    printf("CUDA Illegal Memory Access Test\n");
    printf("===============================\n\n");

    int size = 100;
    int* h_data = (int*)malloc(size * sizeof(int));
    int* d_data;

    // 初始化主机内存
    for (int i = 0; i < size; i++) {
        h_data[i] = 0;
    }

    // 分配设备内存
    cuda_check(cudaMalloc(&d_data, (unsigned long long)(size) * sizeof(int)));
    cuda_check(cudaMemcpy(d_data, h_data, size * sizeof(int), cudaMemcpyHostToDevice));

    // 启动具有非法访问的 kernel
    int blockSize = 256;
    int numBlocks = (size + blockSize - 1) / blockSize;

    printf("Launching kernel with out-of-bounds access...\n");
    illegalMemoryAccessKernel<<<numBlocks, blockSize>>>(d_data, size);

    normalKernel<<<numBlocks, blockSize>>>(d_data, size);

    cuda_check(cudaMemcpy(h_data, d_data, size * sizeof(int), cudaMemcpyDeviceToHost));
    for (int i = 0; i < 5; i++) {
        printf("%d ", h_data[i]);
    }
    printf("\n");

    // 同步以捕捉运行时错误
    cuda_check(cudaDeviceSynchronize());

    printf("Test completed.\n");

    // 清理
    cuda_check(cudaFree(d_data));
    free(h_data);

    return 0;
}
```

这段代码顺序启动两个 kernel（`illegalMemoryAccessKernel` 和 `normalKernel`）。正常运行时，你会看到类似这样的错误提示：

```
CUDA Error at test.cu:62 - cudaMemcpy(h_data, d_data, size * sizeof(int), cudaMemcpyDeviceToHost): an illegal memory access was encountered
```

错误只会在 `cudaMemcpy` 返回值中检测到。即使设置了 `CUDA_LAUNCH_BLOCKING=1`，仍然无法识别是哪一个 kernel 出错。

通过添加 CUDA core dump 相关环境变量，可以观察到如下信息：

```
[00:40:46.606413] coredump: SM 123/132 has finished state collection
[00:40:46.606419] coredump: SM 124/132 has finished state collection
[00:40:46.611453] coredump: Detected an exception of type CUDBG_EXCEPTION_WARP_ILLEGAL_ADDRESS (14)
[00:40:46.611458] coredump:   - Device: 0
[00:40:46.611460] coredump:   - SM: 124
[00:40:46.611462] coredump:   - Warp: exception was detected after the warp has exited
[00:40:46.611465] coredump:   - PC 0x7f31abb9f6d0
[00:40:46.611467] coredump: SM 125/132 has finished state collection

[00:40:46.806153] coredump: Writing ELF file to /tmp/cuda_coredump_xxx.1799919.1754898045

[1]    1799919 IOT instruction (core dumped)  CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1 CUDA_COREDUMP_SHOW_PROGRESS=1 = = ./test3
```

当 GPU 线程触发非法内存访问时，CPU 立即生成 core dump 文件并触发 CPU 异常，直接终止程序。这时我们获得了 core dump 文件 `/tmp/cuda_coredump_xxx.1799919.1754898045`。可以使用 `cuda-gdb` 打开它：

```bash
$ cuda-gdb
(cuda-gdb) target cudacore /tmp/cuda_coredump_xxx.1799919.1754898045
Opening GPU coredump: /tmp/cuda_coredump_xxx.1799919.1754898045

CUDA Exception: Warp Illegal Address
The exception was triggered at PC 0x7f31abb9f6d0  illegalMemoryAccessKernel(int*, int)
[Current focus set to CUDA kernel 0, grid 1, block (0,0,0), thread (0,0,0), device 0, sm 124, warp 0, lane 0]
#0  0x00007f31abb9f6e0 in illegalMemoryAccessKernel(int*, int)<<<(1,1,1),(256,1,1)>>> ()
```

我们可以清晰看到，异常由 `illegalMemoryAccessKernel` 引发，定位在 kernel 0、grid 1、block (0,0,0)、thread (0,0,0)、device 0、sm 124、warp 0、lane 0。

### 调试 CUDA Graph 中的 Kernel 异常

以下是一个更复杂的例子：在 CUDA graph 中插入一个非法访问 kernel：

```python
# core_dump.py
import torch
import torch.nn as nn

from dataclasses import dataclass

@dataclass
class CupyWrapper:
    data_ptr: int
    size_in_bytes: int

    @property
    def __cuda_array_interface__(self):
        return {
            "shape": (self.size_in_bytes,),
            "typestr": '|u1',
            "data": (self.data_ptr, False),
            "version": 3,
        }

def from_buffer(data_ptr: int, size_in_bytes: int) -> torch.Tensor:
    out = torch.as_tensor(CupyWrapper(data_ptr, size_in_bytes))
    assert data_ptr == out.data_ptr(), "not zero-copy convert, something must be wrong!"
    return out


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        # 第 1 层: [B, 10] -> [B, 20] + ReLU 激活
        self.layer1 = nn.Linear(10, 20)
        self.relu = nn.ReLU()
        # 第 2 层: [B, 20] -> [B, 30]
        self.layer2 = nn.Linear(20, 30)
        self.num_called = 0

    def forward(self, x):
        # 输入形状: [B,10]
        x = self.layer1(x)
        x = self.relu(x)
        self.num_called += 1
        if self.num_called > 1:
            y = from_buffer(x.data_ptr(), x.numel() * 1024 * 1024)
            # 会触发非法内存访问
            y.fill_(1)
        x = self.layer2(x)
        return x


# 使用示例
if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    model = NeuralNetwork().to(device)
    batch_size = 4
    input_tensor = torch.randn(batch_size, 10).to(device)

    print(f"Input shape: {input_tensor.shape}")
    print(f"Input device: {input_tensor.device}")

    with torch.no_grad():
        output = model(input_tensor)  # 先 warmup
        g = torch.cuda.CUDAGraph()
        with torch.cuda.graph(g):
            output = model(input_tensor)  # 捕获 graph
        g.replay()  # 重放 graph

    print(f"Output shape: {output.shape}")
    print(f"Output device: {output.device}")
    print(f"Output: {output.sum()}")

    print("\nModel architecture:")
    print(model)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"\nTotal parameters: {total_params}")
    print(f"Model device: {next(model.parameters()).device}")
```

直接执行会报如下错误：

```text
Using device: cuda
Input shape: torch.Size([4, 10])
Input device: cuda:0
Output shape: torch.Size([4, 30])
Output device: cuda:0
Traceback (most recent call last):
  File "core_dump.py", line 76, in <module>
    print(f"Output: {output.sum()}")
RuntimeError: CUDA error: an illegal memory access was encountered
...
```

输出在 `output.sum()` 时才触发，因为此处进行了设备同步，但我们仍不知道哪个 kernel 触发了 IMA。

添加 `CUDA_LAUNCH_BLOCKING=1` 后，错误信息变为：

```text
...  
File "core_dump.py", line 71, in <module>
    g.replay()
RuntimeError: CUDA error: an illegal memory access was encountered
...
```

这让我们推断异常发生在 CUDA graph 内的某个 kernel，但仍无法得知具体是哪一个。

再加上 core dump 的环境变量组合，我们就可以轻松定位：

```text
(cuda-gdb) target cudacore /tmp/cuda_coredump_flow-matic.1929094.1754901120
Opening GPU coredump: /tmp/cuda_coredump_flow-matic.1929094.1754901120

CUDA Exception: Warp Illegal Address
The exception was triggered at PC 0x7fc2afba5e30  void at::native::vectorized_elementwise_kernel<4, at::native::FillFunctor<unsigned char>, std::array<char*, 1ul> >(int, at::native::FillFunctor<unsigned char>, std::array<char*, 1ul>)
[Current focus set to CUDA kernel 0, grid 9, block (17454,0,0), thread (0,0,0), device 0, sm 0, warp 1, lane 0]
#0  0x00007fc2afba5e70 in void at::native::vectorized_elementwise_kernel<4, at::native::FillFunctor<unsigned char>, std::array<char*, 1ul> >(int, at::native::FillFunctor<unsigned char>, std::array<char*, 1ul>)<<<(40960,1,1),(128,1,1)>>> ()
```

很明显，这是一段 `fill` 函数，grid size 达到 `40960`，说明 `y = from_buffer(x.data_ptr(), x.numel() * 1024 * 1024); y.fill_(1);` 无视了 x 的真实长度，扩大了 1 百万倍然后填充，因而触发了 IMA 异常。

在部分 GPU 上，这一行可能报 `invalid argument` 而非 IMA，因为 grid size 超出最大限制。在此情况下，CUDA core dump 不会被触发，需要将扩容比例（`1024 * 1024`）适当调低，以免超过限制。

## 限制与注意事项

1. 理论上，CUDA core dump 应能捕获 GPU 某个线程引发的各种异常。但实际上，在某些 GPU 和驱动版本上，诸如“在全局/共享地址空间执行操作不支持”等异常可能无法触发 core dump。幸运的是， **非法内存访问** 通常能可靠触发 core dump，满足大多数调试需求。
2. 对于硬件相关错误（如“通过 nvlink 非法访问跨 GPU 的内存”或硬件故障），这些并非由具体线程引发，无法归因某个 GPU 线程，不会触发 core dump。
3. 通过 driver API 使用不当造成的错误属于[非粘性错误](https://forums.developer.nvidia.com/t/difference-in-error-handling-between-driver-api-and-runtime-api/336389)，与 GPU 本身无关，会在 driver API 层面报告，同样不会触发 core dump。例如 `cudaMalloc` 时显存不足，不会生成 core dump。
4. 在涉及多 GPU 通信的分布式程序中，通常会通过映射将其他 GPU 的内存映射到当前 GPU。如果另一个 GPU 上的程序退出，映射就失效，再访问它会触发 IMA，但这属于分布式关机期间的特定现象，不属于典型 IMA 问题。使用 core dump 时要区分这种“假阳性”。
5. 启用 CUDA core dump 会对 CUDA kernel 性能有轻微影响（因为每个线程退出时需要检查错误并记录信息），因此不建议在生产环境开启。建议仅在可靠复现 IMA 错误以进行调试时使用。

## 总结

本文解析了 CUDA core dump 的原理与使用场景。这种调试方式对定位不正确的 kernel 启动与 CUDA graph 内的 kernel 异常特别有效，是调试 `illegal memory access` 及更多问题的强大工具。

例如，我们近期在 vLLM 中使用此技术调试了一个复杂的 IMA 问题（详见 [相关 PR](https://github.com/vllm-project/vllm/pull/22593)）。基本情况是，我们为 MRope 添加了一个 triton kernel，但该 kernel 隐含假设 `head_size == rotary_dim`（即完整 Rope）。当 `head_size != rotary_dim`（部分 Rope）时，该 kernel 会触发 IMA，这在新 GLM-4.5V 模型中发生。若无 CUDA core dump，错误被误报为 `Failed: Cuda error /workspace/csrc/custom_all_reduce.cuh:453 'an illegal memory access was encountered'`，极具误导性。利用 core dump，我们轻松定位问题至 MRope kernel 并修复。请注意，对于更复杂的 IMA 问题，我们仍需以最小可复现示例隔离 kernel，然后结合如 [Compute Sanitizer](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html#memcheck-tool) 的专用工具进一步调查。

vLLM 项目旨在为所有人提供简单、高效、低成本的 LLM 推理服务，而易于调试也是重要组成部分。我们将持续分享更多调试技巧与方法，共同构建强大的 LLM 推理生态。如你有 vLLM 使用或调试经验，欢迎提交 PR 分享（地址在[博客仓库](https://github.com/vllm-project/vllm-project.github.io)）。

## 致谢

感谢 Ze Long、Vikram Sharma Mailthody、Jeremy Iverson、Sandarbh Jain（来自 NVIDIA）给予的有益讨论。感谢 Red Hat 的 Lucas Wilkinson 帮助润色初稿。
