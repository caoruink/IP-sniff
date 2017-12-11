from ctypes import *
import struct
import socket


class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),          # 报头长度
        ("version", c_ubyte, 4),      # ip 协议版本
        ("tos",     c_ubyte),         # 区分服务，TOS包括共8位，包括3 bit的优先权字段（取值可以从000-111所有值），4 bit的TOS子字段和1 bit未用位但必须置0。
        ("len",     c_ushort),        # len
        ("id",      c_ushort),        # id
        ("offset",  c_ushort),        # 偏移
        ("ttl",     c_ubyte),         # 过期时间
        ("protocol_num", c_ubyte),    # 控制版本
        ("sum",     c_ushort),        # 检验和
        ("src",     c_ulong),         # 源地址
        ("dst",     c_ulong)          # 目的地址
        ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # 协议映射
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        # 传参
        self.ihl_ = self.ihl
        self.version_ = self.version
        self.tos_ = self.tos
        self.len_ = self.len
        self.id_ = self.id
        self.offset_ = self.offset
        self.ttl_ = self.ttl
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)
        self.sum_ = self.sum
        self.src_ = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_ = socket.inet_ntoa(struct.pack("<L", self.dst))
