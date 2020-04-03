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

