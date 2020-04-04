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
		# velocity angle
		theta=np.random.uniform(0,2*np.pi,nagents)
		# velocity module
		vx=np.ones_like(x)*np.cos(theta)
		vy=np.ones_like(x)*np.sin(theta)

		# health:
		# - 0: healthy
		# - 1: infected but will ultimately survive
		# - 2: infected and dying
		# - 3: dead (gets removed from simulation)
		# - 4: recovered (TBD)
		health=np.zeros(nagents,dtype=int)

		# - 0: will survive
		# - 1: dying
		dying=health

		# death timer
		tdeath=np.zeros_like(x)

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

		# decides which infected agents will die
		# step 1: finds newly infected agents
		mask=np.zeros_like(self.health)
		mask[self.health==1]=1
		# step 2: makes the decision
		self.death_note(mask)




	def death_note(self,mask):
		"""
		Decides which infected agents will die. If the agent is unlucky, 
		starts a countdown for the death.

		mask: array with same size as nagents. 1 if newly-infected
		"""
		# generates random numbers, uniformly distributed, that will
		# be used to decide if agents are goind to die
		r=np.random.uniform(0,100,self.nagents)

		# the decision
		i=np.where((mask==1)&(r<=self.pars['death_ratio']*100.))
		if np.size(i)>0: 
			self.health[i]=2





	def update(self,dt):
		"""
		Update state variables.
		"""
		self.bounce_walls()
		self.move(dt)
		self.proximity_check()





	def bounce_walls(self):
		"""
		Perform reflections off the walls.
		"""
		# bounce off the walls
		# on x
		i=np.where((self.x<self.pars['xbox0']) | (self.x>self.pars['xbox1']))
		if np.size(i)>0: self.vx[i]=-self.vx[i]
		# on y
		j=np.where((self.y<self.pars['ybox0']) | (self.y>self.pars['ybox1']))
		if np.size(j)>0: self.vy[j]=-self.vy[j]

		self.theta=np.arctan2(self.vy,self.vx)




	def move(self,dt):
		"""
		steps position
		"""
		self.x=self.x+self.vx*dt
		self.y=self.y+self.vy*dt



	def proximity_check(self):
		"""
		Checks which particles are close to which. This is essential
		for computing infections due to proximity and scatterings.

		There is room for accelerating this routine.
		"""
		# goes through each particle
		for p in range(self.nagents):
		    # position of current particle
		    xp,yp=self.x[p],self.y[p]
		    # distances to current particle
		    distance=np.sqrt((xp-self.x)**2+(yp-self.y)**2)
		    # mark current particle to avoid issues
		    distance[p]=self.pars['xbox1']**2
		    
			# find those agents that are sick and close to the current one
		    i=np.where((distance<=self.pars['dinfect']) & (self.health==1))

		    # if there is at least one person infected close to the current 
		    # agent and it is healthy...
		    if np.size(i)>0 and self.health[p]==0:
		    	self.infects(p)
		    # otherwise just bounces the agents off each other
		    elif np.size(i)>0:
		    	self.bounce_agent(p,i,distance)





	def infects(self,i):
		"""
		Computes nature of contagion for the current agent i.
		"""
		# creates mask indicating the current agent who was just infected
		mask=np.zeros_like(self.health)
		mask[i]=1

		# will the newly infected die?
		self.death_note(mask)

	    # infects by proximity
		if self.health[i]!=2:
			self.health[i]=1





	def bounce_agent(self,i,j,distance):
		"""
		Elastic collisions between agents

		i: index of current particle (agent 1)
		j: indexes of all particles which are in proximity for a collision
		distance: array of distances between particle i and all others

		Ref. for elastic collision formulas: https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects

		"""
		# gets closest particle to i (i.e. agent 2)
		imin=j[0][distance[j].argmin()]

		# gets agent 1's position in the frame centered in agent 2
		x1=self.x[i]-self.x[imin]
		y1=self.y[i]-self.y[imin]

		# get the angle of the line connecting the two agents
		theta=np.arctan2(y1,x1)

		# gets the perpendicular angle (the contact angle)
		phi=theta+np.pi/2.

		# compute the new velocity angles based on elastic scattering formulas
		# notice that below I assume that the masses of the particles are equal. 
		# if this assumption is violated, then the expression below does not 
		# apply
		#
		# velocity modules before scattering
		v1=np.sqrt(self.vx[i]**2+self.vy[i]**2)
		v2=np.sqrt(self.vx[imin]**2+self.vy[imin]**2)
		# scattered agent 1
		self.vx[i]=v2*np.cos(self.theta[imin]-phi)*np.cos(phi)+v1*np.sin(self.theta[i]-phi)*np.cos(phi+np.pi/2.)
		self.vy[i]=v2*np.cos(self.theta[imin]-phi)*np.sin(phi)+v1*np.sin(self.theta[i]-phi)*np.sin(phi+np.pi/2.)
		self.theta[i]=np.arctan2(self.vy[i],self.vx[i])
