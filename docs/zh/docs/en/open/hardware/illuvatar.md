# Illuvatar

This page collects some news about Illuvatar, reprinted from [Zhidx](https://zhidx.com/news/36736.html).

## Orders Approaching 200 Million Yuan

On April 2, 2024, it was reported that [Illuvatar](https://www.iluvatar.com/) announced that its first general-purpose GPU, the TianYuan 100 chip and TianYuan 100 accelerator card, released in March last year, have supported nearly a hundred clients in the AI field over the past year, conducting training on more than 200 different types of models. The performance of backbone network models like ResNet50, SSD, and BERT is close to that of mainstream products in the international market.

Additionally, the TianYuan 100 widely supports traditional machine learning, mathematical computations, encryption and decryption, and digital signal processing. It is also the only general-purpose GPU product that has adapted to various CPU architectures such as x86, Arm, and MIPS.

Illuvatar has successively completed the introduction of TianYuan 100 products with major domestic server manufacturers and entered their supplier directories. Mainstream server manufacturers will soon begin to release server products equipped with the TianYuan 100 for sale. Illuvatar has reached strategic cooperation agreements with industry partners such as H3C Group to initiate comprehensive collaboration. Currently, the cumulative order amount for the TianYuan 100 products has approached 200 million yuan.

## Participation in Large Model Training

On June 10, 2023, at the fifth ZhiYuan Conference AI Systems sub-forum, Shanghai GPU startup Illuvatar announced that its TianYuan 100 accelerator card computing cluster, based on the Aquila language foundation model with 7 billion parameters from the Beijing ZhiYuan Research Institute, continued training using code data and ran stably for 19 days. The model convergence effect met expectations, proving that Illuvatar has the capacity to support training for large models with hundreds of billions of parameters.

With strong support from Haidian District in Beijing, ZhiYuan Research Institute, Illuvatar, and AiTe YunXiang have collaborated to jointly carry out the large model CodeGen (efficient coding) project based on self-developed general-purpose GPUs. This project generates usable C, Java, and Python code from Chinese descriptions to achieve efficient coding. ZhiYuan Research Institute is responsible for algorithm design, training framework development, and training and tuning of large models. Illuvatar provides TianYuan 100 accelerator cards, builds computing clusters, and offers technical support throughout. AiTe YunXiang is responsible for providing the basic hardware for compute-storage-network integration and intelligent operation and maintenance services.

Through the joint efforts of the three parties, the results of parameter optimization work for the 70 billion parameter AquilaCode large model, based on the computing cluster of TianYuan 100 accelerator cards, showed that after 1 epoch, the loss decreased to 0.8, with a training speed reaching 87K Tokens/s and a linear acceleration ratio exceeding 95%. Compared to international mainstream A100 accelerator card clusters, the TianYuan 100 accelerator card cluster demonstrated comparable convergence effects, training speeds, and linear acceleration ratios, with superior stability. On the HumanEval benchmark dataset, using Pass@1 as the evaluation metric, the model trained on the self-built computing cluster achieved results at the SOAT level for large models with similar parameter counts, demonstrating AI programming capabilities comparable to those of mainstream international GPU products.

![Large Model](../images/illu01.jpeg)

## ZhiKai 100

On December 20, 2022, Shanghai Illuvatar Semiconductor Co., Ltd. (hereinafter referred to as "Illuvatar") launched its general-purpose GPU inference product, ZhiKai 100. ZhiKai 100 is the second product officially introduced to the market after the TianYuan 100, marking Illuvatar as a complete solution provider for a general-purpose computing system that integrates cloud-edge collaboration and training-inference combinations.

It is reported that ZhiKai 100 was successfully powered on in May this year and has three major features:

First, it has high computing performance. The ZhiKai 100 chip supports mixed precision computing with FP32, FP16, and INT8, achieving instruction set enhancement, improved computing density, and rebalancing of computing and storage. It supports decoding for various video specifications. The ZhiKai 100 product card can provide peak computing power of up to 384 TOPS@int8, 96 TFlops@FP16, and 24 TFlops@FP32, with a theoretical peak bandwidth of 800 GB/s and the ability to decode various video specifications concurrently at 128 channels. Compared to existing mainstream products in the market, ZhiKai 100 will provide 2-3 times the actual usage performance.

Second, it has wide application coverage. Based on Illuvatar's second-generation general-purpose GPU architecture, ZhiKai 100 features over 800 general-purpose instruction sets and supports mainstream deep learning development frameworks both domestically and internationally. It has a rich set of programming interface extensions and a high-performance function library, allowing flexible support for various algorithm models and facilitating custom development by customers. ZhiKai 100 is widely applicable in various scenarios such as smart cities, smart ports, smart transportation, intelligent manufacturing, power, intelligent voice, healthcare, education, and smart finance.

Third, it has low usage costs. Continuing the easy migration characteristics of the TianYuan 100, ZhiKai 100 fully supports integrated inference and training solutions, enabling incremental training work without additional procurement costs, effectively reducing user expenditure. Following the ecological compatibility strategy of TianYuan 100, ZhiKai 100 still provides an out-of-the-box product experience, lowering users' development and usage costs.

![New Product](../images/illu02.png)

## Financing News

On July 13, 2022, Shanghai Illuvatar Semiconductor Co., Ltd. announced the completion of over 1 billion yuan in C+ and C++ round financing. This round of financing will support the mass production of AI inference chips ZhiKai 100, the development of second and third generation AI training chips TianYuan 200 and 300, the expansion of the Illuvatar software platform, and the acceleration of AI and graphics integration.

The C+ round was led by Financial Street Capital, while the C++ round was led by HOPU Investment and its subsidiary HOPU Innovation Fund (a joint venture fund management company between HOPU Investment and the globally renowned semiconductor technology IP company ARM). Other well-known enterprises and institutions participating in the investment include the Zhongguancun Science City Technology Growth Fund, Shanghai Guosheng, Xicheng Zhiyuan, Emerging Assets, Dingxiang Capital, Dingli Capital, Guangdong-Hong Kong-Macao Industrial Integration, and Shanghai Free Trade Zone Equity Fund.

![Financing](../images/illu03.png)
