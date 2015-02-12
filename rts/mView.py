import pygame
import os
import sys
import mMap
import mUnit
from misc.mLogger import log


class TextBox(pygame.sprite.Sprite):

	def __init__(self, _pos):
		pygame.sprite.Sprite.__init__(self)
		self.size_ = (100, 100)
		self.pos_ = _pos
		self.initFont()
		self.initImage()

	def initFont(self):
		pygame.font.init()
		self.font = pygame.font.Font(None, 20)

	def initImage(self):
		self.image = pygame.Surface(self.size_)
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos_

	def setText(self, text):
		tmp = pygame.display.get_surface()
		x_pos = self.rect.left + 5
		y_pos = self.rect.top + 5
		for t in text:
			x = self.font.render(t, False, (0, 0, 0))
			tmp.blit(x, (x_pos, y_pos))
			x_pos += 10
			if (x_pos > self.image.get_width() - 5):
				x_pos = self.rect.left + 5
				y_pos += 30


class mView(object):

	def __init__(self, map_):
		pygame.init()
		self.SCREEN_SIZE = (800, 600)
		self.GRIDAREA_SIZE = (600, 600)
		self.TEXTAREA_POS = (620, 100)
		self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
		self.map_ = map_
		self.ROWS, self.CLMNS = self.map_.data_.heigth_, self.map_.data_.heigth_
		pygame.font.init()
		self.font = pygame.font.Font(None, 20)

	def show(self):
		self.screen.fill((255, 255, 255))
		self.draw_grid(self.screen, width=1)
		#self.rect(self.screen, 0, 0, color=(255, 0, 0), scale=0.6)
		for u, i, j in self.map_:
			width = 0
			color = (255, 255, 255)
			if not hasattr(u, 'camp_'):
				color = (255, 255, 255)
			elif u.camp_ == 0:
				if u.lock_:
					width = 3
				else:
					width = 2
				if u.type:
					color = u.map_.camps_[u.camp_].color_
			elif u.camp_ == 1:
				if u.lock_:
					width = 3
				else:
					width = 2
				if u.type:
					color = u.map_.camps_[u.camp_].color_
			else:
				color = (0, 255, 0)
			if u.type == 1:
				text = '@%d/%d'%(u.hp_, u.maxhp)
				self.ellipse(self.screen, i, j, color=color, scale=0.8, width=width, text=text)
			elif u.type == 2:
				text = '@%d/%d$%d'%(u.hp_, u.maxhp, self.map_.camps_[u.camp_].res_)
				self.rect(self.screen, i, j, color=color, scale=0.7, width=width, text=text)
			elif u.type == 3:
				text = '@%d/%d$%d'%(u.hp_, u.maxhp, u.res_)
				self.circle(self.screen, i, j, color=color, scale=0.6, width=width, text=text)
			elif u.type == 4:
				text = '$%d'%(u.res_count,)
				self.rect(self.screen, i, j, color=color, scale=0.8, width=0, text=text)
		self.write()

	def write(self):
		t = TextBox(self.TEXTAREA_POS)
		t.setText(self.map_.desc())
	#	font = pygame.font.Font(None, 25)
	#	t = font.render('adsdfsdf\r\n'*10,1,(255,0,0))
	#	textpos = t.get_rect()
	#	textpos.topleft = 100, 100
	#	self.screen.blit(t, textpos)

	def loop(self):
		for event in pygame.event.get():
			if event.type in (pygame.QUIT, pygame.KEYDOWN):
				sys.exit()
		self.show()
		pygame.display.update()

	def load_image(self, name):
		main_dir = os.path.split(os.path.abspath(__file__))[0]
		path = os.path.join(main_dir, 'res', name)
		return pygame.image.load(path).convert()
	
	def draw_grid(self, screen, color=(0, 0, 0), width=1):
		for r in xrange(1, self.ROWS + 1):
			start_pos, end_pos = (1.0 * r * self.GRIDAREA_SIZE[0] / self.ROWS - 1, 0), (1.0 * r * self.GRIDAREA_SIZE[0] / self.ROWS - 1, self.GRIDAREA_SIZE[1] - 1)
			pygame.draw.line(screen, color, start_pos, end_pos, width)
		for c in xrange(1, self.CLMNS + 1):
			start_pos, end_pos = (0, 1.0 * c * self.GRIDAREA_SIZE[1] / self.CLMNS - 1), (self.GRIDAREA_SIZE[0] - 1, 1.0 * c * self.GRIDAREA_SIZE[1] / self.CLMNS - 1)
			pygame.draw.line(screen, color, start_pos, end_pos, width)
	
	def calc_lu(self, x, y):
		return int(1.0 * x * self.GRIDAREA_SIZE[0] / self.CLMNS), int(1.0 * y * self.GRIDAREA_SIZE[1] / self.ROWS)
	
	def calc_text_pos(self, x, y):
		pos = self.calc_lu(x, y)
		return int(pos[0] + 1.0 * self.GRIDAREA_SIZE[0] / self.ROWS / 6), int(pos[1] + 1.0 * self.GRIDAREA_SIZE[1] / self.CLMNS * 3 / 8)

	def calc_center(self, x, y):
		pos = self.calc_lu(x, y)
		return int(pos[0] + 1.0 * self.GRIDAREA_SIZE[0] / self.ROWS / 2), int(pos[1] + 1.0 * self.GRIDAREA_SIZE[1] / self.CLMNS / 2)
	
	def circle(self, screen, x, y, color=(0, 0, 0), scale=1, width=0, text=''):
		pos = self.calc_center(x, y)
		radius = int(min(1.0 * self.GRIDAREA_SIZE[0] / self.CLMNS / 2, 1.0 * self.GRIDAREA_SIZE[1] / self.ROWS / 2) * scale)
		pygame.draw.circle(screen, color, pos, radius, width)
		if text:
			text_pos = self.calc_text_pos(x, y)
			if width == 0:
				x = self.font.render(text, False, (255, 255, 255))
			else:
				x = self.font.render(text, False, color)
			screen.blit(x, text_pos)
	
	def rect(self, screen, x, y, color=(0, 0, 0), scale=1, width=0, text=''):
		pos = self.calc_center(x, y)
		h, l = int(1.0 * self.GRIDAREA_SIZE[0] / self.CLMNS * scale), int(1.0 * self.GRIDAREA_SIZE[1] / self.ROWS * scale)
		pos = pos[0] - h / 2, pos[1] - l / 2
		rct = pygame.Rect(pos[0], pos[1], h, l)
		pygame.draw.rect(screen, color, rct, width)
		if text:
			text_pos = self.calc_text_pos(x, y)
			if width == 0:
				x = self.font.render(text, False, (255, 255, 255))
			else:
				x = self.font.render(text, False, color)
			screen.blit(x, text_pos)
	
	def ellipse(self, screen, x, y, color=(0, 0, 0), scale=1, width=0, text=''):
		pos = self.calc_center(x, y)
		h, l = int(1.0 * self.GRIDAREA_SIZE[0] / self.CLMNS * scale), 0.8 * int(1.0 * self.GRIDAREA_SIZE[1] / self.ROWS * scale)
		pos = pos[0] - h / 2, pos[1] - l / 2
		rct = pygame.Rect(pos[0], pos[1], h, l)
		pygame.draw.ellipse(screen, color, rct, width)
		if text:
			text_pos = self.calc_text_pos(x, y)
			if width == 0:
				x = self.font.render(text, False, (255, 255, 255))
			else:
				x = self.font.render(text, False, color)
			screen.blit(x, text_pos)
