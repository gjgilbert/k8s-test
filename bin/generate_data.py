#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt


# In[2]:


path = '/Users/research/projects/k8s-test/'

Nobj = 7
Npts = 100

ms = np.random.uniform(-3,3,size=Nobj)
bs = np.random.uniform(-3,3,size=Nobj)

for i in range(Nobj):
    fname = path + 'data/data_{0}.txt'.format(str(i).zfill(3))
    
    x = np.linspace(0,3,Npts)
    y = ms[i]*x + bs[i] + np.random.normal(size=Npts)
    
    np.savetxt(fname, np.vstack([x,y]).T)


# In[ ]:




