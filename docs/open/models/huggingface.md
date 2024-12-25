# Hugging Face

!!! info

    [Hugging Face](https://huggingface.co/) 是机器学习领域中最火热的开源 AI 社区，
    旗下 [Transformers 仓库](https://github.com/huggingface/transformers)的 Star 数达 12.4 万。

<h3 align="center">
    <p>为 Jax、PyTorch 和 TensorFlow 打造的先进的自然语言处理</p>
</h3>

<h3 align="center">
    <a href="https://hf.co/course"><img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/course_banner.png"></a>
</h3>

🤗 Transformers 提供了数以千计的预训练模型，支持 100 多种语言的文本分类、信息抽取、问答、摘要、翻译、文本生成。它的宗旨是让最先进的 NLP 技术人人易用。

🤗 Transformers 提供了便于快速下载和使用的API，让你可以把预训练模型用在给定文本、在你的数据集上微调然后通过 [model hub](https://huggingface.co/models) 与社区共享。同时，每个定义的 Python 模块均完全独立，方便修改和快速研究实验。

🤗 Transformers 支持三个最热门的深度学习库：
[Jax](https://jax.readthedocs.io/en/latest/)、[PyTorch](https://pytorch.org/) 以及 [TensorFlow](https://www.tensorflow.org/) — 并与之无缝整合。
你可以直接使用一个框架训练你的模型然后用另一个加载和推理。

## 在线演示

你可以直接在模型页面上测试大多数 [model hub](https://huggingface.co/models) 上的模型。
Hugging Face 也提供了[私有模型托管、模型版本管理以及推理API](https://huggingface.co/pricing)。

这里是一些例子：

- [用 BERT 做掩码填词](https://huggingface.co/google-bert/bert-base-uncased?text=Paris+is+the+%5BMASK%5D+of+France)
- [用 Electra 做命名实体识别](https://huggingface.co/dbmdz/electra-large-discriminator-finetuned-conll03-english?text=My+name+is+Sarah+and+I+live+in+London+city)
- [用 GPT-2 做文本生成](https://huggingface.co/openai-community/gpt2?text=A+long+time+ago%2C+)
- [用 RoBERTa 做自然语言推理](https://huggingface.co/FacebookAI/roberta-large-mnli?text=The+dog+was+lost.+Nobody+lost+any+animal)
- [用 BART 做文本摘要](https://huggingface.co/facebook/bart-large-cnn?text=The+tower+is+324+metres+%281%2C063+ft%29+tall%2C+about+the+same+height+as+an+81-storey+building%2C+and+the+tallest+structure+in+Paris.+Its+base+is+square%2C+measuring+125+metres+%28410+ft%29+on+each+side.+During+its+construction%2C+the+Eiffel+Tower+surpassed+the+Washington+Monument+to+become+the+tallest+man-made+structure+in+the+world%2C+a+title+it+held+for+41+years+until+the+Chrysler+Building+in+New+York+City+was+finished+in+1930.+It+was+the+first+structure+to+reach+a+height+of+300+metres.+Due+to+the+addition+of+a+broadcasting+aerial+at+the+top+of+the+tower+in+1957%2C+it+is+now+taller+than+the+Chrysler+Building+by+5.2+metres+%2817+ft%29.+Excluding+transmitters%2C+the+Eiffel+Tower+is+the+second+tallest+free-standing+structure+in+France+after+the+Millau+Viaduct)
- [用 DistilBERT 做问答](https://huggingface.co/distilbert/distilbert-base-uncased-distilled-squad?text=Which+name+is+also+used+to+describe+the+Amazon+rainforest+in+English%3F&context=The+Amazon+rainforest+%28Portuguese%3A+Floresta+Amaz%C3%B4nica+or+Amaz%C3%B4nia%3B+Spanish%3A+Selva+Amaz%C3%B3nica%2C+Amazon%C3%ADa+or+usually+Amazonia%3B+French%3A+For%C3%AAt+amazonienne%3B+Dutch%3A+Amazoneregenwoud%29%2C+also+known+in+English+as+Amazonia+or+the+Amazon+Jungle%2C+is+a+moist+broadleaf+forest+that+covers+most+of+the+Amazon+basin+of+South+America.+This+basin+encompasses+7%2C000%2C000+square+kilometres+%282%2C700%2C000+sq+mi%29%2C+of+which+5%2C500%2C000+square+kilometres+%282%2C100%2C000+sq+mi%29+are+covered+by+the+rainforest.+This+region+includes+territory+belonging+to+nine+nations.+The+majority+of+the+forest+is+contained+within+Brazil%2C+with+60%25+of+the+rainforest%2C+followed+by+Peru+with+13%25%2C+Colombia+with+10%25%2C+and+with+minor+amounts+in+Venezuela%2C+Ecuador%2C+Bolivia%2C+Guyana%2C+Suriname+and+French+Guiana.+States+or+departments+in+four+nations+contain+%22Amazonas%22+in+their+names.+The+Amazon+represents+over+half+of+the+planet%27s+remaining+rainforests%2C+and+comprises+the+largest+and+most+biodiverse+tract+of+tropical+rainforest+in+the+world%2C+with+an+estimated+390+billion+individual+trees+divided+into+16%2C000+species)
- [用 T5 做翻译](https://huggingface.co/google-t5/t5-base?text=My+name+is+Wolfgang+and+I+live+in+Berlin)

**[Write With Transformer](https://transformer.huggingface.co)** ，由 Hugging Face 团队打造，是一个文本生成的官方 demo。

## Hugging Face 提供的定制化支持服务

<a target="_blank" href="https://huggingface.co/support">
    <img alt="HuggingFace Expert Acceleration Program" src="https://huggingface.co/front/thumbnails/support.png" style="max-width: 600px; border: 1px solid #eee; border-radius: 4px; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);">
</a><br>

## 快速上手

Hugging Face 为快速使用模型提供了 `pipeline`（流水线）API。
流水线聚合了预训练模型和对应的文本预处理。下面是一个快速使用流水线去判断正负面情绪的例子：

```python
>>> from transformers import pipeline

# 使用情绪分析流水线
>>> classifier = pipeline('sentiment-analysis')
>>> classifier('We are very happy to introduce pipeline to the transformers repository.')
[{'label': 'POSITIVE', 'score': 0.9996980428695679}]
```

第二行代码下载并缓存了流水线使用的预训练模型，而第三行代码则在给定的文本上进行了评估。这里的答案“正面” (positive) 具有 99 的置信度。

许多的 NLP 任务都有开箱即用的预训练流水线。比如说，Hugging Face 可以轻松的从给定文本中抽取问题答案：

``` python
>>> from transformers import pipeline

# 使用问答流水线
>>> question_answerer = pipeline('question-answering')
>>> question_answerer({
...     'question': 'What is the name of the repository ?',
...     'context': 'Pipeline has been included in the huggingface/transformers repository'
... })
{'score': 0.30970096588134766, 'start': 34, 'end': 58, 'answer': 'huggingface/transformers'}
```

除了给出答案，预训练模型还给出了对应的置信度分数、答案在词符化 (tokenized) 后的文本中开始和结束的位置。
你可以从[这个教程](https://huggingface.co/docs/transformers/task_summary)了解更多流水线API支持的任务。

要在你的任务上下载和使用任意预训练模型也很简单，只需三行代码。这里是 PyTorch 版的示例：
```python
>>> from transformers import AutoTokenizer, AutoModel

>>> tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
>>> model = AutoModel.from_pretrained("google-bert/bert-base-uncased")

>>> inputs = tokenizer("Hello world!", return_tensors="pt")
>>> outputs = model(**inputs)
```

这里是等效的 TensorFlow 代码：

```python
>>> from transformers import AutoTokenizer, TFAutoModel

>>> tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
>>> model = TFAutoModel.from_pretrained("google-bert/bert-base-uncased")

>>> inputs = tokenizer("Hello world!", return_tensors="tf")
>>> outputs = model(**inputs)
```

词符化器 (tokenizer) 为所有的预训练模型提供了预处理，并可以直接对单个字符串进行调用（比如上面的例子）或对列表 (list) 调用。
它会输出一个你可以在下游代码里使用或直接通过 `**` 解包表达式传给模型的词典 (dict)。

模型本身是一个常规的 [Pytorch `nn.Module`](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) 或
[TensorFlow `tf.keras.Model`](https://www.tensorflow.org/api_docs/python/tf/keras/Model)（取决于你的后端），
可以常规方式使用。[这个教程](https://huggingface.co/transformers/training.html)解释了如何将这样的模型整合到经典的
PyTorch 或 TensorFlow 训练循环中，或是如何使用 Hugging Face 的 `Trainer` 训练器）API 来在一个新的数据集上快速微调。

## 为什么要用 Transformers？

1. 便于使用的先进模型：

    - NLU 和 NLG 上表现优越
    - 对教学和实践友好且低门槛
    - 高级抽象，只需了解三个类
    - 对所有模型统一的API

1. 更低计算开销，更少的碳排放：

    - 研究人员可以分享已训练的模型而非每次从头开始训练
    - 工程师可以减少计算用时和生产环境开销
    - 数十种模型架构、两千多个预训练模型、100多种语言支持

1. 对于模型生命周期的每一个部分都面面俱到：

    - 训练先进的模型，只需 3 行代码
    - 模型在不同深度学习框架间任意转移，随你心意
    - 为训练、评估和生产选择最适合的框架，衔接无缝

1. 为你的需求轻松定制专属模型和用例：

    - 为每种模型架构提供了多个用例来复现原论文结果
    - 模型内部结构保持透明一致
    - 模型文件可单独使用，方便魔改和快速实验

## 什么情况下不该用 Transformers？

- 本库并不是模块化的神经网络工具箱。模型文件中的代码特意呈若璞玉，未经额外抽象封装，以便研究人员快速迭代魔改而不致溺于抽象和文件跳转之中。
- `Trainer` API 并非兼容任何模型，只为本库之模型优化。若是在寻找适用于通用机器学习的训练循环实现，请另觅他库。
- 尽管 Hugging Face 已尽力而为，[examples 目录](https://github.com/huggingface/transformers/tree/main/examples)中的脚本也仅为用例而已。
  对于你的特定问题，它们并不一定开箱即用，可能需要改几行代码以适之。

## 安装

### 使用 pip

这个仓库已在 Python 3.8+、Flax 0.4.1+、PyTorch 1.11+ 和 TensorFlow 2.6+ 下经过测试。

你可以在[虚拟环境](https://docs.python.org/3/library/venv.html)中安装 🤗 Transformers。如果你还不熟悉 Python 的虚拟环境，
请阅此[用户说明](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)。

首先，用你打算使用的版本的 Python 创建一个虚拟环境并激活。

然后，你需要安装 Flax、PyTorch 或 TensorFlow 其中之一。关于在你使用的平台上安装这些框架，请参阅
[TensorFlow 安装页](https://www.tensorflow.org/install/),
[PyTorch 安装页](https://pytorch.org/get-started/locally/#start-locally) 或
[Flax 安装页](https://github.com/google/flax#quick-install)。

当这些后端之一安装成功后， 🤗 Transformers 可依此安装：

```bash
pip install transformers
```

如果你想要试试用例或者想在正式发布前使用最新的开发中代码，
你得[从源代码安装](https://huggingface.co/docs/transformers/installation#installing-from-source)。

### 使用 conda

🤗 Transformers 可以通过 conda 依此安装：

```shell script
conda install conda-forge::transformers
```

!!! note "笔记"

    从 `huggingface` 渠道安装 `transformers` 已被废弃。

要通过 conda 安装 Flax、PyTorch 或 TensorFlow 其中之一，请参阅它们各自安装页的说明。

## 模型架构

🤗 Transformers 支持的[所有的模型检查点](https://huggingface.co/models)由[用户](https://huggingface.co/users)和
[Hugging Face 组织](https://huggingface.co/organizations)上传，
均与 huggingface.co [model hub](https://huggingface.co) 无缝整合。

目前的模型数量：
![](https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/models&color=brightgreen)
