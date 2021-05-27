import numpy as np
import xarray as xr
import pyqg
from numpy.random import Generator, MT19937, SeedSequence
import os
import yaml

# ensemble member id & parameter for randomness
n = os.getenv('SLURM_ARRAY_TASK_ID') 

# initial conditions from equilibrium run
pickup_file = os.environ['PICKUP_FILE'] 
ds_initial = xr.open_dataset(pickup_file)

# model configuration
config_file = os.environ['CONFIG_FILE'] 
with open(config_file) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

def ensemble_generator(ds_initial, n):
    '''Save ensemble member snapshots at each time step'''
    
    # make a new directory and switch to it
    os.mkdir('/burg/abernathey/users/hillary/'+ str('%03d'%int(n)))
    os.chdir('/burg/abernathey/users/hillary/'+ str('%03d'%int(n)))
    
    # configure model
    m = pyqg.QGModel(tmax=config['tmax'], twrite=config['twrite'], tavestart=config['tavestart'])

    # create an empty array filled with zeros 
    noise = np.zeros_like(ds_initial.q.values)

    # index to the middle of noise and add random perturbation to both levels
    rg = Generator(MT19937(int(n))) 
    noise[:,np.floor(len(ds_initial.x)/2).astype('int'), 
          np.floor(len(ds_initial.y)/2).astype('int')] = config['sig']*rg.random((m.q.shape[0]))

    # set PV anomaly with randomness
    m.set_q(ds_initial.q.values + noise)
    
    # run with snapshots, save model increments as xarray DataSet
    for snapshot in m.run_with_snapshots(tsnapstart=m.t, tsnapint=m.dt):
        model = m.to_dataset()
        model = model.expand_dims(dim='n') # ensemble member n
        model['n'] = [int(n)]
        fn = '/burg/abernathey/users/hillary/'+ str('%03d'%int(n)) +'/QG_proto_EM_'+ str('%03d_%d'%(int(n),model.time.values[0])) +'.nc'
        model.to_netcdf(fn, engine='h5netcdf', invalid_netcdf=True, mode='a')

# generate ensemble
ensemble_generator(ds_initial, n)