# Spin up PYQG model using the config from Zhang et al. 2020(https://www.mdpi.com/2311-5521/5/1/2) using a two-layer QG model to mimic Southern Ocean dynamics.

import os
import numpy as np
import xarray as xr
import pyqg
from numpy.random import Generator, MT19937
import yaml


# model configuration
config_file = os.environ['CONFIG_FILE'] 
with open(config_file) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    
# Initialize QG Model
m = pyqg.QGModel(nx=config['nx'], L=config['L'], dt=config['dt'], tmax=config['tmax'], twrite=config['twrite'],
                 tavestart=config['tavestart'], taveint=config['taveint'], ntd=config['ntd'], beta=config['beta'],
                 rd=config['Ld'], delta=config['delta'], H1=config['H1'], U1=config['U1'], U2=config['U2'], rek=config['rek']) 

# taveint: Time interval for accumulation of diagnostic averages. (units: model time)
# tsnapint: Time interval for snapshots (units: model time)
# tsnapstart: Start time for snapshot writeout (units: model time)

# Set upper and lower layer PV anomalies (in spatial coordinates)
rg = Generator(MT19937(int(1)))
qi = config['sig']*rg.random((m.q.shape))
m.set_q(qi) 

Tsave = config['day']*5
fn = '/burg/abernathey/users/hillary/lcs/spin_up/spin_up.zarr' 

# Run with snapshots and save model at pentad model time increments
for snapshot in m.run_with_snapshots(tsnapstart=m.t, tsnapint=m.dt):
    
    # Only save daily snapshots
        if (m.t % Tsave)==0:
            model = m.to_dataset()
            model = model.chunk() #this uses a global chunk
            
            if m.t == Tsave:
                model.to_zarr(fn, mode='w-', consolidated=True)
            else:
                model.to_zarr(fn, mode='a', append_dim='time', consolidated=True)