import matplotlib.pyplot as plt
import numpy             as np
import h5py
import math
from astropy.cosmology import Planck18 as cosmo
import os

plt.rcParams.update({'font.size': 18})
plt.rc('legend',fontsize=14)

mp = 1.67e-24
Mpc = 3.0856e24
kpc = Mpc/1000.0
erg_to_keV = 6.242e+8
Zsun = 0.0127
Msun = 1.989e33 #g cm^-3
kb = 1.38e-16 # erg/K
erg_to_keV = 6.242e+8
K_to_keV = kb * erg_to_keV
XH = 0.76 #primordial hydrogen fraction
mu = 0.58824; # X=0.76 assumed 
mu_e = mue = 2.0/(1.0+XH); # X=0.76 assumed

def return_xsb_emulator (profile_type='xsb_median', home='./X_emulator_profiles/', suite='SIMBA', interpolation_type='linear'):
    '''
    Inputs:
        A: feedback strength (float)
        z: redshift (float)
        logM: halo mass in log10 Msun
    Return:
        r: radial bins in Mpc (numpy array)
        profile: emulator profile values in log10 cgs units (numpy array)
    '''
    import x_helper_functions_LH as fs
    #mass=fs.mass
    #mass_str=fs.mass_str
    #snap=fs.snap
    #redshifts=fs.choose_redshift(suite)
    #vary,sims=fs.choose_vary(feedback_type)
    #samples=fs.cartesian_prod(vary,redshifts,mass)
    #params = np.vstack([OmegaM,sigma8,ASN1,ASN2,AAGN1,AAGN2]).T
    #samples = fs.LH_cartesian_prod(params, redshifts, mass)
    #nsamp=samples.shape[0]

    samples,radius,y,emulator=fs.build_xsb_emulator(home,suite,profile_type,interpolation_type)
    return radius, emulator

def save_emulator(filename, radius, emulator):

    import pickle

    with open(filename, 'wb') as f:
        pickle.dump((radius, emulator), f) 
    
def load_emulator(filename) :

    import pickle
    with open(filename, 'rb') as f:
        radius, emulator = pickle.load(f) 

    return radius, emulator

def emulated_xsb_profile(emulator, A, z, logM):
    params=[[A, z, logM]] #the order here is important- A, then z, then logM
    profile = emulator(params).ravel()
    return profile


home='./X_emulator_profiles/' #point to your profiles
#suite_list = ['IllustrisTNG','SIMBA'] #SIMBA or IllustrisTNG
suite_list = ['SIMBA'] #SIMBA or IllustrisTNG
interpolation_type='linear' #this is the Rbf interpolation function

feedback_type_list = ['ASN1', 'ASN2', 'AAGN1', 'AAGN2']
rerun_building_emulator = True

for suite in suite_list :
    for feedback_type in feedback_type_list :

        emulator_file =suite+'_LH_xsb_emulator_'+feedback_type+'.pkl' 
        if (not os.path.exists(emulator_file)) or rerun_building_emulator :

            radius_Mpc, x_emulator = return_xsb_emulator(profile_type='xsb_median', home=home, suite=suite)
            save_emulator(emulator_file , radius_Mpc, x_emulator)

