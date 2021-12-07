# Spin up PYQG model using the config from Zhang et al. 2020(https://www.mdpi.com/2311-5521/5/1/2); a two-layer QG model to mimic Southern Ocean dynamics.

import os, pyqg, yaml
from numpy.random import Generator, MT19937

# model configuration
config_file = os.environ['CONFIG_FILE'] 
with open(config_file) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    
# Initialize QG Model
m = pyqg.QGModel(nx=config['nx'], L=config['L'], dt=config['dt'], tmax=config['tmax'], twrite=config['twrite'],
                 tavestart=config['tavestart'], taveint=config['taveint'], ntd=config['ntd'], beta=config['beta'],
                 rd=config['Ld'], delta=config['delta'], H1=config['H1'], U1=config['U1'], U2=config['U2'], rek=config['rek']) 

# Set upper and lower layer PV anomalies (in spatial coordinates)
rg = Generator(MT19937(int(1)))
qi = config['sig']*rg.random((m.q.shape))
m.set_q(qi) 

Tsave = config['day']*30

# Run with snapshots and save model every 30 days, loop breaks at tmax.
for snapshot in m.run_with_snapshots(tsnapstart=m.t, tsnapint=m.dt):
    
    if (m.t % Tsave)==0:
        model = m.to_dataset()
        model = model.chunk() #this uses a global chunk

        if m.t == Tsave:
            model.to_zarr(os.environ['OUT_FILE'], mode='w-', consolidated=True)
        else:
            model.to_zarr(os.environ['OUT_FILE'], mode='a', append_dim='time', consolidated=True)