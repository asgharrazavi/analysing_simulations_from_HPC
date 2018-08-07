import os,sys
if len(sys.argv) < 5:
    print """\nThe %s script needs following inputs:
1. path to projections on tica
2. number of microstates
3. generic name of tica projection files (e.g. 'on_tica_l20' in traj56_on_tica_l20.h5)
4. start trajectory number
5. end trajectory number
6. path to save the results        
""" %(sys.argv[0])
    sys.exit(True)

import numpy as np
from msmbuilder.cluster import KMeans, KCenters
import mdtraj.io as io
import matplotlib
# to be able to plot figures on HPC
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams['axes.linewidth'] = 2
rcParams.update({'font.size': 16})
from tqdm import tqdm


def cluster():
    '''
    This function perfomes K-means clustering on the tICA space and saves assignsment files for each trajectory.
    Cluster centers are also saved at `microstate_centers.txt` file.
    '''
    cluster = KMeans(n_clusters=n_states,n_jobs=-1,verbose=0, max_iter=100, tol=0.0001,)
    dataset, ev0, ev1 = [], [], []
    print "Loading projected data..."
    for i in tqdm(range(start_traj, end_traj+1)):
        a = io.loadh('%s/traj%d_%s.h5' %(proj_path,i,traj_name))['arr_0']
        a = a[:,0:2]
        dataset.append(a)
	ev0.extend(a[:,0])
	ev1.extend(a[:,1])
    print "Clustering %d datapoints..." %len(ev0)
    cluster.fit(dataset)
    for i in range(start_traj,end_traj+1):
        np.savetxt('%s/assigns_%d.txt' %(out_path,i),np.array(cluster.labels_[i-start_traj]),fmt='%d')
    np.savetxt('%s/microstate_centers.txt' %out_path,np.array(cluster.cluster_centers_))
    print "Saved microstate assignments and microstate centers at %s" %out_path
    return cluster.cluster_centers_, np.array(ev0), np.array(ev1)

def plot_gens_on_tICA(ev0, ev1, cluster_centers):
    plt.figure(figsize=(20,15))
    plt.hist2d(ev0,ev1,bins=200,norm=LogNorm())
    plt.plot(cluster_centers[:,0],cluster_centers[:,1],'ro',markersize=12)
    for i in range(len(cluster_centers)):
        plt.text(cluster_centers[:,0][i],cluster_centers[:,1][i],i,fontsize=18)
    plt.xlabel('tIC 1')
    plt.ylabel('tIC 2')
    plt.title('Microstate centers on tICA')
    plt.savefig('%s/microstates_on_tICA.pdf' %(out_path))
    print "Plotted microstate centers on tICA space at %s" %out_path

# load inputs
proj_path = sys.argv[1]
n_states = int(sys.argv[2])
traj_name = sys.argv[3]
start_traj = int(sys.argv[4])
end_traj = int(sys.argv[5])
out_path = sys.argv[6]

if not os.path.exists(out_path): os.system('mkdir %s' %out_path)

# cluster data
cluster_centers, ev0, ev1 = cluster()

# project and plot data and cluster centers on tICA landscape
plot_gens_on_tICA(ev0, ev1, cluster_centers)


