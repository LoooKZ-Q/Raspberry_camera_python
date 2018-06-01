×××××××××××××××××××××××××××××××××××××××
× Raspberry Pi camera_python_API ×
× module:picamera Python3.5      ×
×××××××××××××××××××××××××××××××××××××××
    import time
    from picamera import PiCamera  # 导入模块
    camera = PiCamera()  # 创建相机对象

1.相机旋转
    camera.rotation = 180  # 旋转角度 180倒置

2.启动相机
    camera.start_preview()  # 开启相机预览
    time.sleep(10)  # 延时
    camera.stop_preview()  # 关闭相机预览

3.改变照片透明度.启动相机参数
    camera.start_preview(alpha=200)  # alpha 取值范围 0-255

4.拍照片
    camera.capture("/home/pi/Desktop/image.jpg")  # 开启预览后插入，截取照片

5.拍视频
    camera.start_recording('/home/pi/video.h264')  # 开启预览后，运行录像开始
    time.sleep(10)  # 延时
    camera.stop_recording()  # 关闭录像
--------------------------------------------------------------------------------------------------------------------------------------------------
-->       进阶
1.摄像头分辨率自行设定， 照片最大分辨率2592x1944 视频1920x1080，最小分辨率64x64
    camera.resolution = (2592,1944)  # 设置分辨率
    camera.framerate = 15  # 帧速率15
2.添加文字annotate_text
    camera.annotate_text  # 开启预览后添加文字
3.调节文字大小 6-160 预设32
    camera.annotate_text_size = 50  # 文字大小设置为50 
4.改变亮度，范围0-100 预设为：50
    camera.brightness = 70  # 亮度设置为70
5.改变文字颜色
from picamera import Color  # 导入Color模块
    camera.annotate_background = Color('blue')  # 背景色
    camera.annotate_foreground = Color('yellow')  # 前景色
    camera.annotate_text = ‘hello word’  # 设置文字
6.camera.image_effect为图片添加特效
    参数：[none，negative，solarize，sketch，denoise，emboss，oilpaint，hatch，gpen，
    pastel，watercolor，film，blur，saturation，colorswap，washedout，posterise，
    colorpoint，colorbalance，cartoon，deinterlace1,deinterlace2]
                [无，负，太阳光，素描，去噪，浮雕，油彩，舱口，手绘，
                粉彩，水彩，电影，模糊，饱和度，色彩交换，洗刷，分页，
                色点，彩色平衡，卡通，去交错1，去交错2]
    用法：camera.image_effect = '参数' ，默认none
7.设置白平衡
    参数：[off,auto, sunlight, cloudy, shade, tungsten, fluorescent,incandescent, flash，horizon]
                 [关闭，自动，阳光，阴天，阴凉，钨，荧光，白炽灯，闪光，地平线]
    用法：camera.awb_mode = '参数' ，默认auto
8.设置曝光模式
    参数：[off，auto，night，nightpreview，nightpreview，spotlight，sports，snow，beach，verylong，fixedfps，antishake，fireworks]
                [关闭，自动，夜间，夜景，夜景，聚光灯，体育，雪，海滩，非常长，固定FPS，防抖，烟花爆竹]
    用法：camera.exposure_mode = '参数'  预设auto
