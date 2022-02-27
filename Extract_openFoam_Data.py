import os
import numpy as np
import matplotlib.pyplot as plt
from fluidfoam import readscalar
from fluidfoam import readvector
from sklearn.model_selection import train_test_split


def Extract_openFoam_Data(parent_dir, Para_array, timenamearray, filter_size=64):
	
	BernardCells = {}

	for Para in Para_array:
		directory = 'BernardCells_T'+str(Para)
		path = os.path.join(parent_dir, directory)

		T_dict = {}
		p_dict = {}
		phi_dict = {}
		p_rgh_dict = {}
		ux_dict = {}
		uy_dict = {}

		for timename in timenamearray:
			T_ = np.array(readscalar(path, timename, 'T'))
			T_ = np.flipud(np.reshape(T_, (filter_size,filter_size)))
			T_dict['t='+timename] = T_
			
			p_ = np.array(readscalar(path, timename, 'p'))
			p_ = np.flipud(np.reshape(p_, (filter_size,filter_size)))
			p_dict['t='+timename] = p_
			
			p_rgh_ = np.array(readscalar(path, timename, 'p_rgh'))
			p_rgh_ = np.flipud(np.reshape(p_rgh_, (64,64)))
			p_rgh_dict['t='+timename] = p_rgh_
			
			phi_ = np.array(readscalar(path, timename, 'phi'))
			#phi_ = np.flipud(np.reshape(phi_, (64,64)))
			phi_dict['t='+timename] = phi_
			
			U_ = np.array(readvector(path, timename, 'U'))
			ux_ = np.flipud(np.reshape(U_[0], (filter_size,filter_size)))
			uy_ = np.flipud(np.reshape(U_[1], (filter_size,filter_size)))
			ux_dict['t='+timename] = ux_
			uy_dict['t='+timename] = uy_
		
		BernardCells['_T'+str(Para)] = {'T': T_dict, 
										'p': p_dict, 
										'p_rgh': p_rgh_dict, 
										'ux': ux_dict, 
										'uy': uy_dict}


	# plt.imshow(BernardCells['_T320']['T']['t=200'])
	# plt.show()


	Data_T = np.zeros((len(Para_array), len(timenamearray), filter_size, filter_size))
	Data_p = np.zeros((len(Para_array), len(timenamearray), filter_size, filter_size))
	Data_ux = np.zeros((len(Para_array), len(timenamearray), filter_size, filter_size))
	Data_uy = np.zeros((len(Para_array), len(timenamearray), filter_size, filter_size))
	Data_p_rgh = np.zeros((len(Para_array), len(timenamearray), filter_size, filter_size))

	for c, Para in enumerate(Para_array):
		for t, timename in enumerate(timenamearray):
			Data_T[c, t, :, :] = BernardCells['_T'+str(Para)]['T']['t='+timename]
			Data_p[c, t, :, :] = BernardCells['_T'+str(Para)]['p']['t='+timename]
			Data_ux[c, t, :, :] = BernardCells['_T'+str(Para)]['ux']['t='+timename]
			Data_uy[c, t, :, :] = BernardCells['_T'+str(Para)]['uy']['t='+timename]
			Data_p_rgh[c, t, :, :] = BernardCells['_T'+str(Para)]['p_rgh']['t='+timename]


	Train_T,Test_T, Train_p,Test_p, Train_ux,Test_ux, Train_uy,Test_uy, Train_p_rgh,Test_p_rgh = train_test_split(Data_T, Data_p, Data_ux, Data_uy, Data_p_rgh, shuffle=True)

	print(Train_T.shape, Test_T.shape)


	np.savez('TrainingData.npz',T=Train_T,
								p=Train_p,
								ux=Train_ux,
								uy=Train_uy,
								p_rgh=Train_p_rgh)
						

	np.savez('TestingData.npz', T=Test_T,
								p=Test_p,
								ux=Test_ux,
								uy=Test_uy,
								p_rgh=Test_p_rgh)

	Load_TraningData = np.load('TrainingData.npz')


	# plt.imshow(Train_T[0,19,:,:])
	# plt.show()





if __name__ == '__main__':
	
	parent_dir = '../BernardCells_T'


	timenamearray = [str(i) for i in range(10, 201, 10)]
	Para_array = range(320, 1001, 20)
	filter_size = 64

	Extract_openFoam_Data(parent_dir, Para_array, timenamearray, filter_size)
