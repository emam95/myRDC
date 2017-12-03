import pygame
import time
import socket
import threading
from PIL import Image
import pyscreenshot as ImageGrab
import zlib

IMAGE_SIZE = 1024, 768

class Client(object):
	def __init__(self):
		self.running = True
		self.server_host = 'localhost'
		self.my_socket = None
		pygame.init()
		size=(IMAGE_SIZE)
		self.screen = pygame.display.set_mode(size) 
		self.clock = pygame.time.Clock() # clock for timing
		pygame.display.set_caption('myRDC', 'myRDC')

	def run(self):
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.connect((self.server_host, 6666))
		max_size = 3 * IMAGE_SIZE[0] * IMAGE_SIZE[1]
		try:
			data = self.my_socket.recv(max_size)
			while self.running:
				if(len(data) == max_size):
					#decimg = zlib.decompress(data)
					img = pygame.image.fromstring(data, IMAGE_SIZE, "RGB")
					self.screen.blit(img,(0,0))
					pygame.display.flip() # update the display
					client.clock.tick(30) # only tick 30 frames per second
					data = self.my_socket.recv(max_size)
				else:
					data += self.my_socket.recv(max_size)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.running = False
			self.kill()
			pygame.quit()
		except SystemExit:
			self.kill()
		pygame.quit()

		#threading.Thread(target=self.receive).start()

	def kill(self):
		self.running = False
		self.my_socket.close()


if __name__ == '__main__':
	client = Client()
	client.run()
