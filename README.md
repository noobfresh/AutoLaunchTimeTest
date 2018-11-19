# AutoLaunchTimeTest
LaunchTime Automoatic Test Demo

使用流程

##使用流程
###使用环境配置（Windows版）
####1、JDK环境配置
####2、ANDROID SDK环境配置
####3、python 2.7.x安装
去官网下载python安装包，然后默认安装，安装完成后打开cmd，输入python回车，出现python的版本号说明安装正常，没有出现说明python没有加入到环境变量，请手动加入到环境变量
####4、FFmpeg下载和环境变量配置
[FFmpeg下载地址](https://www.ffmpeg.org/download.html#build-windows "Markdown")   
下载后解压，解压后在目录中找到bin文件夹，把bin目录添加到环境变量path
####5、python库安装



#### 数据表格统计生成:
当所有数据跑完之后，会结果会以json的格式生成，现在包括两种数据生成，示例如下：
1. excel统计表格

|机型 | 版本 | 首次启动耗时（s） |非首次启动耗时（s）|
|---------|---------|---------|---------|
|OPPO R9s | 7.11.1 | 7.17 |5.65 |
| | 7.12 | 4.97|3.04|
| | 虎牙6.6.5 | 3.65 |2.15 |
| |陌陌8.10.4 | 1.63 |2.44|
     
2. 折线图

![折线图示例](https://github.com/hutcwp/img-floder/blob/master/line.png)
