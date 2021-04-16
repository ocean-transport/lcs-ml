import numpy as np
import xarray as xr
import pyqg
from numpy.random import Generator, MT19937, SeedSequence
import os

# parameter for randomness
n = os.getenv('SLURM_ARRAY_TASK_ID')

# initial conditions from equilibrium run
ds_initial = xr.open_dataset('/burg/abernathey/users/hillary/QG_equilibrium_proto.nc')
initial_PV = ds_initial.q.values

# model configuration
year = 24*60*60*360.
day = 24*60*60.
tmax = year
twrite = day
tavestart = day
sig = 1.e-6

def ensemble_generator(initial_PV, n):
    
    # configure model
    m = pyqg.QGModel(tmax=tmax, twrite=twrite, tavestart=tavestart)

    # create an empty array filled with zeros 
    noise = np.zeros_like(ds_initial.q.values)

    # index to the middle of noise and add random perturbation to both levels
    rg = Generator(MT19937(int(n))) 
    noise[:,np.floor(len(ds_initial.x)/2).astype('int'), 
          np.floor(len(ds_initial.y)/2).astype('int')] = sig*rg.random((m.q.shape[0]))

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