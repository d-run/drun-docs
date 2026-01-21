# llm-d as the Agentic Runtime Northstar

## Scope

This Northstar defines the architectural evolution of llm-d from a generic, **request-centric** inference engine to a specialized **agentic-runtime**, in the framework’s shift towards **workload-aware inference**.

We assert that the next order of magnitude in efficiency will not come from micro-optimizing isolated requests, but from orchestrating stateful workloads.

This document serves as the umbrella for the agentic workload in the evolution of inference, defining fundamental principles and technical execution pillars. It serves as the strategic bridge between our engineering roadmaps and the emerging needs of the agentic ecosystem.

**The "Use-Case First" Principle:** We reject abstract optimization in favor of **Workload-Derived Engineering**. Every architectural pillar proposed here is a direct response to a specific "friction point" observed in canonical agentic patterns.

By anchoring our roadmap to these behaviors, we ensure llm-d solves the actual bottlenecks of production agents - Cost, Latency, and State Management - rather than merely chasing raw token throughput.

## Motivation: The Agentic Tax

State-of-The-Art inference frameworks have perfected the art of the **Isolated Request**. We have optimized TTFT (Time to First Token) and TPOT (Time Per Output Token) by treating the KV-cache as a managed memory layer. However, the industry is shifting from simple chat interactions to **Agentic Workflows** (e.g., Tree-of-Thought, LLM-as-a-Judge swarms, multi-step tool-use).

In these workflows, an inference request is rarely coincidential; it is part of a **program**.

- **The State Overlap:** Agentic workflows exhibit massive KV-cache prefix overlaps across "branches" of reasoning.

- **The Scheduling Blindness:** Current schedulers optimize for request-level fairness, but agentic programs care about **Program Completion Time**. A delay in one "thought" branch can stall the entire agentic loop.

To reach the next order of magnitude in efficiency, the inference stack must understand the *intent* and *structure* of the agentic program. We need to bridge the gap where the application provides hints and context taints, and llm-d provides the context-aware infrastructure & integrations to execute them.

## Gaps: Why SOTA Inference is not yet Agent-Native

Despite llm-d nailing the fundamentals of generic KV-cache centric inference, several gaps prevent us from evolving to an agentic runtime:

1. **Metric Misalignment:** We optimize for request-level latencies. Agents require **Total Program Latency** and **Throughput of Completed Tasks**. Current stacks don't know which requests belong to the same "task".
1. **Reactive vs. Proactive State:** Our KV-cache management is largely reactive (load on demand). Agents are predictable; if a "Plan" step is finished, we know the "Execute" steps are coming. We lack the APIs to **proactively orchestrate** KV-cache across the cluster throughout and in-between programs.
1. **Context Indifference:** The inference stack treats all KV-cache blocks as equal. In an agentic flow, a "System Prompt" or "Tool Definition" is high-value/long-lived (Static Context), while a "Chain of Thought" scratchpad might be transient (Ephemeral Context). We lack the **Context Taints** to apply different eviction and offloading policies based on the *type* of data.
1. **The "Tax" of Disaggregation:** While KV-disaggregation allows us to scale, the physical distance between compute and the KV-cache can introduce latency that agentic loops (which require many sequential calls) are highly sensitive to.

## The Vision: A Context-Aware Inference Ecosystem

Our northstar is to transform llm-d into a system where the **KV-cache is the primary medium of coordination**.

Instead of treating the inference stack as a black box that receives text, we envision an ecosystem where the **Inference Runtime understands the Agentic Program**.

This vision rests on three fundamental principles and five architectural pillars:

- **Frameworks provide Hints:** The agentic layer "taints" requests with program IDs, priority hints, and context lifetimes.
- **llm-d manages the Lifecycle:** The inference stack uses these hints to make intelligent decisions about where to store KV-cache, when to move it, and which branches of a program to prioritize in the scheduler.

    This calls for explicit awareness of agentic workflow elements, and a level of association of such information with KV-cache.

- **The Stack is Global:** KV-cache is no longer bound to a session or a node; it is a global, addressable resource that guides and follows the agent's logic across the cluster.

## The 5 Pillars of Execution (PEs)

### I. The Program-Aware Scheduler

We elevate the scheduler from managing "queues of requests" to managing **Program Execution Graphs**. The scheduler requires **structural awareness** and understands the agent's dependency structure (e.g., "This is a blocking step", "These 10 branches can run in parallel"). The system identifies critical paths in the agent's logic and allocates resources to clear bottlenecks that would otherwise stall the entire workflow.

### II. Proactive State Management

We invert the data flow: instead of pinning requests to where state resides (Affinity), **we move state to where compute is available** (Mobility). By leveraging P2P NIXL and shared storage, the KV-cache becomes a unified, fluid pool.

This pillar extends the control plane with KV-cache APIs such as “Move (to tier)”, “Pin (in tier)” and “Evict (from tier)”, and the logic for proactive orchestration.

### III. The Semantic KV-Cache

We evolve the KV-cache from a raw tensor dump into a **Typed Data Structure** **capturing workload semantics & taints**. Just as code has types, Agentic State has types: `SystemPrompt`, `ToolDefinition`, `ReasoningBranch`, `ExecutionCheckpoint`.

By associating semantic metadata with cache blocks, the engine can apply distinct policies such as "Always Replicate `ToolDefinitions`", and "Never Offload `Checkpoints`". This pillar extends the control plane with KV-cache tainting APIs, and the data-structures that capture semantic associations.

### IV. Context-Aware KV-Caching Policies

We replace naive LRU eviction with **Explicit Lifecycle Management**. The agentic framework uses APIs to "taint" context blocks - pinning high-value "Skills" while marking intermediate "Thoughts" for early eviction - giving the runtime explicit control over memory.

### V. Workload-Driven Benchmarking & Simulation

We establish a continuous feedback loop between real agentic patterns and infrastructure evolution. Instead of optimizing against synthetic token throughput, **we build/reuse canonical workload simulators** that capture the three core use cases and measure what matters: program completion time, zero-recompute hit rates, and effective cache utilization across semantic context types.

The simulation framework exposes configurable parameters for prefix overlap ratios, branching factors, tool invocation frequencies, and delegation depths, enabling benchmark-driven development where **every optimization is validated** against actual friction points observed in production agentic workflows.

## Use-Case Driven Agenda

We focus on three canonical patterns that define the next generation of AI applications to guide our development.

### Use Case 1: Tree-of-Thought / Branching Exploration

**Pattern**: Generate N parallel reasoning paths from shared context, evaluate them, optionally expand best candidates.

**Example**: Code generation exploring 8 implementation approaches from same problem description, evaluating each, expanding top 2.

**Key Characteristics**:

- Large shared prefix (30-100k tokens) across all branches
- Branches diverge at specific points but share majority of context
- Parallel execution, but results needed together before next step
- Branch-specific context is transient, shared context is stable

**Note: this use-case is valuable for RL.**

### Use Case 2: Multi-Turn Tool Use / ReAct Loops

**Pattern**: Agent iteratively reasons → calls tool → processes result → reasons again. Each turn builds on previous context with predictable structure.

**Example**: Data analysis: Load dataset → describe_statistics → reason about outliers → plot_distribution → synthesize findings.

**Key Characteristics**:

- Sequential dependency: turn N+1 requires context from turn N
- High context reuse: tool definitions repeated every turn (10-30k tokens)
- Predictable patterns: tool call → likely another reasoning turn coming
- Mixed lifecycle: tool defs are durable, intermediate thoughts are ephemeral

### Use Case 3: Hierarchical Agent Swarms / Delegation

**Pattern**: Parent agent spawns N child agents with shared instructions/data but independent working memory. Children complete, parent aggregates.

**Example**: Essay grading: supervisor spawns 50 graders, each evaluates 1 essay against shared rubric (30k tokens), returns score for aggregation.

**Key Characteristics**:

- Massive context overlap: N children share 90-95% of parent's context
- Batch semantics: completion time = slowest child
- Hierarchical structure: children → parent flow with result aggregation
- Two-phase execution: parallel children, then supervisor synthesis

### Use Case 4: Workflow Spanning Multiple Agents

**Pattern:** The agentic program is a workflow involving multiple agents offering different functionality. These agents could be connected in sequence, in parallel or with fork/join constructs.

**Example**: Investment Analysis agentic program: A Researcher agent --> Financial Analyst agent --> Investment Recommendation agent. 

**Key Characteristics:**

- Workload identity: Spans across multiple agents
- KV Cache reuse: Generated content by an agent becomes context for downstream agents
- Execution dependency: every agent requires output and/or context from one or more previous agents
- Program level optimization: latency and memory performance is measured across agents

## Goals

- **Goal 1: Program-Centric Optimization (Beyond TTFT)** Transition from optimizing isolated requests to optimizing the execution of entire **Agentic Programs**. Success means minimizing the "end-to-end" latency of a multi-turn workflow (e.g., MCTS, Reflection), and increasing **task throughput**.

- **Goal 2: Cluster-Wide "Zero-Recompute"** Establish a "Write Once, Read Anywhere" invariant. If a semantic block (e.g., a 100k context document or a Tool Definition) exists *anywhere* in the cluster (GPU, CPU, or Storage), no other node should burn compute to regenerate it - regardless of which node holds it or where it sits in the prompt sequence.

    KV-disagg roadmap alignment:

    - **Shared Storage Offloading** - Enabling cluster-wide KV cache sharing through the utilization of an intermediate shared storage medium as a KV memory tier.
    - **P2P KVConnector (NIXL)** - Enabling direct Engine-to-Engine KV memory transfer across tiers (GPU, CPU, Storage) to bypass re-computation.
    - **Position Independent KV-Caching** - Allowing partial blocks to be merged and reused regardless of where they sit in the sequence, critical for non-linear agent flows like "Map-Reduce" summarization (and RAG).

- **Goal 3: Explicit "Semantic" Cache Control** Move from "Black Box" eviction (LRU) to **Context-Aware Lifecycle Management**. The agentic framework must be able to signal which blocks are "System-Prompt/Skills/Tools/…" (durable, high priority) and which are "Thoughts" (ephemeral, low priority).

    KV-disagg roadmap alignment:

    - **KV-Cache Control APIs** - Exposing primitives for "Pin", "Evict", “Move”, and "Prefetch".
    - **Context-Aware Caching-Policy** - Implementing eviction logic that respects these signals rather than blindly flushing old tokens.
    - **True Tiered-KV-Cache** - Implement evictions-based offloading policies in vLLM.

- **Goal 4: Proactive State Distribution** The inference engine should not just react to cache misses; it should anticipate them. When an agent scales horizontally (e.g., spawning 10 workers for a parallel search), the context should be replicated proactively.KV-disagg roadmap alignment:

    **Proactive Prefix-Caching (v0.6/Autoscaling)** Pushing prefixes to new nodes as they spin up, rather than pulling on demand.

- **Goal 5: Benchmarking & Evaluation**

    Extend llm-d’s benchmarking tools with agentic workflow simulators and benchmarks, for benchmark-driven development.

## Non-Goals

- **Non-Goal 1: Managing Agent Logic**

    We do not manage the control flow (loops, conditionals) or the "cognitive" decisions of the agent. llm-d remains the **Execution Engine**; we simply provide the hooks for the Logic Layer (LangChain, LlamaIndex, etc.) to drive the engine efficiently.
    
    It is plausible that a “meet them where they are at” approach is to revolve around Skills/MCP servers.

- **Non-Goal 2: Single-Node Scheduler Micro-Optimization**

    We are not trying to reinvent the OS scheduler within a single vLLM instance. Our focus is on **Cluster-Scale Orchestration**.
