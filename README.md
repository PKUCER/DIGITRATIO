# DigitRatio

## 文件说明

```shell
.
|-- images：存放待检测图像文件
|-- models：
|   |-- xxx: 模型1，source link
|   |-- xxx:
|-- requirements.txt:
|-- find_circle.py:
|-- hand_detect.py:
```

备注：

* 图像为jpeg格式

## 使用

1. ESIEC2019数据预处理：
    * 去除不含手掌的照片
    * ESIEC2019logo贴纸以3cm为标准

0. python3环境之下

0. pip install -r requirements.txt

0. python find_dircle.py
    运行结果：
    生成images_preprocessed文件夹

    ```shell
    images_preprocessed
    |-- images_list.txt: images文件夹下图片列表
    |-- images_radius.txt: 检测出logo的图片列表及logo的像素半径
    |-- images_without_logo.txt: 未检测出logo的图片列表
    |-- images_cropped/: 检测出logo的图片
    ```

    备注：
    * images_cropped中的图片相比图片照片缩小0.5倍，并进行了裁剪边缘和旋转操作。logo半径计算以图片中识别到的最大蓝色圆圈为准。

0. python hand_detect.py
    运行结果：
    生成images_result文件夹

    ```shell
    images_result
    |-- images_result_1: 模型1计算的像素长度
    |-- images_result_2: 模型2计算的像素长度
    |-- images_final_result_1: 模型1的实际长度
    |-- images_final_result_2: 模型2的实际长度
    |-- images_failed/: 未被成功检测的照片
    |-- images_result_visualiztion: 处理后图片的可视化结果
    ```

    备注：
    * 对于没有检测到logo的图片，以平均logo像素半径作为参考计算手指的实际长度
    * images_result_visualization中XXX
