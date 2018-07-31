import os,sys,glob
if len(sys.argv) < 8:
    print """The script %s needs following inputs:
\t1. number of frames to be extracted
\t2. tica lagtime
\t3. pdb file
\t4. start trajectory number
\t5. end trajectory number
\t6. path to trajectories
\t7. generic name of the trajectories
"""
    quit()

import mdtraj as md
import numpy as np
import mdtraj.io as io
import matplotlib
matplotlib.use('Agg')
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams['axes.linewidth'] = 2
rcParams.update({'font.size': 16})


def plot_extracted_frames_locations_on_tica(stretch,tica_lag,n_frames):
    ev0 = io.loadh('analysis/tica_projections/ev0.h5')['arr_0']
    ev1 = io.loadh('analysis/tica_projections/ev1.h5')['arr_0']
    center_ev0 = ev0 - np.mean(ev0)
    center_ev1 = ev1 - np.mean(ev1)
    r = (center_ev0 + center_ev1)**2
    ind = np.argsort(r)
    plt.figure(figsize=(12,8))
    plt.hist2d(ev0,ev1,bins=100,norm=LogNorm())
    stretch = stretch
    plt.plot(ev0[ind[-n_frames * stretch::stretch]],ev1[ind[-n_frames * stretch::stretch]],'r*',markersize=18)
    np.savetxt('analysis/ev0_selected.txt', (ev0[ind[-n_frames * stretch::stretch]]))
    np.savetxt('analysis/ev1_selected.txt', (ev1[ind[-n_frames * stretch::stretch]]))
    plt.xlabel('tIC 1')
    plt.ylabel('tIC 2')
    plt.savefig('analysis/location_of_%d_extracted_frames_on_tica_l%d.png' %(n_frames,tica_lag))
    print "\nInfo: saved 'location_of_%d_extracted_frames_on_tica_l%d.png' at folder 'analysis'\n" %(n_frames,tica_lag)
    return ev0[ind[-n_frames * stretch::stretch]] , ev1[ind[-n_frames * stretch::stretch]]

def extract_frames(pdb,start_traj,end_traj,tica_lag,selected_ev0,selected_ev1,traj_path,traj_name):
    if not os.path.exists('selected_frames'): os.system('mkdir selected_frames')
    for i in range(start_traj,end_traj+1):
        xtcs = glob.glob('%s/%d/*xtc' %(traj_path,i))
        phase_ids = np.array([int(ii.split('.xtc')[0].split('_')[-1]) for ii in xtcs])
        sortt = np.sort(phase_ids)
        print "starting phase id: %d, ending phase id: %d" %(sortt[0], sortt[-1])
        
  	proj = io.loadh('analysis/tica_projections/traj%d_on_tica_l%d.h5' %(i,tica_lag))['arr_0']
 	phase_ids = np.loadtxt('analysis/%d/analysis/traj_%d_number_of_phases_frames.txt' %(i,i))							# (n_frames)
#        ind = [ 1 if iii in np.array(selected_ev0) else 0 for iii in proj[:,0]  ]
        ind = []
	for k in proj[:,0]: 
	    if k in selected_ev0: ind.append(True)
	    else: ind.append(False)
        ind = np.array(ind)
        for j in range(len(phase_ids)):
	    if j == 0: start = 0
	    else : start = int(np.sum(phase_ids[0:j]))
 	    end =  int(np.sum(phase_ids[0:j+1]))
	    selected =  np.where(ind[start:end] == True)[0]
	    if len(selected) != 0:
 	        print "selected frames from traj %d and phase %d:" %(i,j)
	        print np.where(ind[start:end] == True)[0]
		traj = md.load('%s/%d/%s_%d.xtc' %(traj_path,i,traj_name,j+sortt[0]),top=ref)
		try : xyz = np.concatenate((xyz,traj.xyz[selected,:,:]))
		except: xyz = traj.xyz[selected,:,:]
    traj.xyz = xyz
    outname = 'selected_frames/%d_selected_frames_from_traj_%d_to_%d.xtc' %(len(ind),start_traj,end_traj)
    traj.save_xtc2(outname)
    print "\nInfo: saved selected frames from trajectory %d at '%s'\n" %(i,outname)

# load input
n_frames = int(sys.argv[1])
tica_lag = int(sys.argv[2])
pdb = sys.argv[3]
start_traj = int(sys.argv[4])
end_traj = int(sys.argv[5])
traj_path = sys.argv[6]
traj_name = sys.argv[7]

ref = md.load(pdb)

selected_ev0, selected_ev1 = plot_extracted_frames_locations_on_tica(3,tica_lag,n_frames)
extract_frames(pdb,start_traj,end_traj,tica_lag,selected_ev0,selected_ev1,traj_path,traj_name)
