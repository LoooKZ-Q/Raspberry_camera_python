#!/usr/bin/python3
import time
import os
import re
import socket
from picamera import PiCamera


# 拍摄照片储存路径
PATH = "./cut.jpg"

# 创建web服务器类
class HtmlServer(object):
    def __init__(self):
        '''
        初始化soket, 创建camera对象
        '''
        self.serve_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serve_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.serve_socket.bind(("", 9999))
        self.serve_socket.listen(10)
        self.get_picture = CameraOpen()

    def recv_path(self):
        '''
        监听浏览器是否链接,返回通信soket,解析请求报文-->拼接路径
        '''
        self.cli_socket, ip_port = self.serve_socket.accept()
        print(ip_port)
        path_data = self.cli_socket.recv(1024).decode("utf-8").split("\r\n")[0]
        if path_data:
            path = re.match(r"\w+\s(.+)\s", path_data).group(1)
            path = os.getcwd() + "/www" + path
            self.send_data(path, self.cli_socket)

    def send_data(self, path, cli_socket):
        '''
        通过http协议返回客户端响应报文,
        :param path: 拼接的网页数据的路径
        :param cli_socket: 监听返回的socket
        :return:
        '''
        response_line = "HTTP1.1 200 OK\r\n"
        response_head = "Server:my home 0.1\r\n"
        response_head += "Content-Type: text/html\r\n"
        response_body = b""
        # 判断路径是否存在,否返回404错误
        if not os.path.exists(path):
            response_line = "HTTP1.1 404 Not Found\r\n"
            response_body1 = "<h1>ERROR NOT EXISTS</h1>".encode()
        else:
            # 判断path是否是文件,是
            if os.path.isfile(path):
                # 判断path的文件是不是video.html 视频界面,否,直接打开页面
                if not os.path.basename(path) == "video.html":
                    with open(path, "rb") as f:
                        response_body1 = self.open_file(f, response_body)
                else:
                    # 如果是video ,调用树莓派相机进行拍照,并返回网页
                    self.get_picture.take_picture()
                    with open(path, "rb") as f:
                        response_body1 = self.open_file(f, response_body)
            # 如果不是文件,将访问index.html
            else:
                with open(path + "index.html", "rb") as f:
                    response_body1 = self.open_file(f, response_body)
        # 响应报文拼接,并发送服务器响应报文
        response = response_line.encode() + response_head.encode() + "\r\n".encode() + response_body1
        cli_socket.send(response)

    def open_file(self, f, response_body):
        '''
        循环打开读取文件
        :param f: 文件对象
        :param response_body: 需进行拼接到响应体
        :return: 返回响应体,进行响应报文拼接
        '''
        while True:
            res_data = f.read(1024 * 1024)
            if res_data:
                response_body += res_data
            else:
                return response_body
    # 运行函数循环
    def run_main(self):
        while True:
            self.recv_path()

    # 关闭socket
    def __del__(self):
        self.cli_socket.close()
        self.serve_socket.close()


# 创建树莓派拍照类
class CameraOpen(object):
    def __init__(self):
        # 初始化树莓派相机
        self.camera = PiCamera()

    def take_picture(self):
        self.camera.rotation = 0  # 相机倒置
        # 开启相机预览
        self.camera.start_preview()
        time.sleep(0.1)
        # 将当前时间,以文本格式放入照片
        self.camera.annotate_text = str(time.ctime())
        # 设置文本大小10
        self.camera.annotate_text_size = 20
        # 开始拍照并存入PATH
        self.camera.capture(PATH)
        # 关闭相机预览
        self.camera.stop_preview()


if __name__ == '__main__':
    serv = HtmlServer()
    serv.run_main()
