import os,sys,glob
if len(sys.argv) < 5:
    print """\nThe %s script needs following inputs:
1. Id of the microstate to extract frames from (zero based)
2. generic name of the mapping file (Ex. 'number_of_phases_frames' in traj_40_number_of_phases_frames.txt)
3. start trajectory number
4. end trajectory number
5. path to assignment files
6. path to save the results        
7. reference pdb file
8. path to trajectories
9. generic name of trajectories  (Ex. leuT_phase4)
""" %(sys.argv[0])
    sys.exit(True)
import numpy as np
import mdtraj.io as io
import mdtraj as md
from tqdm import tqdm

# load inputs
micro_id = int(sys.argv[1])
name = sys.argv[2]
start_traj = int(sys.argv[3])
end_traj = int(sys.argv[4])
assign_path = sys.argv[5]
out_path = sys.argv[6]
ref_path = sys.argv[7]
traj_path = sys.argv[8]
traj_name = sys.argv[9]
if not os.path.exists(out_path): os.system('mkdir %s' %out_path)

ref = md.load(ref_path)

def get_phases(idd):
    xtcs = glob.glob('%s/%d/%s_*.xtc' %(traj_path,idd,traj_name))
    nn = np.array([int(xtc.split('.xtc')[0].split('_')[-1]) for xtc in xtcs])
    n_phases = len(nn)
    start_phase = np.min(nn)
    print "\nTrajectory %d has %d phases and starting phase is %d" %(idd,n_phases,start_phase)
    return n_phases, start_phase


def extract(micro_id,start_traj,end_traj):
    n_phases, start_phase = get_phases(start_traj)
#    traj = md.load('%s/%d/%s_%d.xtc' %(traj_path,start_traj,traj_name,start_phase),top=ref)
#    xyz = traj.xyz[0:2,:,:]
    for i in range(start_traj,end_traj+1):
        n_phases, start_phase = get_phases(i)
 	assign = np.loadtxt('%s/assigns_%d.txt' %(assign_path,i),dtype=int)
  	map = np.loadtxt('%s/analysis_tica/analysis/%d/analysis/traj_%d_%s.txt' %(traj_path,i,i,name))
        if micro_id not in assign: continue
	ind = np.where(assign == micro_id)[0]
	if len(ind) > 1000: ind2 = np.random.choice(ind,20) 
	elif len(ind) > 100 and len(ind) < 1000: ind2 = np.random.choice(ind,10) 
	elif len(ind) > 10 and len(ind) < 100: ind2 = np.random.choice(ind,5) 
	elif len(ind) < 10: ind2 = np.random.choice(ind,5) 
        print "\n%d frames are selected from traj %d" %(len(ind2),i)
	phase_frame = []
        map2 = []
  	ii = 0
        try: n_ppp = len(map) 
        except: map = [map]
        for j in range(len(map)):
#        for j in range(len(map)):
	    for k in range(int(map[j])):
	 	map2.append([j,k]) 
        map2 = np.array(map2)
        selected_phases = map2[:,0][ind2] + start_phase
        selected_frames = map2[:,1][ind2]
        for ii in range(len(selected_phases)): print "\tselected frames for phase: %d --> " %selected_phases[ii], selected_frames[ii]

 	for ii in range(len(selected_phases)):
	    traj = md.load('%s/%d/%s_%d.xtc' %(traj_path,i,traj_name,selected_phases[ii]),top=ref)
	    xyz2 = np.zeros((1,traj.xyz.shape[1],3))
 	    try : xyz2[0] = traj.xyz[selected_frames[ii],:,:]
 	    except : xyz2 = traj.xyz[selected_frames[ii],:,:]
	    try: xyz = np.concatenate((xyz,xyz2),axis=0)
	    except: xyz = xyz2
    print "\nTotal number of snapshots saved for microstate %d is: %d" %(micro_id,xyz.shape[0])
    traj.xyz = xyz[1:,:,:]
    traj.save_xtc2('%s/selected_snapshots_for_microstate_%d.xtc' %(out_path,micro_id))
	

        

extract(micro_id,start_traj,end_traj)
