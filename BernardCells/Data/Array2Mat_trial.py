
import numpy as np
from scipy.sparse import coo_matrix

from fluidfoam import readscalar

import csv
import matplotlib.pyplot as plt
  
row  = np.array([0, 0.01, 0.02, 0.03])
col  = np.array([0, 0.02, 0.01, 0.01])
data = np.array([4, 5, 7, 9])

ans = coo_matrix((data, (row, col)), shape=(4, 4), dtype=np.float32).toarray()

#ans = coo_matrix((p, (x, y)), shape=(20, 5)).toarray()
#print(ans)
  

with open('test.csv','rt')as f:
  data = csv.reader(f)
  for row in data:
        pass#print(row)
        
x, y, z, p = [], [], [], []
        
reader = csv.DictReader(open("test.csv"))
for raw in reader:
    x.append(float(raw['Points:0']))
    y.append(float(raw['Points:1']))
    z.append(float(raw['Points:2']))
    
    p.append(float(raw['p']))


def make_grid(x, y, z):
    '''
    Takes x, y, z values as lists and returns a 2D numpy array
    '''
    dx = abs(np.sort(list(set(x)))[1] - np.sort(list(set(x)))[0])
    dy = abs(np.sort(list(set(y)))[1] - np.sort(list(set(y)))[0])
    i = ((x - min(x)) / dx).astype(int) # Longitudes
    j = ((y - max(y)) / dy).astype(int) # Latitudes
    grid = np.nan * np.empty((len(set(j)),len(set(i))))
    grid[-j, i] = z # if using latitude and longitude (for WGS/West)
    return grid
    
    
ans = make_grid(np.array(x), np.array(y), np.array(p))


####################################################################
sol = '../'
timename = '50'

T50 = np.array(readscalar(sol, timename, 'T'))

T50 = np.reshape(T50, (64,64))
T50 = np.flipud(T50)


plt.imshow(T50)
plt.show()

