import math
import pygame as pg
from random import randint
pg.init()

screen_width = 1300
screen_height = 700
screen_title = "АКРЛДН"
framerate = 60

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption(screen_title)

entity_speed = 5.0

points_to_go = []

class Plane():
	def __init__(self, x, y, width, height, color):
		pg.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		#self.rect = (x, y, width, height)

		self.speed = 5
		self.active = False
		self.image = pg.Surface((20, 20))
		self.frame = pg.Rect(0, 0, 20, 20)
		self.rect = self.image.get_rect()
		self.display_surface = screen
		self.rect.center = (x, y)

	def draw(self, screen):
		self.rect = (self.x, self.y, 20, 20)
		pg.draw.rect(screen, self.color, self.rect)

	def move_kb(self):
		keys = pg.key.get_pressed()

		if self.x < 0:
			self.x = 0
		if self.x > screen_width-30:
			self.x = screen_width-30
		if self.y < 0:
			self.y = 0
		if self.y > screen_height-30:
			self.y = screen_height-30
			
		if keys[pg.K_w]:
			self.y -= self.speed
		if keys[pg.K_s]:
			self.y += self.speed
		if keys[pg.K_a]:
			self.x -= self.speed
		if keys[pg.K_d]:
			self.x += self.speed

		self.rect = (self.x, self.y, self.width, self.height)

	def select_me(self, mouse_pos):
		""" It's a method to select the object with a mouse LEFT click. """
		#self.active = self.rect.collidepoint(mouse_pos)
		self.active = True
	def deselect_me(self):
		""" It's a method to select the object with a mouse LEFT click. """
		self.active = False		
		#print('Frame active')
	def draw_frame(self, screen):
		#pg.draw.rect(screen, self.color, self.rect)
		if self.active:
			self.image.fill((100, 100, 200))
			pg.draw.rect(self.image, (0, 255, 0), self.frame, 3)
			#print('frame drawn')
			self.display_surface.blit(self.image, self.rect)						
	

class Entity:
	"""
	It's a class describing the movable object.

	Arguments:
	----------
	display_surface : pg.Surface
		It's a surface on which the object will be drawn.
	x : float
		It's the object's position on the X-axis.
	y : float
		It's the object's position on the Y-axis.

	Attributes:
	----------
	display_surface : pg.Surface
		See part "Arguments". 
	image : pg.Surface
		It's the object's image/ sprite.
	rect : pg.Rect
		It's the object's collision rectangle. Here it detects mouse clicks.
	frame : pg.Rect
		It's a rectangle that is drawn if the object is selected.
	active : bool
		It stores information about the object is selected or not.
	start_pos : list or tuple
		It stores information about the starting point of the motion.
	goal_pos : list or tuple
		It stores information about the ending point of the motion.
	shift : float
		It stores the distance between the starting point of the motion and the object's current position.
	speed : float
		It's the movement speed of the object.
	"""
	def __init__(self, display_surface, x, y, speed=entity_speed, points_to_go=points_to_go):
		self.display_surface = display_surface
		self.image = pg.Surface((20, 20))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.frame = pg.Rect(0, 0, 20, 20)

		self.active = False

		self.start_pos = None
		self.goal_pos = None
		self.shift = 0
		self.speed = entity_speed
		self.color = (100, 200, 100)

		self.x = x
		self.y = y
		self.recty = (x,y,40, 40)
		self.allow_to_move = False

		self.points_to_go = points_to_go
	def select_me(self, mouse_pos):
		""" It's a method to select the object with a mouse LEFT click. """
		self.active = self.rect.collidepoint(mouse_pos)

	def select_route(self, mouse_pos):
		""" It's a method to set up the attributes of movement. """
		if self.active:
			self.reset_route()
			self.start_pos = self.rect.center
			self.goal_pos = mouse_pos

	def reset_route(self):
		""" It's a method to reset the attributes of movement. """
		self.shift = 0
		self.start_pos = None
		self.goal_pos = None

	def next_point(self, start_pos, goal_pos):
		""" It's a method to reset the attributes of movement. """
		self.shift = 0
		self.start_pos = start_pos
		self.goal_pos = goal_pos


	def move_me(self):
		""" It's a method to move the object. """
		#self.start_pos = self.rect.center			
		if self.goal_pos is not None:
			print(f'goal_pos: {self.goal_pos}, start_pos: {self.start_pos}')
			dx = self.goal_pos[0] - self.start_pos[0]
			dy = self.goal_pos[1] - self.start_pos[1]

			distance = math.sqrt(dx*dx + dy*dy)
			self.shift += self.speed

		try:
			if self.shift/distance < 0.99:
				self.rect.center = (self.start_pos[0] + self.shift/distance * dx,
									 self.start_pos[1] + self.shift/distance * dy)
				print(f'going to: {self.goal_pos}')
		except ZeroDivisionError:
				pass	
		return True		


	def move_me_on_spawn(self):
		""" It's a method to move the object. """
		if self.points_to_go:
			self.start_pos = self.points_to_go[0]
			for point in self.points_to_go[1:]:
				for i in range(len(self.points_to_go[1:])):
					self.goal_pos = self.points_to_go[i]
					
					self.move_me()
					#self.start_pos = 
					#print(self.goal_pos)
					#if self.move_me():
					#	i += 1
					#	print('switch')



	def draw_me(self):
		""" It's a method to draw the object on the screen. """
		self.image.fill((100, 200, 100))
		if self.active: pg.draw.rect(self.image, (100, 100, 200), self.frame, 3) #if active => draw frame around selected entity width 3
		self.display_surface.blit(self.image, self.rect)	

	def draw_a50(self):
		""" It's a method to draw the object on the screen. """
		pg.draw.rect(self.image, (100, 200, 100), self.rect)
	
		#self.display_surface.blit(self.image, self.rect)

	def draw(self, screen):
		pg.draw.rect(screen, self.color, self.rect)
		if self.active: pg.draw.rect(self.image, (100, 100, 200), self.frame, 3) #if active => draw frame around selected entity width 3
		#self.display_surface.blit(self.image, self.rect)				
			#self.hitbox = (self.x, self.y, 10, 40) #defining this var again 
			#pygame.draw.rect(window, (255,0,0), self.hitbox,2) # To draw the hit box around the cactus
	def deselect_me(self):
		""" It's a method to select the object with a mouse LEFT click. """
		self.active = False		

class UI:
	def __init__(self, x, y, width=None, height=None, x1=None, y1=None, color=(150,150,150)):
		self.x = x
		self.y = y
		self.x1 = x1
		self.y1 = y1
		self. width = width
		self.height = height
		self.rect = (x, y, width, height)
		self.color = color
		self.hitbox = (0,0, 10, 40)
		self.allow_to_drag = False

	def draw_ui(self, screen):
		pg.draw.rect(screen, self.color, self.rect)

	def draw_slider(self, screen):
		pg.draw.line(screen, (0,0,0), [self.x, self.y], [self.x1, self.y1],5)
	def draw_widget(self, screen):
		self.rect = (self.x, self.y, 10, 30)
		pg.draw.rect(screen, self.color, self.rect)
		pg.draw.rect(screen, (50,50,50), self.rect, 2)
		#self.hitbox = (self.x, self.y, 10, 30)
		#pg.draw.rect(screen, (250,0,0), self.hitbox,1)

def count_speed(x, x1):
	return (x1-x)/1000 * (ui_speed_widget.x - ui_speed_slider.x)

clock = pg.time.Clock()
entity = Entity(screen, 100.5, 100)
test = Entity(screen, 10,10)
coords = (400, 200)
a50 = Plane(400,200,40,40,(100,100,200))
next_tick = 500



#ui_speed_slider = UI()

entity_array, planes_array = [],[]



#entity_array.append(entity)
#entity_array.append(test)
planes_array.append(a50)

ui_frame = UI(0,screen_height-100, screen_width, screen_height-600)
ui_speed_slider = UI(x=100,y=630,x1=200,y1=630)
ui_speed_widget = UI(x=150,y=615,width=10,height=30,color=(200,200,200))
angle = 0
speed = 1
run = True

white = (255,255,255)
black = (0,0,0)


def redrawWindow():
	for plane in planes_array:
		plane.draw(screen)
	a50.draw_frame(screen)
	for entity in entity_array:
		entity.draw_me()
	#test.draw_me()
	ui_frame.draw_ui(screen)
	#UI.draw_slider(UI, screen)
	#pg.draw.line(screen, (0,0,0), [300, 650], [400, 650],5)
	ui_speed_slider.draw_slider(screen)
	ui_speed_widget.draw_widget(screen)
	UI_text()

def move_coords(angle, radius, coords):
	theta = math.radians(angle)
	#print(theta)
	return coords[0] + radius * math.cos(theta), coords[1] + radius * math.sin(theta)


def UI_text():
	global entity_speed

	font = pg.font.Font('C:/Users/Banan/Music/iTunes/Music/9303.ttf',20)
	text = font.render(f"Speed:", True, (0,0,0))
	text_rect = text.get_rect(center=(50,630))
	screen.blit(text, text_rect)

	font = pg.font.Font('C:/Users/Banan/Music/iTunes/Music/9303.ttf',20)
	text = font.render(f"{entity_speed}", True, (0,0,0))
	text_rect = text.get_rect(center=(240,630))
	screen.blit(text, text_rect)	

landscape = pg.image.load("map.jpg").convert()

while run:

	mouse_pos = pg.mouse.get_pos()
	isMouseLC = pg.mouse.get_pressed()
	ticks = pg.time.get_ticks()
	if ticks > next_tick:
		next_tick += speed
		angle += 1 
		coords = move_coords(angle, 2, coords)
		#print(coords)
		#a50.topleft = coords
		a50.x, a50.y = coords[0], coords[1]
		#print(a50.x, a50.y)
		a50.draw(screen)
	for event in pg.event.get():
		if event.type == pg.QUIT:
			quit()
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				quit()
		if event.type == pg.KEYUP:
			if event.key == pg.K_UP:
				entity_random_x, entity_random_y = randint(20, 750), randint(20, 550)
				entity_array.append(Entity(screen, entity_random_x, entity_random_y, points_to_go))
				
				entity = entity_array[-1]
				entity.move_me_on_spawn()
				print(entity.points_to_go)
				points_to_go.clear()		
			if event.key == pg.K_DOWN:
				entity_array.pop()
						
		if event.type == pg.MOUSEMOTION:
				#print('dragging')
				if ui_speed_widget.allow_to_drag == True:
					#if mouse_pos[0] > ui_speed_widget.x and mouse_pos[0] < ui_speed_widget.x+10:
					#	if mouse_pos[1] > ui_speed_widget.y and mouse_pos[1] < ui_speed_widget.y+30:
					entity_speed = round(count_speed(ui_speed_slider.x, ui_speed_slider.x1),2)
					print(entity_speed)
					if ui_speed_widget.x >= ui_speed_slider.x and ui_speed_widget.x <= ui_speed_slider.x1:
						ui_speed_widget.x = mouse_pos[0]
					if ui_speed_widget.x < ui_speed_slider.x:
						ui_speed_widget.x = ui_speed_slider.x
					if ui_speed_widget.x > ui_speed_slider.x1:
						ui_speed_widget.x = ui_speed_slider.x1

					#if ui_speed_widget.x < 							
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				#print('mouse down')
				if mouse_pos[1] < screen_height-100:
					points_to_go.append(mouse_pos)
					print(points_to_go)
				if mouse_pos[0] > ui_speed_widget.x and mouse_pos[0] < ui_speed_widget.x+10:
					if mouse_pos[1] > ui_speed_widget.y and mouse_pos[1] < ui_speed_widget.y+30:
						ui_speed_widget.allow_to_drag = True
						print('True')
				for entity in entity_array:
					entity.select_me(mouse_pos)
				a50.select_me(mouse_pos)
				#test.select_me(mouse_pos)
			if event.button == 2:
				for entity in entity_array:
					entity.deselect_me()
				a50.deselect_me()		
			if event.button == 3:
				for entity in entity_array:
					entity.select_route(mouse_pos)
				#test.select_route(mouse_pos)
		if event.type == pg.MOUSEBUTTONUP:
			if event.button == 1:
				ui_speed_widget.allow_to_drag = False		
	for entity in entity_array:

		entity.move_me()
	#test.move_me()
	#a50.move_me()
	#a50.move_kb()

	#screen.fill((200, 200, 200))
	screen.blit(landscape, (0,0))
	
	#a50.draw()
	redrawWindow()
	pg.display.flip()
	clock.tick(framerate)
	pg.display.update()

'''		
if self.points_to_go:
	for point in self.points_to_go:
		self.goal_pos = point
		print(point)
		print(self.goal_pos[0], self.goal_pos[1])
		dx = self.goal_pos[0] - self.start_pos[0]
		dy = self.goal_pos[1] - self.start_pos[1]

		distance = math.sqrt(dx*dx + dy*dy)
		self.shift += self.speed

		if self.shift/distance < 0.99:
			self.rect.center = (self.start_pos[0] + self.shift/distance * dx,
								 self.start_pos[1] + self.shift/distance * dy)
		else:
			self.rect.center = (self.goal_pos[0], self.goal_pos[1])
			self.next_point(self.goal_pos[0], self.goal_pos[1])
'''		

'''
		if self.points_to_go:
			self.start_pos = (0,0)	
			for point in self.points_to_go:
				#for i in range(len(self.points_to_go)):
				#come = False
				#while not come:
				
				self.goal_pos = point
				print(self.start_pos, self.goal_pos)
				#print(self.goal_pos[0], self.goal_pos[1])
				dx = self.goal_pos[0] - self.start_pos[0]
				dy = self.goal_pos[1] - self.start_pos[1]

				distance = math.sqrt(dx*dx + dy*dy)
				self.shift += self.speed
				try:
					if self.shift/distance < 0.99:
						self.rect.center = (self.start_pos[0] + self.shift/distance * dx,
											 self.start_pos[1] + self.shift/distance * dy)
				except ZeroDivisionError:
					pass #lol	
					#else:
					#	come = True
				#else:
				self.rect.center = (self.goal_pos[0], self.goal_pos[1])
				#self.next_point(self.goal_pos[0], self.goal_pos[1])
				self.start_pos = self.goal_pos
		self.allow_to_move = True
		self.points_to_go.clear()
'''