#!/usr/bin/env python3
import socket

host  = '175.102.132.197' # 要测试的ip
port = 58080 #测试端口
bufsize = 1024  #定义缓冲大小

tcp = True
udp = True


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

def main(tcp_test,udp_test):
	while True:
		data = input('>>> ')
		if not data:
			break

		client = test_port(host, port)
		if udp:
			client.test_udp(data)

		if tcp:
			client.test_tcp(data)

if __name__ == '__main__':
	main(tcp,udp)
