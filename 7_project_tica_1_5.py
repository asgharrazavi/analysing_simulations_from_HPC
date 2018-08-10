import os,sys,glob
if len(sys.argv) < 5:
    print """The script %s needs following inputs:
\t1. tICA lagtime (in terms of number of steps)
\t2. parameters.txt that contains name of parameters (e.g. na2_na1, r5_y268)
\t3. start trajectory number
\t4. end trajectory number
"""%(sys.argv[0])
   sys.exit(True)    

import h5py
import mdtraj.io as io
import matplotlib
# disable this if using local computer
matplotlib.use('Agg')
import msmbuilder.decomposition.tica as ti
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams['axes.linewidth'] = 2
rcParams.update({'font.size': 16})


def train(start_traj,end_traj,n_parms):
    dataset = []
    for i in range(start_traj,end_traj+1):
	ref1 = np.loadtxt('analysis/%d/analysis/parameters/%s.txt' %(i,parms[0]))
    	d = np.zeros((len(ref1),n_parms))
    	print "\tworking on trajectory:", i
    	for p in range(n_parms):
	    data = np.loadtxt('analysis/%d/analysis/parameters/%s.txt' %(i,parms[p]))
	    d[:,p] = data
    	dataset.append(d)
    return dataset

def project(start_traj,end_traj,n_parms,tica,tica_lag):
    dataset = []
    if not os.path.exists('analysis/tica_projections') : 
        os.system('mkdir analysis/tica_projections')
    for i in range(start_traj,end_traj+1):
	ref1 = np.loadtxt('analysis/%d/analysis/parameters/%s.txt' %(i,parms[0]))
    	d = np.zeros((len(ref1),n_parms))
    	for p in range(n_parms):
	    data = np.loadtxt('analysis/%d/analysis/parameters/%s.txt' %(i,parms[p]))
	    d[:,p] = data
        proj = np.dot(d,tica['components'].T)
        io.saveh('analysis/tica_projections/traj%d_on_tica_l%d.h5' %(i,tica_lag), proj)
    	print "\tsaved projected trajectory %d at folder 'analysis/tica_projections' " %i
        dataset.append(proj)
    return dataset

# load inputs
tica_lag = int(sys.argv[1])
parms = np.loadtxt(sys.argv[2],dtype=str)
start_traj = int(sys.argv[3])
end_traj = int(sys.argv[4])

# information about tICA parameters and simulation trajectories
n_parms = len(parms)
n_trajs = end_traj - start_traj + 1
print "there are %d parameters" %n_parms
print "there are %d trajectories in the 'analysis/parameters' folder" %n_trajs

# load tICA parameters and build tICA object
tica = ti.tICA(n_components=None, lag_time=tica_lag)
print "Obtaining tICA object..."
dataset1 = train(start_traj,end_traj,n_parms)
tica.fit(dataset1)
print "first 5 tICA eigenvalues:", tica.eigenvalues_[0:5]
tica.save('analysis/tica_l%d.h5' %tica_lag)
print "saved tICA object: 'tica_l%d.h5'  in folder 'analysis' "  %tica_lag

# project simulations on tICA eigenvectors to obtain tICA landscape
tica = io.loadh('analysis/tica_l%d.h5' %tica_lag)
dataset = project(start_traj,end_traj,n_parms,tica,tica_lag)
ev0, ev1 = [], []
for i in range(n_trajs):
    ev0.extend(dataset[i][:,0]); ev1.extend(dataset[i][:,4])
ev0, ev1 = np.array(ev0), np.array(ev1)

# save projected data 
io.saveh('analysis/tica_projections/ev0.h5',ev0)
io.saveh('analysis/tica_projections/ev4.h5',ev1)
print "saved all projected frames: 'ev0.h5 & ev4.h5' at 'analysis/tica_projections' "

# plot and save tICA landscape
plt.figure(figsize=(12,8))
plt.hist2d(ev0,ev1,bins=200,norm=LogNorm())
plt.savefig('analysis/tica_l%d_1_5.png' %tica_lag)
print "saved tica landscape for lag time %d at 'analysis/tica_l%d_1_5.png' " %(tica_lag,tica_lag)

