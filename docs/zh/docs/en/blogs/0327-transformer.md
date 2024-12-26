# Who Will Replace the Transformer?

> This article is reprinted from [AI Technology Review](https://mp.weixin.qq.com/s/Q8PIn0FOuXkOT1TiIOuDaA)

![Image](./images/transformer01.png)

The common challenge faced by non-Transformer models is still to prove how high their ceiling is.

## The Past and Present of the Transformer

The 2017 paper "Attention Is All You Need" published by Google has become a bible for contemporary artificial intelligence, and the global AI boom can be directly traced back to the invention of the Transformer.

Due to its ability to handle both local and long-range dependencies and its parallel training capabilities, the Transformer gradually replaced the previous RNN (Recurrent Neural Network) and CNN (Convolutional Neural Network), becoming the standard paradigm for cutting-edge research in NLP (Natural Language Processing).

Today’s mainstream AI models and products—OpenAI's ChatGPT, Google's Bard, Anthropic's Claude, Midjourney, Sora, and domestic models like Zhipu AI's ChatGLM, Baichuan Intelligent's Baichuan model, Kimi chat, etc.—are all based on the Transformer architecture.

The Transformer has become the undisputed gold standard of today's AI technology, and its dominant position remains unshaken.

While the Transformer has thrived, some dissenting voices have emerged, such as: "The efficiency of the Transformer is not high"; "The ceiling of the Transformer is easily seen"; "The Transformer is good, but it cannot achieve AGI or create a world model."

This is because the power of the Transformer is also its weakness: the inherent self-attention mechanism in the Transformer presents challenges, primarily due to its quadratic complexity. This complexity makes the architecture **computationally expensive and memory-intensive** when dealing with long input sequences or in resource-constrained situations.

In simple terms, this means that as the sequence length (for example, the number of words in a paragraph or the size of an image) processed by the Transformer increases, the required computational power grows quadratically, quickly becoming enormous. Hence, there is a saying that "the Transformer is not efficient." This is also a major reason for the global shortage of computing power triggered by the current AI boom.

Based on the limitations of the Transformer, many non-Transformer architectures have emerged, including China's RWKV, Meta's Mega, Microsoft's RetNet, Mamba, and DeepMind's Hawk and Griffin. These models have been proposed following the dominance of the Transformer in the LLM development landscape.

Most of them build on the original RNN foundation, aiming to improve upon the flaws and limitations of the Transformer, attempting to develop what is known as "efficient Transformers," which are architectures that resemble human thinking.

Efficient Transformers refer to models that require less memory and incur lower computational costs during training and inference, trying to overthrow the Transformer’s hegemony.

## Where Is Current Research on Non-Transformer Architectures Heading?

Currently, mainstream non-Transformer research is primarily focused on optimizing the attention mechanism to improve the full attention aspect and finding ways to transform this part into an RNN model to enhance inference efficiency.

Attention is the core of the Transformer—the reason the Transformer model is so powerful is that it abandoned the previously widely used recurrent and convolutional networks in favor of a special structure—the attention mechanism—to model text.

Attention allows the model to consider the relationships between words, regardless of how far apart they are, and to identify which words and phrases in a paragraph deserve the most attention.

This mechanism enables the Transformer to achieve parallelization in language processing, analyzing all words in a specific text simultaneously rather than sequentially. The parallelization of the Transformer provides a more comprehensive and accurate understanding of the text being read and written, making it more computationally efficient and scalable than RNNs.

In contrast, Recurrent Neural Networks (RNNs) face the problem of vanishing gradients, making it difficult for them to train on long sequences. Additionally, they cannot parallelize in time during the training process, limiting their scalability. Convolutional Neural Networks (CNNs) excel at capturing local patterns but lack in long-range dependencies, which are crucial for many sequence processing tasks.

However, RNNs have the advantage that when making inferences, their complexity remains constant, so their memory and computational demands grow linearly. In contrast to the quadratic growth of memory and computational complexity of the Transformer with sequence length, RNNs have lower memory and computational demands. Therefore, many non-Transformer studies today are striving to "retain the advantages of RNNs while achieving Transformer-level performance."

**Based on this goal, today’s non-Transformer technical research can be divided into two main schools:**

The first school, represented by RWKV, Mamba, and S4, completely replaces attention with a recurrent structure. This approach uses fixed memory to retain previous information, but it appears that while it can remember a certain length, achieving longer lengths is challenging.

The second school aims to transform the full attention dense structure into a sparse one, such as Meta's Mega, which no longer requires calculating every element in the attention matrix during subsequent computations, thereby improving the model's efficiency.

Analyzing the various non-Transformer models, RWKV is the first domestically developed open-source large language model with a non-Transformer architecture, and it has now evolved to the sixth generation RWKV-6. The author of RWKV, Peng Bo, began training RWKV-2 in May 2022, starting with 100 million (100M) parameters, and later in March 2023, he trained the RWKV-4 version with 14 billion (14B) parameters.

Peng Bo once told AI Technology Review why he wanted to create a model different from the Transformer architecture:

"Because the world itself does not operate on the logic of Transformers; the laws of the world's operation are based on structures similar to RNNs—what happens in the next second will not be related to all your past time and information, but only to the previous second. The Transformer, which needs to recognize all tokens, is unreasonable."

Thus, RWKV uses linear attention to approximate full attention, attempting to combine the advantages of RNNs and Transformers while avoiding the drawbacks of both, alleviating the memory bottleneck and quadratic expansion issues posed by the Transformer, achieving more effective linear scaling while providing parallel training and scalability, similar to the Transformer. In short, it emphasizes high performance, low energy consumption, and low memory usage.

Mamba, which has been discussed frequently, has two authors: Albert Gu, an assistant professor in the Machine Learning Department at Carnegie Mellon University, and Tri Dao, Chief Scientist at Together.AI.

In their paper, they claim that Mamba is a new SSM architecture that outperforms Transformer models of comparable size in language modeling, both in pre-training and downstream evaluation. Their Mamba-3B model can compete with Transformer models twice its size and can achieve linear scaling with increasing context length, with performance improving in practical data up to million-token length sequences and achieving a fivefold increase in inference throughput.

A non-Transformer researcher told AI Technology Review that Mamba relies entirely on recurrent structures without using attention, so when predicting the next token, **its memory size remains fixed and does not increase over time; however, its problem is that during the rolling process, the memory is very small, resulting in limited extrapolation capability.**

This researcher believes that Microsoft's RetNet also follows a completely recurrent approach. RetNet introduces a multi-scale retention mechanism to replace multi-head attention, with three computation paradigms: parallel, recurrent, and block-recurrent representations.

The paper states that the inference cost of RetNet is independent of length. For a 7B model with an 8k sequence length, RetNet's decoding speed is 8.4 times faster than Transformers with key-value caching, saving 70% of memory.

During training, RetNet can also save 25-50% of memory compared to standard Transformers, achieving a sevenfold speedup and excelling in highly optimized FlashAttention. Additionally, RetNet's inference latency is insensitive to batch size, resulting in significant throughput.

Meta’s Mega represents the second technical route in non-Transformer research. Mega’s approach combines recurrent structures with sparse attention matrices.

One of the core researchers of Mega, Max, told AI Technology Review that attention has irreplaceable roles, and as long as its complexity is kept within a certain range, the desired effects can be achieved. Mega spent a long time researching how to combine recurrent structures and attention for maximum efficiency.

Therefore, Mega still employs an attention structure, but limits attention to a fixed window size while incorporating a rolling memory form similar to Mamba, though Mega's rolling form is much simplified, resulting in faster overall computation.

"Rolling memory" means that all efficient Transformers introduce recurrent structures into the Transformer, where the model first looks at a segment of history, remembers it, then looks at the next segment, updates memory, possibly forgetting some of the first segment's history while adding the necessary parts of the second segment to the overall history, continuously rolling forward.

The advantage of this memory approach is that the model can maintain a fixed-length rolling memory that does not increase over time, but the problem is that for certain special tasks, at the last moment, it may not know which parts of the previous memory are useful and which are not, making it difficult to complete this rolling memory.

Mega has been trained on the same data as LLaMA and, in a fair comparison with LLaMA2, it was found that Mega2 outperformed LLaMA2 significantly under the same data conditions. Additionally, Mega uses a 32K window size for pre-training, while Transformers with the same 32K window size are much slower than Mega2. If the window size increases further, Mega's advantages will become even more apparent. Currently, Mega2 has been trained to a size of 7B.

DeepMind's Hawk and Griffin teams also believe that attention is essential, representing gated linear RNNs, and like Mega, they belong to a hybrid model category.

Apart from RWKV, domestic company Rockchip Intelligence has also released a general natural language LLM with a non-attention mechanism called the Yan model. Rockchip Intelligence's CTO Liu Fanping stated that Yan has no relation to linear attention or RNNs; the LLM architecture of Yan removes the high-cost attention mechanism from the Transformer, replacing it with lower-complexity linear computations, improving modeling efficiency and training speed, thus enhancing efficiency and reducing costs.

## Can the Transformer Be Overturned?

While numerous non-Transformer research proposals have emerged, from an evaluation perspective, they generally outperform Transformers of equivalent size. However, they share the common challenge and skepticism: when scaled up to the size of today’s Transformer models, can they still demonstrate strong performance and efficiency improvements?

Among them, the largest parameter model, RWKV, has 14 billion parameters; Meta's Mega has 7 billion parameters; while GPT-3 has 175 billion parameters, and GPT-4 is rumored to have 1.8 trillion parameters, indicating that non-Transformers urgently need to train a model with hundreds of billions of parameters to prove themselves.

RWKV, the most representative non-Transformer research, has made significant progress—it has completed seed funding of several million yuan; some companies in China are reportedly trying to use RWKV to train models; and in the past year, RWKV has seen partial implementation in both To C and To B markets.

However, several investors have told AI Technology Review that they have struggled with whether to invest in RWKV, betting on non-Transformers. Due to significant internal disagreements—fearing that non-Transformers may not perform well—they ultimately gave up.

Currently, based on the existing hardware computing power foundation, it is very challenging to create LLMs on the edge with Transformers; calculations and inferences still need to be done in the cloud, and the response speed is unsatisfactory, making it difficult for end-users to accept.

An industry insider told AI Technology Review, "On the edge, RWKV may not necessarily be the optimal solution, because with advancements in semiconductors, AI chips are evolving. In the future, the costs of hardware, computing, and energy will eventually be leveled out, and LLMs could easily run directly on the edge without needing significant changes to the underlying architecture. One day, we will reach such a critical point."

RWKV's approach operates from the framework layer, allowing the model to compute locally after lightweighting the framework. However, one investor expressed the view that the ideal state for non-Transformers is to reach OpenAI's level before discussing lightweighting, "not for the sake of being small or localized."

The aforementioned investor evaluated RWKV as "small but complete," achieving an overall experience that can reach 60 points compared to GPT-3.5, but it is uncertain whether it can ultimately reach GPT's 80 or 90 points. This is also a problem for non-Transformers: if the complexity of the framework is discarded, it may sacrifice the upper ceiling.

Someone close to OpenAI told AI Technology Review that OpenAI had actually tested RWKV internally but later abandoned this route, as "its ceiling has not yet been revealed from a long-term perspective, and the possibility of achieving AGI is low."

Proving how high their ceiling is has become a common challenge for all non-Transformer architectures.

Some model researchers claim that the Transformer has not yet reached its ceiling for text LLMs; after all, the scaling law has not failed. The bottleneck of the Transformer may still lie in generating longer sequences, such as in the multimodal domain of video generation, which is essential for achieving AGI in the future. Thus, the context window remains a bottleneck for the Transformer.

If, like OpenAI, one is not afraid of spending money, they could continue to push the scaling law of the Transformer. However, the issue is that for every doubling of the sequence length, the cost quadruples, and the time spent also quadruples. The quadratic growth makes the Transformer inefficient in handling long sequence problems, and resources have limits.

It is understood that leading LLM companies in China primarily utilize Transformers. However, there are speculations about whether GPT-5 will still use the Transformer architecture, as there has been no further open-sourcing since GPT-2. But most prefer to believe that the ceiling of the Transformer is still far away. Therefore, pursuing the Transformer path to catch up with GPT-4 and GPT-5 may not be wrong. In the era of LLMs, everyone is betting.

But whether the Transformer is the only path to achieving AGI remains uncertain. What can be confirmed is that the monopoly formed by the Transformer is hard to break, whether in terms of resources or ecosystem; current non-Transformer research cannot compete.

It is understood that teams researching new non-Transformer architectures are either in academia or are startups like RWKV, with few large companies investing significant teams in researching new architectures. Thus, in terms of resources, the gap between non-Transformer research and Transformers is still substantial.

Moreover, the biggest obstacle in front of them is the increasingly solid ecological moat of the Transformer.

Now, whether in hardware, systems, or applications, everything is adapted and optimized around the Transformer, making the cost-effectiveness of developing other architectures lower, resulting in increasing difficulty in developing new architectures.

In terms of evaluation, many evaluation tasks are designed to favor Transformer architectures, meaning that the tasks they design may only be solvable by Transformer models, while non-Transformers may find it difficult or more challenging. This design can showcase the advantages of Transformers but is not friendly to other architectures.

MIT PhD student and flash-linear-attention project lead Yang Songlin once told AI Technology Review that one of the obstacles faced by non-Transformer research is the evaluation method—simply looking at perplexity shows that non-Transformers actually have no gap compared to Transformer models, but many practical capabilities (such as in-context copy and retrieval) still have significant differences. She believes that current non-Transformer models lack a more comprehensive evaluation method to improve the capability gap with Transformers.

Undoubtedly, the current position of the Transformer remains unshakable; it is still the most powerful AI architecture today. However, outside the echo chamber effect, the work of developing the next generation of artificial intelligence architectures is being vigorously pursued.

Breaking the monopoly is certainly difficult, but according to the laws of technological development, it is hard for any architecture to maintain eternal dominance. In the future, non-Transformers need to continue proving how high their ceiling is, and the Transformer architecture must do the same.
