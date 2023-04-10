#!/usr/bin/env python
# coding: utf-8

# In[ ]:
if __name__ == '__main__':

    import numpy as np
    import matplotlib.pyplot as plt
    import pymc as pm
    from   astropy.io import fits
    import os
    import argparse


    # In[ ]:


    parser = argparse.ArgumentParser(description="K8s toy model")
    parser.add_argument("--run_id", default=None, type=str, required=True)
    parser.add_argument("--data_dir", default=None, type=str, required=True)
    parser.add_argument("--output_dir", default=None, type=str, required=True)

    args = parser.parse_args()

    run_id = int(args.run_id)
    data_dir = args.data_dir
    output_dir = args.output_dir


    # In[ ]:


    #run_id = 3
    #data_dir = '/Users/research/projects/k8s-test/data/'
    #output_dir = '/Users/research/projects/k8s-test/results/'


    # In[ ]:


    # load data and run linear regression
    fname = os.path.join(data_dir, 'data_{0}.txt'.format(str(run_id).zfill(3)))
    data = np.loadtxt(fname).T
    x, y = data

    with pm.Model() as model:
        m = pm.Uniform("m", -5, 5)
        b = pm.Uniform("b", -5, 5)

        obs = pm.Normal("obs", m*x + b, observed=y)

    with model:
        trace = pm.sample(chains=2, tune=1000, draws=1000)


    # In[ ]:


    # output posterior chains as .fits file
    primary_hdu = fits.PrimaryHDU()
    header = primary_hdu.header
    header['RUN_ID']  = run_id
    header['NCHAINS'] = trace.sample_stats.dims['chain']
    header['SAMPTIME'] = trace.sample_stats.attrs['sampling_time']

    primary_hdu.header = header

    hdulist = []
    hdulist.append(primary_hdu)

    hdulist.append(fits.ImageHDU(np.array(trace.posterior.m), name='M'))
    hdulist.append(fits.ImageHDU(np.array(trace.posterior.b), name='B'))

    hdulist = fits.HDUList(hdulist)
    
    obs = pm.Normal("obs", m*x + b, observed=y)
    
    os.mkdirs(output_dir, exist_ok=True)
    fname = os.path.join(output_dir, 'results_{0}.fits'.format(str(run_id).zfill(3)))

    hdulist.writeto(fname, overwrite=True)


    # In[ ]: