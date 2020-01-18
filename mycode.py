import pygame
import neat 
import time
import os
import random
pygame.font.init()


WIN_WIDTH=500
Win_Height=700
Floor=630

GEN=0

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

		d=self.vel*(self.tick_count) + 1.5*(self.tick_count)**2
		
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

		if (self.image_count<=self.Animation_time):
			self.img=self.imgs[0]
		elif(self.image_count<=self.Animation_time*2):
			self.img=self.imgs[1]	
		elif(self.image_count<=self.Animation_time*3):
			self.img=self.imgs[2]	
		elif(self.image_count<=self.Animation_time*4):
			self.img=self.imgs[1]
		elif(self.image_count==self.Animation_time*4 +1):
			self.img=self.imgs[0]									
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
		# self.gap=100

		self.top=0
		self.bottom=0
		self.Pipe_Top=pygame.transform.flip(Pipe_imgs,False,True)
		self.Pipe_Bottom=Pipe_imgs

		self.passed=False
		self.set_height()

	def set_height(self):
		self.height=random.randrange(50,450)
		self.top=self.height - self.Pipe_Top.get_height()	
		self.bottom=self.height + self.Gap

	def move(self):
		self.x-=self.Vel

	def draw(self,win):
		win.blit(self.Pipe_Top,(self.x,self.top))
		win.blit(self.Pipe_Bottom,(self.x,self.bottom))
			
	def collide(self,bird):
		bird_mask=bird.get_mask()
		top_mask=pygame.mask.from_surface(self.Pipe_Top)
		bottom_mask=pygame.mask.from_surface(self.Pipe_Bottom)

		top_offset=(self.x-bird.x,self.top - round(bird.y))
		bottom_offset=(self.x-bird.x,self.bottom - round(bird.y))

		b_point=bird_mask.overlap(bottom_mask,bottom_offset)
		t_point=bird_mask.overlap(top_mask,top_offset)

		if(t_point or b_point):
			return True
		
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



def draw_window(win,birds,pipes,base,score,gen):
	win.blit(Bg_img,(0,0))

	for pipe in pipes:
		pipe.draw(win)

	
	base.draw(win)	
	for bird in birds:
		bird.draw(win)
		

	
	text=Stat_Font.render("Score: "+str(score),1,(255,255,255))
	win.blit(text,(WIN_WIDTH-10-text.get_width(),10))


	score_label= Stat_Font.render("Gens: " + str(gen),1,(255,255,255))
	win.blit(score_label, (10, 10))
	pygame.display.update()	

def main(genomes,config):

	nets=[]
	ge=[]
	birds=[]

	global GEN
	GEN+=1
	for _,g in genomes:
		net=neat.nn.FeedForwardNetwork.create(g,config)
		nets.append(net)
		birds.append(Bird(230,350))
		g.fitness=0
		ge.append(g)


	base=Base(Floor)
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
				pygame.quit()
				quit()	
				break		


		pipe_ind=0
		if(len(birds))>0:
			if(len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].Pipe_Top.get_width()):
				pipe_ind=1
		else:
			run =False	
		

		for x,bird in enumerate(birds):
			ge[x].fitness+=0.1
			bird.move()

			output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

			if(output[0]>0.5):
				bird.jump()


		base.move()		

		add_pipe=False
		rem=[]

		for pipe in pipes:
			pipe.move()

			for x,bird in enumerate(birds):
				if (pipe.collide(bird)):
					ge[x].fitness-=1
					birds.pop(x)
					nets.pop(x)
					ge.pop(x)
			
			if (not pipe.passed and pipe.x< bird.x):
				pipe.passed=True
				add_pipe=True

			if(pipe.x + pipe.Pipe_Top.get_width()<0):
				rem.append(pipe)			

			

		if(add_pipe):
			score+=1
			for g in ge:
				g.fitness+=5
			pipes.append(Pipe(WIN_WIDTH))

		for r in rem:
			pipes.remove(r)	

		for x,bird in enumerate(birds):
			if(bird.y+bird.img.get_height()-10 >=Floor or bird.y<0):
				birds.pop(x)
				nets.pop(x)
				ge.pop(x)

		base.move()
		draw_window(win,birds,pipes,base,score,GEN)

	

def run(config_file):

	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
	p = neat.Population(config)

		    # Add a stdout reporter to show progress in the terminal.
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
		    #p.add_reporter(neat.Checkpointer(5))

		    # Run for up to 50 generations.
	winner=p.run(main, 50)

	print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
	local_dir=os.path.dirname(__file__)
	config_path=os.path.join(local_dir,"config.txt")
	run(config_path)	



