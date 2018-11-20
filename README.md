# AutoLaunchTimeTest
LaunchTime Automoatic Test Demo
## 介绍
使用python结合图像对比，实现自动化测试app启动耗时。



## 使用流程
### 使用环境配置（Windows版）
#### 1、JDK环境配置
#### 2、ANDROID SDK环境配置
#### 3、python 2.7.x安装
去官网下载python安装包，然后默认安装，安装完成后打开cmd，输入python回车，出现python的版本号说明安装正常，没有出现说明python没有加入到环境变量，请手动加入到环境变量
#### 4、FFmpeg下载和环境变量配置
[FFmpeg下载地址](https://www.ffmpeg.org/download.html#build-windows "Markdown")   
下载后解压，解压后在目录中找到bin文件夹，把bin目录添加到环境变量path
#### 5、python库安装
opencv_python, pillow, numpy, flatten, scikit-image,pyecharts
,pyExcelerator,uiautomator

### 代码部分
代码主要分为3部分
#### 1、screen_record.py
主要通过adb命令和UIAutomator进行应用的安装，弹窗处理，视频录制上传，视频切帧。   
弹窗处理主要通过UIAutomator的对界面元素的点击，部分OPPO手机的安装界面，的取消和安装按钮点击不了，原因是dump出来的xml里面没有这几个按钮，现在的做法是对这些手机分别做处理。    
暂时只支持单个手机插入，后面会做处理。    
录屏的视频会在手机/sdcard/screenrecord存一份，所有流程走完后会上传视频，然后通过FFmpeg把视频切成帧。目前还未对视频以及帧的存储目录做处理，可能会有一些问题。    
目前启动应用只支持YY，后续打算通过配置文件进行处理，扩展到支持其他APP
#### 2、calculate
#### 算法部分

输入：视频帧
输出：2个json文件

安装内容：opencv_python, pillow, numpy, flatten, scikit-image

潜规则：app图标必须防止桌面中间（稍后解决）；
且启动时会有置灰效果，才可以判断出启动首帧。

当前已适配的手机：MiNote2, OPPOR9s, OPPOR11Plusk, vivoX7, vivoX21A

特征图输入：需要输入app启动特征图（图标置灰图），
及首页加载完成特征图（如“热门推荐”）

ps：特征图需保证唯一，放置在feature目录下，
且命名格式为"手机型号_launch/homepage_feature"，图片格式统一取jpg

手机型号获取：在安装adb的前提下，命令行执行“adb shell getprop ro.product.model”,若获取到的设备号
有空格，则去除空格


特征图获取途径：，必须从视频帧or截图裁剪得到，不要用截图截！

关键计算：
1. 首帧：根据启动特征图，匹配视频帧；匹配到视频帧后，利用彩色直方图做二次判断，当前阈值大于0.6时则认为匹配
2. 末帧：根据首页特征图，匹配视频帧；匹配到视频帧后，利用彩色直方图做二次判断，当前阈值大于0.6时则认为匹配；
最后，计算该帧RGB平均值，与homepage目录下的首页样本库的所有图片的RGB平均值，做差值比较，
当前做法：RGB三个值相差在20内则认为到达首页
#### 3、datachart

#### 数据表格统计生成:
当所有数据跑完之后，会结果会以json的格式生成，现在包括两种数据生成，示例如下：
1. excel统计表格：统计某台手机所有测试项平均数据

	|机型 | 版本 | 首次启动耗时（s） |非首次启动耗时（s）|
	|---------|---------|---------|---------|
	|OPPO R9s | 7.11.1 | 7.17 |5.65 |
	| | 7.12 | 4.97|3.04|
	| | 虎牙6.6.5 | 3.65 |2.15 |
	| |陌陌8.10.4 | 1.63 |2.44|
     
2. 折线图：表示任意测试项平均数据
	![折线图示例](https://github.com/hutcwp/img-floder/blob/master/line.png)




