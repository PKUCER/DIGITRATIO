# DigitRatio

## 目录说明

```shell
.
|-- images：存放待检测图像文件
|-- models：
|   |-- model_a: 模型a
|   |-- model_b: 模型b
|-- requirements.txt:
|-- FindCircle.py: 检测logo，为计算手指实际长度建立标尺
|-- HandDetect.py: 检测关节点，输出最终数据
```

备注：
* 图像为jpeg/png/jpg格式
* model_a: [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
* model_b: [BaiduAI](https://ai.baidu.com/tech/body/hand)


## 使用

1. 环境准备
    * python3.8.5
    * pip install -r requirements.txt

0. python FindCircle.py
    运行结果：生成images_preprocessed文件夹

    ```shell
    images_preprocessed
    |-- images_list.txt: images文件夹下图片列表
    |-- images_radius.txt: 检测出logo的图片列表及logo的像素半径
    |-- images_without_logo.txt: 未检测出logo的图片列表
    |-- images_cropped/: 检测出logo的图片。相比原始缩小0.5倍，并进行了裁剪边缘和旋转操作。logo半径计算以图片中识别到的最大蓝色圆圈为准。

    ```

0. python HandDetect.py
    运行结果：
    生成images_result文件夹

    ```shell
    images_result
    |-- images_result_1:        模型1计算的像素长度：2D/4D，拇指，食指，中指，无名指，小指
    |-- images_result_2:        模型2计算的像素长度：2D/4D，拇指，食指，中指，无名指，小指
    |-- images_final_result_1:  模型1的实际长度：2D/4D，拇指，食指，中指，无名指，小指
    |-- images_final_result_2:  模型2的实际长度：2D/4D，拇指，食指，中指，无名指，小指
    |-- images_failure_1:       模型1检测失败的图片列表
    |-- images_failure_2:       模型2检测失败的图片列表
    |-- images_keypoints_1:     模型1检测的21个关键点坐标(x,y)
    |-- images_keypoints_2:     模型2检测的21个关键点坐标(x,y)
    |-- images_visualiztion:    处理后图片的可视化结果。apid为关键点测量图，apis为标识了长度的关键点测量图
    ```

    备注：
    * 对于没有检测到logo的图片，以平均logo像素半径作为参考计算手指的实际长度
    * 关键点坐标图示如下

    ![](assets/fingerpoint.png)

## 拍照操作建议

1. 红色背景板，右上角贴直径3cm白底logo贴纸
0. 红色背景板不要反光（不要外面套塑料纸）
0. 手心朝下,伸直、压平
0. 镜头同背景板平行
0. 灯光明亮，不要有阴影入境
0. 照片中手指朝上
