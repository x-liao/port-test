#!/usr/bin/env python3
import socket
import threading
import time

host = '0.0.0.0' #监听接口
port = 50050 #端口
addr = (host,port) 


class TCP_server(threading.Thread):
	def __init__(self, addr):
		super(TCP_server, self).__init__()
		self.addr = addr

	def run(self):
		global threads1
		global threads2
		#tcp
		tcpServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		tcpServer.bind(self.addr)
		tcpServer.listen(5)

		client_tcp_socket,addr = tcpServer.accept()
		msg = "tcp连接成功,连接地址: %s" % str(addr)
		print(msg)
		client_tcp_socket.send(msg.encode('utf-8'))
		tcpServer.close()
		threads1 = []


class UDP_server(threading.Thread):
	def __init__(self, addr):
		super(UDP_server, self).__init__()
		self.addr = addr

	def run(self):
		global threads2
		global threads1
		udpServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		udpServer.bind(self.addr)

		data,addr = udpServer.recvfrom(1024)  #接收数据和返回地址
		#处理数据
		data  = data.decode('utf-8').upper()
		msg = "udp连接成功,连接地址: %s,data:%s" %(str(addr),data)
		print(msg)
		#发送数据
		udpServer.sendto(msg.encode('utf-8'),addr)
		udpServer.close()
		threads2 = []


threads1 = []
threads2 = []

while True:
	if len(threads1) == 0 :
		tcp_thread = TCP_server(addr)
		tcp_thread.start()
		threads1.append(tcp_thread)

	if len(threads2) == 0:
		udp_thread = UDP_server(addr)
		udp_thread.start()
		threads2.append(udp_thread)
	
