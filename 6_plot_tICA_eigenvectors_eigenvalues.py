import os,sys
if len(sys.argv) < 3:
    print """\nThe script %s needs these inputs:
\t1. tICA file (e.g. tICA_l20.h5)
\t2. parameter file (e.g. parameters.txt)
""" %(sys.argv[0])
    sys.exit(True) 

import numpy as np
import mdtraj.io as io
import matplotlib
# comment out the below line if using local computer
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams['axes.linewidth'] = 2
rcParams.update({'font.size': 20})


def plot_evs():
    evs = tica['vecs']
    plt.figure(figsize=(20,7))
    plt.plot(evs[:,0]/float(np.sum(abs(evs[:,0]))),'-ro',linewidth=2)
    plt.plot(evs[:,1]/float(np.sum(abs(evs[:,1]))),'-bo',linewidth=2)
    plt.plot([-0.5,len(parms)],[0,0],'k')
    plt.legend(('tIC 1','tIC 2'),fontsize=20,ncol=3,handletextpad=0.2,shadow=True,fancybox=True,columnspacing=1,labelspacing=0.1,loc='upper center')
    plt.ylabel('Normalized Eigenvector')
    plt.xlabel('tICA Parameters')
    plt.xlim([-0.5,len(parms)+1])
    plt.xticks(range(len(parms)),parms,rotation='vertical',fontsize=20)
    plt.savefig('analysis/tICA_eigenvectors_ev1_ev2.pdf',dpi=100)
    print '\nSaved analysis/tICA_eigenvectors.pdf\n'
    plt.close()

def plot_vals():
    plt.figure(figsize=(10,7))
    plt.plot(tica['vals'],'o-',lw=2)
    plt.ylabel('Eigenvalue values')
    plt.xlabel('Eigenvalue indecies')
    plt.savefig('analysis/tICA_eigenvalues.pdf')
    print '\nSaved analysis/tICA_eigenvalues.pdf\n'
    plt.close()

def plot_contributions():
    vecs = tica['components']
    cov = tica['covariance']
    dott = np.dot(cov,vecs.T)
    trr = 0
    for i in range(dott.shape[0]):
        s = np.linalg.norm(dott[:,i])**2
        trr += s
    trr = float(trr)
    c3 = 0
    cont = []
    for i in range(dott.shape[0]):
        s = np.linalg.norm(dott[:,i])**2
        c3 += s / trr
        cont.append(c3)
    plt.plot(cont,'o-',lw=2)
    plt.xlim([-1,vecs.shape[0]+1])
    plt.ylim([0,1])
    plt.grid(True,lw=1)
    plt.xlabel('tICA eigenvector')
    plt.ylabel('Contribution to total fluctuation')
    plt.savefig('analysis/tICA_contributions.pdf',dpi=100)
    print "\nSaved analysis/tICA_contributions.pdf\n"


# load inputs
tica = io.loadh(sys.argv[1])
parms = np.loadtxt(sys.argv[2],dtype=str)

# plot tICA eigenvalues
plot_evs()

# plot tICA eigenvectors
plot_vals()

# plot contribution of each tICA eigenvector to total dynamics
plot_contributions()
