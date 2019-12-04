#!/usr/bin/env python3
import sys
import getopt
import socket
import threading
import time

bufsize = 1024  #定义缓冲大小

def help():
	print('help')
	exit(0)

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
		data  = data.decode('utf-8')
		msg = "udp连接成功,连接地址: %s,data:%s" %(str(addr),data)
		print(msg)
		#发送数据
		udpServer.sendto(msg.encode('utf-8'),addr)
		udpServer.close()
		threads2 = []


class test_port(object):
	"""docstring for test_port"""
	def __init__(self, host, port):
		super(test_port, self).__init__()
		self.host = host
		self.port = port
		self.addr = (host,port)

	def test_udp(self, data):
		udpClient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
		data = data.encode("utf-8") 
		udpClient.sendto(data,self.addr) # 发送数据
		try:
			udpClient.settimeout(5)
			data,addr = udpClient.recvfrom(bufsize) #接收数据和返回地址
			print(data.decode("utf-8"),'from',addr)
		except Exception as e:
			print('except:', e)
			print('UDP端口测试失败')
		
		udpClient.close()

	def test_tcp(self, data):
		tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		tcpClient.settimeout(5)
		data = data.encode("utf-8")
		try:
			tcpClient.connect(self.addr)
			tcpClient.send(data)
		except Exception as e:
			print('except:', e)
			print('TCP端口测试失败')

		buffer = []
		while True:
			try:
				d = tcpClient.recv(1024)
			except Exception as e:
				#buffer.append(d)
				break

			if d:
				buffer.append(d)
			else:
				break
		msg = b''.join(buffer)
		tcpClient.close()
		print(msg.decode("utf-8"),'from',self.addr)

def Client(host,port,protocol):
	if not protocol:
		protocol = ['tcp']
	while True:
		data = input('>>> ')
		if not data:
			break

		client = test_port(host, port)
		if 'udp' in protocol:
			client.test_udp(data)
		if 'tcp' in protocol:
			client.test_tcp(data)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		help()
	port = 8899
	protocol = []
	args=sys.argv[1:]
	optlist,arg = getopt.getopt(args,'hlutr:p:i:',['help'])
	for opt,v in optlist:
		if opt in ('-h','--help'):
			help()
		if opt in ('-l'):
			mode = 'l'
			host = '0.0.0.0'
		if opt in ('-r'):
			host = v
			mode = 'r'
		if opt in ('-u'):
			protocol.append('udp')
		if opt in ('-t'):
			protocol.append('tcp')
		if opt in ('-p'):
			port = int(v)
		if opt in ('-i'):
			host = v

	if mode == 'r':
		Client(host,port,protocol)
	elif mode == 'l':
		addr = (host,port) 
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