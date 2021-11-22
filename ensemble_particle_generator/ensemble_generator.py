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
    
    # configure model
    m = pyqg.QGModel(nx=config['nx'], L=config['L'], dt=config['dt'], tmax=config['tmax'], twrite=config['twrite'], tavestart=config['tavestart'], ntd=config['ntd'], beta=config['beta'], rd=config['Ld'], delta=config['delta'], H1=config['H1'], U1=config['U1'], U2=config['U2'], rek=config['rek']) 
    
    # create an empty array filled with zeros 
    noise = np.zeros_like(ds_initial.q.values)

    # index to the middle of noise and add random perturbation to both levels
    rg = Generator(MT19937(int(n))) 
    noise[:,np.floor(len(ds_initial.x)/2).astype('int'), 
          np.floor(len(ds_initial.y)/2).astype('int')] = config['sig']*rg.random((m.q.shape[0]))

    # set PV anomaly with randomness
    m.set_q(ds_initial.q.values + noise)
    
    # Set up Lagrangian particles and advect using gridded u and v
    dx = m.dx/2   # or 4
    dy = m.dy/2

    x0,y0 = np.meshgrid(np.arange(0,m.L,dx)+dx/2,
                        np.arange(0,m.W,dy)+dy/2)

    x0 = x0.ravel()
    y0 = y0.ravel()
    
    itr = -1

    lpa = particles.GriddedLagrangianParticleArray2D(x0, y0, m.nx, m.ny,
            periodic_in_x=True, periodic_in_y=True,
            xmin=0, xmax=m.L, ymin=0, ymax=m.W)

    uprev = m.ufull[0].copy()   
    vprev = m.vfull[0].copy()

    Tsave = config['day'] # daily snapshots will be saved
    
    # run with snapshots, save model increments as xarray DataSet
    for snapshot in m.run_with_snapshots(tsnapstart=m.t, tsnapint=m.dt):
        
        # set up velocities for Lagrangian advection
        u = m.ufull[0]
        v = m.vfull[0]

        # Advance particles using a gridded velocity field.
        lpa.step_forward_with_gridded_uv(uprev, vprev, u, v, m.dt)

        uprev = u.copy()
        vprev = v.copy()

        if itr==-1:
            qi = m.q[0].copy()
            ui = u.copy()
            vi = v.copy()

            itr+=1

        # Only save daily snapshots
        if (m.t % Tsave)==0:
            print(m.t)
            
            # Vorticity 
            relative_vorticity = m.ifft(-(m.k**2 + m.l**2)*m.ph)[0]
            particle_vorticity = lpa.interpolate_gridded_scalar(lpa.x, lpa.y, relative_vorticity)

            # Strain 
            strain_normal = m.ifft(2 * m.k * m.l * m.ph)
            strain_shear = m.ifft((-m.k**2 + m.l**2)*m.ph)
            strain_magnitude = np.sqrt(strain_normal**2 + strain_shear**2)[0]
            particle_strain = lpa.interpolate_gridded_scalar(lpa.x, lpa.y, strain_magnitude)

            itr+=1

            shape = (1, np.int64(m.L/dx), np.int64(m.W/dx))
            ds_particles = xr.Dataset({
                'x': (('time', 'y0', 'x0'), np.reshape(lpa.x.copy(), shape),{'long_name': 'particle position in the x direction', 'units': 'grid point'}),
                'y': (('time', 'y0', 'x0'), np.reshape(lpa.y.copy(), shape),{'long_name': 'particle position in the y direction', 'units': 'grid point'}),
                'vort': (('time', 'y0', 'x0'), np.reshape(particle_vorticity, shape),{'long_name': 'particle relative vorticity', 'units': 'second -1'}),
                'strain': (('time', 'y0', 'x0'), np.reshape(particle_strain, shape),{'long_name': 'particle strain magnitude', 'units': 'unitless'}),
            },
                coords = {
                    'x0': (('x0'), np.reshape(x0, shape[1:])[0,:],{'long_name': 'real space grid points in the x direction', 'units': 'grid point'}),
                    'y0': (('y0'), np.reshape(y0, shape[1:])[:,0],{'long_name': 'real space grid points in the y direction', 'units': 'grid point'}),
                    'time': (('time'), np.array([m.t]),{'long_name': 'model time', 'units': 'seconds',})
                },
                attrs = ds_initial.attrs,
            )
            
            ds_particles = ds_particles.expand_dims(dim='n') # ensemble member
            ds_particles['n'] = [int(n)]
            ds_particles['n'].attrs = {'long_name': 'ensemble member', 'units': 'none',}
    
            
            # Save as Zarr
            fn = '/burg/abernathey/users/hillary/lcs/pyqg_ensemble/'+'%03d'%int(n)+'.zarr' 
            ds_particles = ds_particles.chunk() #this uses a global chunk
            if m.t == Tsave:
                ds_particles.to_zarr(fn, mode='a', consolidated=True)
            else:
                ds_particles.to_zarr(fn, mode='a', append_dim='time', consolidated=True)
        if m.t==Tsave*90:
                break
                

# generate ensemble
ensemble_generator(ds_initial, n)
