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
		self.nagents=d['nagents']

		# positions
		self.x=np.random.uniform(d['xbox0'],d['xbox1'],self.nagents)
		self.y=np.random.uniform(d['ybox0'],d['ybox1'],self.nagents)

		# velocities initialized all the same, with random directions
		self.theta=np.random.uniform(0,2*np.pi,self.nagents)
		self.vx=np.ones_like(x)*np.cos(theta)
		self.vy=np.ones_like(x)*np.sin(theta)

		# health:
		# - 0: healthy
		# - 1: infected
		# - 2: recovering
		self.health=np.zeros(self.nagents,dtype=int)

		self.init_infect()






	def init_infect():
		# randomly initialize a fraction of the agents as infected
		# list of random elements, non-repeating
		i=random.sample(range(self.nagents),int(self.sick*self.nagents))
		
		self.health[i]=1

