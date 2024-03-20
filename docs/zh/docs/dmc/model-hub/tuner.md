---
hide:
  - toc
---

# 微调模型

微调模型是指上线到模型仓库后，又通过 [DataTunerX](https://github.com/DataTunerX/datatunerx) 等工具的微调实验得出的模型。

## 部署

1. 点击某个模型右侧的 **...** ，在弹出菜单中选择 **部署** 。

    ![点击部署按钮](../images/tuner01.png)

2. 填写各项参数后点击 **确定** 。

    ![填写参数](../images/inner03.png)

    !!! info "支持国产 GPU"

        其中算力类型支持 Nvidia GPU 和 Ascend 等国产 GPU。

3. 屏幕提示创建成功，接下来可以通过部署的模型提供服务。

下一步：[模型服务](../model-service/index.md)

## 删除

1. 点击某个模型右侧的 **...** ，在弹出菜单中选择 **删除** 。

    ![点击删除按钮](../images/tuner01.png)

2. 输入模型名称，确认无误后删除。

    !!! note

        删除操作不可逆，请谨慎操作。
