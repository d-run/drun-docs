# Hugging Face

!!! info

    [Hugging Face](https://huggingface.co/) is the hottest open-source AI community in the field of machine learning, with its [Transformers repository](https://github.com/huggingface/transformers) reaching 124,000 stars.

<h3 align="center">
    <p>Advanced natural language processing built for Jax, PyTorch, and TensorFlow</p>
</h3>

<h3 align="center">
    <a href="https://hf.co/course"><img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/course_banner.png"></a>
</h3>

🤗 Transformers provides thousands of pre-trained models that support text classification, information extraction, question answering, summarization, translation, and text generation in over 100 languages. Its mission is to make cutting-edge NLP technology accessible to everyone.

🤗 Transformers offers an API for quick downloading and usage, allowing you to apply pre-trained models to given text, fine-tune on your dataset, and then share with the community through the [model hub](https://huggingface.co/models). Additionally, each defined Python module is completely independent, making it easy to modify and quickly research experiments.

🤗 Transformers supports the three most popular deep learning libraries: [Jax](https://jax.readthedocs.io/en/latest/), [PyTorch](https://pytorch.org/), and [TensorFlow](https://www.tensorflow.org/) — seamlessly integrating with them. You can train your model using one framework and then load and infer with another.

## Online Demos

You can directly test most models on the [model hub](https://huggingface.co/models) model pages. Hugging Face also offers [private model hosting, model version management, and inference APIs](https://huggingface.co/pricing).

Here are some examples:

- [Fill in the blanks with BERT](https://huggingface.co/google-bert/bert-base-uncased?text=Paris+is+the+%5BMASK%5D+of+France)
- [Named entity recognition with Electra](https://huggingface.co/dbmdz/electra-large-discriminator-finetuned-conll03-english?text=My+name+is+Sarah+and+I+live+in+London+city)
- [Text generation with GPT-2](https://huggingface.co/openai-community/gpt2?text=A+long+time+ago%2C+)
- [Natural language inference with RoBERTa](https://huggingface.co/FacebookAI/roberta-large-mnli?text=The+dog+was+lost.+Nobody+lost+any+animal)
- [Text summarization with BART](https://huggingface.co/facebook/bart-large-cnn?text=The+tower+is+324+metres+%281%2C063+ft%29+tall%2C+about+the+same+height+as+an+81-storey+building%2C+and+the+tallest+structure+in+Paris.+Its+base+is+square%2C+measuring+125+metres+%28410+ft%29+on+each+side.+During+its+construction%2C+the+Eiffel+Tower+surpassed+the+Washington+Monument+to+become+the+tallest+man-made+structure+in+the+world%2C+a+title+it+held+for+41+years+until+the+Chrysler+Building+in+New+York+City+was+finished+in+1930.+It+was+the+first+structure+to+reach+a+height+of+300+metres.+Due+to+the+addition+of+a+broadcasting+aerial+at+the+top+of+the+tower+in+1957%2C+it+is+now+taller+than+the+Chrysler+Building+by+5.2+metres+%2817+ft%29.+Excluding+transmitters%2C+the+Eiffel+Tower+is+the+second+tallest+free-standing+structure+in+France+after+the+Millau+Viaduct)
- [Question answering with DistilBERT](https://huggingface.co/distilbert/distilbert-base-uncased-distilled-squad?text=Which+name+is+also+used+to+describe+the+Amazon+rainforest+in+English%3F&context=The+Amazon+rainforest+%28Portuguese%3A+Floresta+Amaz%C3%B4nica+or+Amaz%C3%B4nia%3B+Spanish%3A+Selva+Amaz%C3%B3nica%2C+Amazon%C3%ADa+or+usually+Amazonia%3B+French%3A+For%C3%AAt+amazonienne%3B+Dutch%3A+Amazoneregenwoud%29%2C+also+known+in+English+as+Amazonia+or+the+Amazon+Jungle%2C+is+a+moist+broadleaf+forest+that+covers+most+of+the+Amazon+basin+of+South+America.+This+basin+encompasses+7%2C000%2C000+square+kilometres+%282%2C700%2C000+sq+mi%29%2C+of+which+5%2C500%2C000+square+kilometres+%282%2C100%2C000+sq+mi%29+are+covered+by+the+rainforest.+This+region+includes+territory+belonging+to+nine+nations.+The+majority+of+the+forest+is+contained+within+Brazil%2C+with+60%25+of+the+rainforest%2C+followed+by+Peru+with+13%25%2C+Colombia+with+10%25%2C+and+with+minor+amounts+in+Venezuela%2C+Ecuador%2C+Bolivia%2C+Guyana%2C+Suriname+and+French+Guiana.+States+or+departments+in+four+nations+contain+%22Amazonas%22+in+their+names.+The+Amazon+represents+over+half+of+the+planet%27s+remaining+rainforests%2C+and+comprises+the+largest+and+most+biodiverse+tract+of+tropical+rainforest+in+the+world%2C+with+an+estimated+390+billion+individual+trees+divided+into+16%2C000+species)
- [Translation with T5](https://huggingface.co/google-t5/t5-base?text=My+name+is+Wolfgang+and+I+live+in+Berlin)

**[Write With Transformer](https://transformer.huggingface.co)**, developed by the Hugging Face team, is the official demo for text generation.

## Customized Support Services Offered by Hugging Face

<a target="_blank" href="https://huggingface.co/support">
    <img alt="HuggingFace Expert Acceleration Program" src="https://huggingface.co/front/thumbnails/support.png" style="max-width: 600px; border: 1px solid #eee; border-radius: 4px; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);">
</a><br>

## Quick Start

Hugging Face provides a `pipeline` API for quickly using models. The pipeline aggregates pre-trained models and corresponding text preprocessing. Here’s a quick example of using the pipeline to classify sentiment:

```python
>>> from transformers import pipeline

# Using the sentiment analysis pipeline
>>> classifier = pipeline('sentiment-analysis')
>>> classifier('We are very happy to introduce pipeline to the transformers repository.')
[{'label': 'POSITIVE', 'score': 0.9996980428695679}]
```

The second line of code downloads and caches the pre-trained model used by the pipeline, while the third line evaluates the given text. The answer "positive" has a confidence of 99%.

Many NLP tasks have out-of-the-box pre-trained pipelines. For example, Hugging Face can easily extract question answers from given text:

``` python
>>> from transformers import pipeline

# Using the question answering pipeline
>>> question_answerer = pipeline('question-answering')
>>> question_answerer({
...     'question': 'What is the name of the repository?',
...     'context': 'Pipeline has been included in the huggingface/transformers repository'
... })
{'score': 0.30970096588134766, 'start': 34, 'end': 58, 'answer': 'huggingface/transformers'}
```

In addition to providing the answer, the pre-trained model also gives the corresponding confidence score, as well as the start and end positions of the answer in the tokenized text. You can learn more about the tasks supported by the pipeline API from [this tutorial](https://huggingface.co/docs/transformers/task_summary).

It is also simple to download and use any pre-trained model for your task with just three lines of code. Here’s an example in PyTorch:
```python
>>> from transformers import AutoTokenizer, AutoModel

>>> tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
>>> model = AutoModel.from_pretrained("google-bert/bert-base-uncased")

>>> inputs = tokenizer("Hello world!", return_tensors="pt")
>>> outputs = model(**inputs)
```

Here’s the equivalent TensorFlow code:

```python
>>> from transformers import AutoTokenizer, TFAutoModel

>>> tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
>>> model = TFAutoModel.from_pretrained("google-bert/bert-base-uncased")

>>> inputs = tokenizer("Hello world!", return_tensors="tf")
>>> outputs = model(**inputs)
```

The tokenizer provides preprocessing for all pre-trained models and can be called directly on a single string (like in the above example) or on a list. It outputs a dictionary that can be used in downstream code or directly unpacked using the `**` expression to pass to the model.

The model itself is a standard [Pytorch `nn.Module`](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) or [TensorFlow `tf.keras.Model`](https://www.tensorflow.org/api_docs/python/tf/keras/Model) (depending on your backend), and can be used in a conventional manner. [This tutorial](https://huggingface.co/transformers/training.html) explains how to integrate such models into classic PyTorch or TensorFlow training loops, or how to use Hugging Face's `Trainer` API to quickly fine-tune on a new dataset.

## Why Use Transformers?

1. User-friendly advanced models:

    - Excellent performance in NLU and NLG
    - Educational and practical, with low barriers to entry
    - High-level abstractions, requiring knowledge of only three classes
    - Unified API for all models

2. Lower computational overhead and reduced carbon emissions:

    - Researchers can share trained models instead of retraining from scratch each time
    - Engineers can reduce computation time and production costs
    - Dozens of model architectures, over 2,000 pre-trained models, and support for more than 100 languages

3. Comprehensive support for every part of the model lifecycle:

    - Training advanced models requires just 3 lines of code
    - Models can be easily transferred between different deep learning frameworks
    - Choose the most suitable framework for training, evaluation, and production, with seamless integration

4. Easily customize exclusive models and use cases for your needs:

    - Multiple use cases provided for each model architecture to reproduce original paper results
    - Internal structure of models remains transparent and consistent
    - Model files can be used independently for easy modifications and quick experiments

## When Not to Use Transformers?

- This library is not a modular neural network toolbox. The code in the model files is intentionally presented in a raw form without additional abstraction, allowing researchers to quickly iterate and modify without getting lost in abstractions and file navigation.
- The `Trainer` API is not compatible with any model; it is optimized for models in this library. If you are looking for a training loop implementation suitable for general machine learning, please look for another library.
- Although Hugging Face has made significant efforts, the scripts in the [examples directory](https://github.com/huggingface/transformers/tree/main/examples) are just examples. They may not be plug-and-play for your specific problem and might require some modifications.

## Installation

### Using pip

This repository has been tested with Python 3.8+, Flax 0.4.1+, PyTorch 1.11+, and TensorFlow 2.6+.

You can install 🤗 Transformers in a [virtual environment](https://docs.python.org/3/library/venv.html). If you are not familiar with Python's virtual environments, please refer to this [user guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

First, create a virtual environment with the version of Python you plan to use and activate it.

Then, you need to install either Flax, PyTorch, or TensorFlow. For instructions on installing these frameworks on your platform, see the [TensorFlow installation page](https://www.tensorflow.org/install/), the [PyTorch installation page](https://pytorch.org/get-started/locally/#start-locally), or the [Flax installation page](https://github.com/google/flax#quick-install).

Once one of these backends is successfully installed, you can install 🤗 Transformers as follows:

```bash
pip install transformers
```

If you want to try out examples or use the latest development code before the official release, you need to [install from source](https://huggingface.co/docs/transformers/installation#installing-from-source).

### Using conda

🤗 Transformers can be installed via conda as follows:

```shell script
conda install conda-forge::transformers
```

!!! note "Note"

    Installing `transformers` from the `huggingface` channel has been deprecated.

For instructions on installing either Flax, PyTorch, or TensorFlow via conda, please refer to their respective installation pages.

## Model Architectures

All model checkpoints supported by 🤗 Transformers are uploaded by [users](https://huggingface.co/users) and [Hugging Face organizations](https://huggingface.co/organizations) and are seamlessly integrated with the huggingface.co [model hub](https://huggingface.co).

Current number of models:
![](https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/models&color=brightgreen)
