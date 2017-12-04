import socket
import threading
import time
from PIL import Image
import pyscreenshot as ImageGrab
import zlib
from pymouse import PyMouse

IMAGE_SIZE = 1366, 768
PORT_NUMBER = 6666

def capscreen():
	#return zlib.compress(ImageGrab.grab().resize(IMAGE_SIZE).tobytes())
	return ImageGrab.grab().resize(IMAGE_SIZE).tobytes()

class Server():
	def __init__(self):
		self.running = True
		self.socket = None
		self.client_socket = None
		self.client_address = None
		self.mouse = PyMouse()

	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(('localhost', PORT_NUMBER))
		self.socket.listen(1) # max 1 connection for now
		print('Waiting for connections...')
		self.client_socket, self.client_address = self.socket.accept()
		print('connected to ' + str(self.client_address))
		threading.Thread(target=self.receive).start()
		#self.client_socket.send(str(IMAGE_SIZE).encode()) #sending dimensions
		while self.running:
			self.sendcap()

	def sendcap(self):
		ss = capscreen()
		self.client_socket.send(ss)

	def receive(self):
		while self.running:
			mouse_location = (self.client_socket.recv(1024).decode())
			print(mouse_location)
			if ',' in mouse_location:
				x, y = map(float, mouse_location.split(','))
				self.mouse.move(int(x), int(y))

	def kill(self):
		self.running = False
		self.client_socket.close()

if __name__ == '__main__':
	server = Server()
	server.run()

