
import numpy as np
import matplotlib.pyplot as plt
from fluidfoam import readscalar
from fluidfoam import readvector


sol = '../'
timenamearray = [str(i) for i in range(50, 1050, 50)]

filter_size = 64

T_dict = {}
p_dict = {}
phi_dict = {}
p_rgh_dict = {}
ux_dict = {}
uy_dict = {}


for timename in timenamearray:
	T_ = np.array(readscalar(sol, timename, 'T'))
	T_ = np.flipud(np.reshape(T_, (filter_size,filter_size)))
	T_dict['T'+timename] = T_
	
	p_ = np.array(readscalar(sol, timename, 'p'))
	p_ = np.flipud(np.reshape(p_, (filter_size,filter_size)))
	p_dict['p'+timename] = p_
	
	p_rgh_ = np.array(readscalar(sol, timename, 'p_rgh'))
	p_rgh_ = np.flipud(np.reshape(p_rgh_, (64,64)))
	p_rgh_dict['p_rgh'+timename] = p_rgh_
	
	phi_ = np.array(readscalar(sol, timename, 'phi'))
	#phi_ = np.flipud(np.reshape(phi_, (64,64)))
	phi_dict['phi'+timename] = phi_
	
	U_ = np.array(readvector(sol, timename, 'U'))
	ux_ = np.flipud(np.reshape(U_[0], (filter_size,filter_size)))
	uy_ = np.flipud(np.reshape(U_[1], (filter_size,filter_size)))
	ux_dict['ux'+timename] = ux_
	uy_dict['uy'+timename] = uy_
	

#print(T_dict['T50'])

plt.imshow(uy_dict['uy200'])
plt.show()

