import os,sys,glob
if len(sys.argv) < 10:
    print """The script: %s needs following inputs:
\t1. psf file
\t2. selected frames xtc file
\t3. path to vmd
\t4. parameter files
\t5. tica lag time
\t6. tica file
\t7. ev0.h5
\t8. ev1.h5
\t9. output (Ex. output.png)
""" %sys.argv[0]
    quit()

import numpy as np
import mdtraj as md
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import mdtraj.io as io
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams['axes.linewidth'] = 2
rcParams.update({'font.size': 16})


def vmd_cal_parms(vmd_path,psf,traj):
    text = """%s -dispdev none %s %s <<EOF
#animate delete  beg 0 end 0 skip 0 0
play tk_TM3_TM4_EC.tcl
play tk_TM3_TM6_EC.tcl
play tk_TM4_TM6_EC.tcl
play tk_TM4_TM6_MID.tcl
play tk_t333_y439.tcl
play tk_e313_r432.tcl
play tk_e318_r432.tcl
play tk_y439_r432.tcl
quit
EOF
""" %(vmd_path,psf,traj)
    f = open('vmd_temp.sh','w')
    f.writelines(text)
    f.close()
    os.system('chmod +x vmd_temp.sh')
    os.system('./vmd_temp.sh')
    os.system(' mv   TM3_TM4_EC.txt                selected_frames/')
    os.system(' mv   TM3_TM6_EC.txt                selected_frames/')
    os.system(' mv   TM4_TM6_EC.txt                selected_frames/')
    os.system(' mv   TM4_TM6_MID.txt                selected_frames/')
    os.system(' mv   t333_y439.txt                selected_frames/')
    os.system(' mv   e313_r432.txt                selected_frames/')
    os.system(' mv   e318_r432.txt                selected_frames/')
    os.system(' mv   y439_r432.txt                selected_frames/')

def project(n_parms,tica_evs,tica_lag):
    ref1 = np.loadtxt('selected_frames/TM3_TM4_EC.txt')
    d = np.zeros((len(ref1),n_parms))
    for p in range(n_parms):
        data = np.loadtxt('selected_frames/%s.txt' %(parms[p]))
        d[:,p] = data
    proj = np.dot(d,tica_evs.T)
    io.saveh('selected_frames/selected_frames_on_tica_l%d.h5' %(tica_lag), proj)
    return proj

# load inputs
psf = sys.argv[1]
traj = sys.argv[2]
vmd_path = sys.argv[3]
parms = np.loadtxt(sys.argv[4],dtype=str)
n_parms = len(parms)
tica_lag = int(sys.argv[5])
tica_evs = io.loadh(sys.argv[6])['components']
ev0 = io.loadh(sys.argv[7])['arr_0']
ev1 = io.loadh(sys.argv[8])['arr_0']
output = sys.argv[9]

vmd_cal_parms(vmd_path,psf,traj)
data = project(n_parms,tica_evs,tica_lag)
 
plt.figure(figsize=(20,15))
plt.hist2d(ev0,ev1,bins=200,norm=LogNorm())
plt.plot(data[:,0],data[:,1],'ro',markersize=12)
plt.xlabel('tIC 1')
plt.ylabel('tIC 2')
plt.savefig('/pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/%s' %output)
print "Saved %s" %('/pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/%s' %output)

