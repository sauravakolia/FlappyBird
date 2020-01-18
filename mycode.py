import pygame
import neat 
import time
import os
import random
pygame.font.init()


WIN_WIDTH=400
Win_Height=700

Bird_imgs=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
Pipe_imgs=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
Base_imgs=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
Bg_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

Stat_Font=pygame.font.SysFont("comicsans",50)

class Bird:
	imgs=Bird_imgs
	Rot_vel=20
	Max_rotation=25
	Animation_time=5

	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.tilt=0
		self.tick_count=0
		self.vel=0
		self.height=self.y
		self.image_count=0
		self.img=self.imgs[0]
	
	def jump(self):
		self.vel=-10.5
		self.tick_count=0
		self.height=self.y

	def move(self):
		self.tick_count+=1

		d=self.vel*self.tick_count + 1.5*self.tick_count**2
		
		if d>=16:
			d=16

		if d<0:
			d=-2

		self.y=self.y+d

		if(d<0 or self.y<self.height+50):
			if(self.tilt<self.Max_rotation):
				self.tilt=self.Max_rotation

		else:
			if(self.tilt>-90):
				self.tilt-=self.Rot_vel		

	def draw(self,win):
		self.image_count+=1

		if (self.image_count<self.Animation_time):
			self.img=self.imgs[0]
		elif(self.image_count<self.Animation_time*2):
			self.img=self.imgs[1]	
		elif(self.image_count<self.Animation_time*3):
			self.img=self.imgs[1]	
		elif(self.image_count<self.Animation_time*3):
			self.img=self.imgs[1]	
		elif(self.image_count<self.Animation_time*4):
			self.img=self.imgs[1]
		elif(self.image_count<self.Animation_time*4 +1):
			self.img=self.imgs[1]									
			self.image_count=0

		if (self.tilt <=-80):
			self.img=self.imgs[1]
			self.image_count=self.Animation_time*2	

		rotated_image=pygame.transform.rotate(self.img,self.tilt)
		new_rect=rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)	
		win.blit(rotated_image,new_rect.topleft)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)


class Pipe():
	Gap=200
	Vel=5

	def __init__(self,x):
		self.x=x
		self.height=0
		self.gap=100

		self.top=0
		self.bottom=0
		self.Pipe_Top=pygame.transform.flip(Pipe_imgs,False,True)
		self.Pipe_Bottom=Pipe_imgs

		self.passed=False
		self.set_height()

	def set_height(self):
		self.height=random.randrange(50,450)
		self.top=self.height-self.Pipe_Top.get_height()	
		self.bottom=self.height+self.Gap

	def move(self):
		self.x-=self.Vel

	def draw(self,win):
		win.blit(self.Pipe_Top,(self.x,self.top))
		win.blit(self.Pipe_Bottom,(self.x,self.bottom))
			
	def collide(self,bird):
		bird_mask=bird.get_mask()
		top_mask=pygame.mask.from_surface(self.Pipe_Bottom)
		bottom_mask=pygame.mask.from_surface(self.Pipe_Bottom)

		top_offset=(self.x-bird.x,self.top-round(bird.y))
		bottom_offset=(self.x-bird.x,self.bottom-round(bird.y))

		b_point=bird_mask.overlap(bottom_mask,bottom_offset)
		t_point=bird_mask.overlap(bottom_mask,bottom_offset)

		if(t_point or b_point):
			return True
		else:
			return False	



class Base:
	Vel=5
	Width=Base_imgs.get_width()
	img=Base_imgs

	def __init__(self,y):
		self.y=y
		self.x1=0
		self.x2=self.Width

	def move(self):	
		self.x1-=self.Vel
		self.x2-=self.Vel
		

		if(self.x1+self.Width <0):
			self.x1=self.x2 +self.Width

		if(self.x2+self.Width <0):
			self.x2=self.x1 + self.Width

	def draw(self,win):
		win.blit(self.img,(self.x1,self.y))
		win.blit(self.img,(self.x2,self.y))			

def draw_window(win,bird,pipes,base,score):
	win.blit(Bg_img,(0,0))

	for pipe in pipes:
		pipe.draw(win)

	text=Stat_Font.render("Score: "+str(score),1,(255,255,255))
	win.blit(text,(WIN_WIDTH-10-text.get_width(),10))

	base.draw(win)	
	bird.draw(win)
	pygame.display.update()		

def main():
	bird=Bird(230,350)
	base=Base(630)
	pipes=[Pipe(500)]

	win=pygame.display.set_mode((WIN_WIDTH,Win_Height))
	clock=pygame.time.Clock()
	score=0
	run=True
	while run:
		clock.tick(30)
		for event in pygame.event.get():
			if (event.type==pygame.QUIT):
				run=False

		# bird.move()
		add_pipe=False
		rem=[]
		for pipe in pipes:
			if (pipe.collide(bird)):
				pass
			if(pipe.x + pipe.Pipe_Top.get_width()<0):
				rem.append(pipe)	
			if (not pipe.passed and pipe.x<bird.x):
				pipe.passed=True
				add_pipe=True

			pipe.move()
		if(add_pipe):
			score+=1
			pipes.append(Pipe(600))
		for r in rem:
			pipes.remove(r)	

		if(bird.y+bird.img.get_height() >=730):
			pass
		base.move()
		draw_window(win,bird,pipes,base,score)

	pygame.quit()
	quit()			


main()






