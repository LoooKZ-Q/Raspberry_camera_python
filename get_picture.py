import time 
from picamera import PiCamera
# 创建相机对象
camera = PiCamera()
# 将相机图像倒置
# camera.rotation = 180
camera.resolution = (640, 480)
i = 0
# 循环拍摄照片,存入img文件夹
while True:
	camera.start_preview()
	time.sleep(1)
#	time1 = time.ctime()
#	camera.annotate_text = str(time1) 
#	camera.annotate_text_size = 10
	camera.capture("./img/{}.jpg".format(i))
	camera.stop_preview()
	i += 1
	time.sleep(9)
