import numpy as np
import xarray as xr
import pyqg
from numpy.random import Generator, MT19937, SeedSequence
import os
import yaml

# parameter for randomness
n = os.getenv('SLURM_ARRAY_TASK_ID')
pickup_file = os.environ['PICKUP_FILE']
config_file = os.environ['CONFIG_FILE']

# initial conditions from equilibrium run
ds_initial = xr.open_dataset(pickup_file)
initial_PV = ds_initial.q.values

# model configuration
with open(config_file) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

def ensemble_generator(initial_PV, n):
    
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
    datasets = []
    for snapshot in m.run_with_snapshots(tsnapstart=m.t, tsnapint=m.dt):
        model = m.to_dataset()
        model = model.assign(q=(('time','lev','y','x'), m.q.copy()[np.newaxis,...]))
        datasets.append(model)

    ds = xr.concat(datasets, dim='time')
    ds = ds.expand_dims(dim='ensemble_member')
    ds['ensemble_member'] = [int(n)]
    
    # Save model to netCDF
    fn = '/burg/abernathey/users/hillary/QG_proto_EM_'+ str('%03d'%int(n)) +'.nc'
    ds.to_netcdf(fn, engine='h5netcdf', invalid_netcdf=True)
    
# generate ensemble
ensemble_generator(initial_PV, n)