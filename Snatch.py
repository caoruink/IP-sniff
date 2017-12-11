import socket
import os
from time import*
from IP import IP


class Snatch(object):
    """
    预先设定嗅探器，绑定端口号。sniffer.setsockopt(),sniffer.ioctl()不设置则抓不到数据
    """
    @staticmethod
    def socket_Snatch():
        # 设定嗅探器
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        # 获取主机IP
        host = socket.gethostbyname(socket.gethostname())
        # 绑定端口号以嗅探
        sniffer.bind((host, 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_MAX)
        return sniffer

    """
    监听数据，并返回数据报，用IP类解析报头中的信息，并返回
    """
    @staticmethod
    def Receive(sniffer=None):
        if not sniffer:
            return None
        try:
            # 65565不是端口号是缓存大小
            raw_buffer = sniffer.recvfrom(65565)[0]
            ip_header = IP(raw_buffer[0:20])
            # print(" Version:%s \n Protocol:%s \n Len:%s \n Src:%s -> Dst:%s\n Time:%s\n"
            #         % ( ip_header.version_,ip_header.protocol, ip_header.len_, ip_header.src_,
            # ip_header.dst_, time())
            #       )
            return [strftime('%Y-%m-%d %H-%M-%S', localtime(time())), ip_header.version_, ip_header.protocol,
                    ip_header.src_, ip_header.dst_, ip_header.len_]

        except KeyboardInterrupt:
            if os.name == "nt":
                sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == "__main__":
    s = Snatch.socket_Snatch()
    while True:
        Snatch.Receive(s)
