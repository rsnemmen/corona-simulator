"""
Methods to read and visualize PLUTO's output.
"""

import numpy as np
import random








class Agents:
	"""
	Class that defines a population of agents infected by an epidemic.
	
	The object's attributes are the properties of the agents:
	
	- x,y: position
	- vx,vy: velocities
	- health
	- sick: is the agent sick?

	d is a dictionary with the initial state for the population.
	"""
		
	def __init__(self, d, *arg,**args):
		nagents=d['nagents']

		# positions
		x=np.random.uniform(d['xbox0'],d['xbox1'],nagents)
		y=np.random.uniform(d['ybox0'],d['ybox1'],nagents)

		# velocities initialized all the same, with random directions
		theta=np.random.uniform(0,2*np.pi,nagents)
		vx=np.ones_like(x)*np.cos(theta)
		vy=np.ones_like(x)*np.sin(theta)

		# health:
		# - 0: healthy
		# - 1: infected
		# - 2: recovering
		health=np.zeros(nagents,dtype=int)

		# assign object attributes
		self.pars=d
		self.x, self.y=x, y
		self.theta=theta
		self.nagents=nagents
		self.vx, self.vy=vx, vy
		self.sick=d['sick']
		self.health=health

		self.init_infect()






	def init_infect(self):
		# randomly initialize a fraction of the agents as infected
		# list of random elements, non-repeating
		i=random.sample(range(self.nagents),int(self.sick*self.nagents))
		
		self.health[i]=1




	def update(self,dt):
		"""
		Update state variables.
		"""
		self.bounce()
		self.move(dt)
		self.infect()





	def bounce(self):
		"""
		Perform reflections off the walls and between agents.
		"""
		# on x
		i=np.where((self.x<self.pars['xbox0']) | (self.x>self.pars['xbox1']))
		if np.size(i)>0: self.vx[i]=-self.vx[i]
		# on y
		j=np.where((self.y<self.pars['ybox0']) | (self.y>self.pars['ybox1']))
		if np.size(j)>0: self.vy[j]=-self.vy[j]




	def move(self,dt):
		"""
		steps position
		"""
		self.x=self.x+self.vx*dt
		self.y=self.y+self.vy*dt



	def infect(self):
		## goes through each particle
		for p in range(self.nagents):
		    # position of current particle
		    xp,yp=self.x[p],self.y[p]
		    # distances to current particle
		    distance=np.sqrt((xp-self.x)**2+(yp-self.y)**2)
		    # mark current particle to avoid issues
		    distance[p]=self.pars['xbox1']**2
		    
		    # find those agents that are sick and close to the current one
		    i=np.where((distance<=self.pars['dinfect']) & (self.health==1))
		         
		    if np.any((distance<=self.pars['dinfect']) & (self.health==1)): 
		        self.health[p]=1