"""
Methods to read and visualize PLUTO's output.
"""

import numpy as np
import random








class Pluto:
	"""
	Class that defines a population of agents infected by an epidemic.
	
	The object's attributes are the properties of the agents:
	
	- x,y: position
	- vx,vy: velocities
	- health
	- sick: is the agent sick?
	"""
		
	def __init__(self, *arg,**args):			
		# mesh,  and velocities
		'''
		if d.n1>1: 
			self.x1,self.v1,self.n1,self.dx1=d.x1,d.vx1,d.n1,d.dx1
			self.speed=numpy.sqrt(self.v1*self.v1)
		if d.n2>1: 
			self.x2,self.v2,self.n2,self.dx2=d.x2,d.vx2,d.n2,d.dx2
			self.speed=numpy.sqrt(self.v1*self.v1 + self.v2*self.v2)
		if d.n3>1: 
		'''
		self.x1,self.v1,self.n1,self.dx1=d.x1,d.vx1,d.n1,d.dx1
		self.x2,self.v2,self.n2,self.dx2=d.x2,d.vx2,d.n2,d.dx2
		self.x3,self.v3,self.n3,self.dx3=d.x3,d.vx3,d.n3,d.dx3
		self.speed=numpy.sqrt(self.v1*self.v1 + self.v2*self.v2 + self.v3*self.v3)

		# polar coordinates (code units in spherical coords)
		self.r=self.x1
		self.th=-(self.x2-numpy.pi/2.) # spherical angle => polar angle

		# convenient meshgrid arrays
		self.X1,self.X2=numpy.meshgrid(self.x1,self.x2)
		self.DX1,self.DX2=numpy.meshgrid(self.dx1,self.dx2)
		self.R,self.TH=numpy.meshgrid(self.r,self.th)
		self.X,self.Y=nmmn.misc.pol2cart(self.R,self.TH)

		# fluid variables
		self.p=d.prs # pressure
		self.rho=d.rho # volume density
		self.getgamma() # gets value of adiabatic index
		self.entropy=numpy.log(self.p/self.rho**self.gamma)
		self.am=self.v3.T*self.X1*numpy.sin(self.X2) # specific a. m., vphi*r*sin(theta)
		self.Be=self.speed.T**2/2.+self.gamma*self.p.T/((self.gamma-1.)*self.rho.T)-1./self.X1	# Bernoulli function
		self.Omega=self.v3.T/self.X1	# angular velocity

		# misc. info
		self.t=d.SimTime
		self.pp =d # pypluto object
		self.frame=i
		self.vars=d.vars
		self.geometry=d.geometry

		# sound speed
		#self.soundspeed() # computes numerical cs (no need to specify EoS)
		self.cs=numpy.sqrt(self.gamma*self.p/self.rho)

		# mach number
		if d.n1>1: self.mach1=self.v1/self.cs
		if d.n2>1: self.mach2=self.v2/self.cs
		if d.n3>1: self.mach3=self.v3/self.cs
		self.mach=self.speed/self.cs

		# accretion rates as a function of radius
		self.getmdot() # net accretion rate, self.mdot
		self.getmdotin() # inflow, self.mdotin
		self.getmdotout() # outflow, self.mdotout

		# total mass in computational volume, self.mass
		self.getmass()





