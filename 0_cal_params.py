import os,sys,glob
if len(sys.argv) < 6:
    print """The script: %s needs following inputs:
\t1. pdb file
\t2. psf file
\t3. generic name of the trajectory files
\t4. path to vmd
\t5. path to trajectories
""" %sys.argv[0]
    quit()

import numpy as np
import mdtraj as md
import multiprocessing

def vmd_cal_parms(vmd_path,psf,traj,phase_idd):
    text = """%s -dispdev none %s %s <<EOF
#animate delete  beg 0 end 0 skip 0 0
#play /pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/analysis_tica/tcls/tk_TM3_TM4_EC.tcl
#play /pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/analysis_tica/tcls/tk_TM3_TM6_EC.tcl
#play /pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/analysis_tica/tcls/tk_TM4_TM6_EC.tcl
#play /pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/analysis_tica/tcls/tk_TM4_TM6_MID.tcl
#play /pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/analysis_tica/tcls/tk_TM4_TM6_MIN.tcl
#play /pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/analysis_tica/tcls/tk_t333_y439.tcl
#play /pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/analysis_tica/tcls/tk_e313_r432.tcl
#play /pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/analysis_tica/tcls/tk_e318_r432.tcl
#play /pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/analysis_tica/tcls/tk_y439_r432.tcl
play /pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/analysis_tica/tcls/tk_TM3_kink.tcl
play /pbtech_mounts/hwlab_store_athena/khelgeo/tmem/md_simulations/tica_analysis/WT/analysis_tica/tcls/tk_TM4_kink.tcl
quit
EOF
""" %(vmd_path,psf,traj)
    f = open('vmd_temp.sh','w')
    f.writelines(text)
    f.close()
    os.system('chmod +x vmd_temp.sh')
    os.system('./vmd_temp.sh')
    if not os.path.exists('analysis'): os.system('mkdir analysis')
    if not os.path.exists('analysis/parameters'): os.system('mkdir analysis/parameters')
 #   os.system(' mv   TM3_TM4_EC.txt        	analysis/parameters/TM3_TM4_EC_%d.txt' %phase_idd)     
 #   os.system(' mv   TM3_TM6_EC.txt        	analysis/parameters/TM3_TM6_EC_%d.txt' %phase_idd)     
 #   os.system(' mv   TM4_TM6_EC.txt        	analysis/parameters/TM4_TM6_EC_%d.txt' %phase_idd)     
 #   os.system(' mv   TM4_TM6_MID.txt        	analysis/parameters/TM4_TM6_MID_%d.txt' %phase_idd)     
#    os.system(' mv   TM4_TM6_MIN.txt        	analysis/parameters/TM4_TM6_MIN_%d.txt' %phase_idd)     
 #   os.system(' mv   t333_y439.txt              analysis/parameters/t333_y439_%d.txt' %phase_idd)
 #   os.system(' mv   e313_r432.txt              analysis/parameters/e313_r432_%d.txt' %phase_idd)
 #   os.system(' mv   e318_r432.txt              analysis/parameters/e318_r432_%d.txt' %phase_idd)
 #   os.system(' mv   y439_r432.txt              analysis/parameters/y439_r432_%d.txt' %phase_idd)
#    os.system(' mv   lip_126_Z.txt        	        analysis/parameters/lip_126_Z_%d.txt' %phase_idd)     
#    os.system(' mv   lipid_EC.txt        	        analysis/parameters/lipid_EC_%d.txt' %phase_idd)     
#    os.system(' mv   lipid_MID.txt       	        analysis/parameters/lipid_MID_%d.txt' %phase_idd)     
#    os.system(' mv   lipid_contacting_313_432.txt      	        analysis/parameters/lipid_contacting_313_432_%d.txt' %phase_idd)     
 #   os.system(' mv   water_EC.txt        	        analysis/parameters/water_EC_%d.txt' %phase_idd)     
 #   os.system(' mv   water_MID.txt        	        analysis/parameters/water_MID_%d.txt' %phase_idd)     
    os.system(' mv   TM3_kink.txt        	        analysis/parameters/TM3_kink_%d.txt' %phase_idd)     
    os.system(' mv   TM4_kink.txt        	        analysis/parameters/TM4_kink_%d.txt' %phase_idd)     
    return len(np.loadtxt('analysis/parameters/TM3_TM4_EC_%d.txt' %phase_idd))

def concat():
 #    os.system('cat analysis/parameters/TM3_TM4_EC_?.txt analysis/parameters/TM3_TM4_EC_??.txt analysis/parameters/TM3_TM4_EC_???.txt  > analysis/parameters/TM3_TM4_EC.txt')
 #    os.system('cat analysis/parameters/TM3_TM6_EC_?.txt analysis/parameters/TM3_TM6_EC_??.txt analysis/parameters/TM3_TM6_EC_???.txt  > analysis/parameters/TM3_TM6_EC.txt')
 #    os.system('cat analysis/parameters/TM4_TM6_EC_?.txt analysis/parameters/TM4_TM6_EC_??.txt analysis/parameters/TM4_TM6_EC_???.txt  > analysis/parameters/TM4_TM6_EC.txt')
 #    os.system('cat analysis/parameters/TM4_TM6_MID_?.txt analysis/parameters/TM4_TM6_MID_??.txt analysis/parameters/TM4_TM6_MID_???.txt  > analysis/parameters/TM4_TM6_MID.txt')
 #    os.system('cat analysis/parameters/TM4_TM6_MIN_?.txt analysis/parameters/TM4_TM6_MIN_??.txt analysis/parameters/TM4_TM6_MIN_???.txt  > analysis/parameters/TM4_TM6_MIN.txt')
     os.system('cat analysis/parameters/TM3_kink_?.txt analysis/parameters/TM3_kink_??.txt analysis/parameters/TM3_kink_???.txt  > analysis/parameters/TM3_kink.txt')
     os.system('cat analysis/parameters/TM4_kink_?.txt analysis/parameters/TM4_kink_??.txt analysis/parameters/TM4_kink_???.txt  > analysis/parameters/TM4_kink.txt')
 #    os.system('cat analysis/parameters/t333_y439_?.txt analysis/parameters/t333_y439_??.txt analysis/parameters/t333_y439_???.txt  > analysis/parameters/t333_y439.txt')
 #    os.system('cat analysis/parameters/e313_r432_?.txt analysis/parameters/e313_r432_??.txt analysis/parameters/e313_r432_???.txt  > analysis/parameters/e313_r432.txt')
 #    os.system('cat analysis/parameters/e318_r432_?.txt analysis/parameters/e318_r432_??.txt analysis/parameters/e318_r432_???.txt  > analysis/parameters/e318_r432.txt')
 #    os.system('cat analysis/parameters/y439_r432_?.txt analysis/parameters/y439_r432_??.txt analysis/parameters/y439_r432_???.txt  > analysis/parameters/y439_r432.txt')
#    os.system('cat analysis/parameters/lip_126_Z_?.txt analysis/parameters/lip_126_Z_??.txt analysis/parameters/lip_126_Z_???.txt  > analysis/parameters/lip_126_Z.txt')
#    os.system('cat analysis/parameters/lipid_EC_?.txt analysis/parameters/lipid_EC_??.txt analysis/parameters/lipid_EC_???.txt  > analysis/parameters/lipid_EC.txt')
#    os.system('cat analysis/parameters/lipid_MID_?.txt analysis/parameters/lipid_MID_??.txt analysis/parameters/lipid_MID_???.txt  > analysis/parameters/lipid_MID.txt')
#    os.system('cat analysis/parameters/lipid_contacting_313_432_?.txt analysis/parameters/lipid_contacting_313_432_??.txt analysis/parameters/lipid_contacting_313_432_???.txt  > analysis/parameters/lipid_contacting_313_432.txt')
 #   os.system('cat analysis/parameters/water_EC_?.txt analysis/parameters/water_EC_??.txt analysis/parameters/water_EC_???.txt  > analysis/parameters/water_EC.txt')
 #   os.system('cat analysis/parameters/water_MID_?.txt analysis/parameters/water_MID_??.txt analysis/parameters/water_MID_???.txt  > analysis/parameters/water_MID.txt')
     os.system('rm *txt')


def run_one(traj_idd,dummy):
# 	os.system('mkdir analysis')
# 	os.system('mkdir analysis/%d' %traj_idd)
	os.chdir('analysis/%d' %traj_idd)
        xtcs = glob.glob('%s/%d/*xtc' %(traj_path,traj_idd))
        print "number of phases in trajectory %d: %d" %(traj_idd,len(xtcs))
        phase_ids = np.array([int(ii.split('.xtc')[0].split('_')[-1]) for ii in xtcs])
	sortt = np.sort(phase_ids)
  	print "starting phase id: %d, ending phase id: %d" %(sortt[0], sortt[-1])
        n_phases = len(xtcs)
#        n_frames_in_each_phase = 25				#this needs to be adjusted
        phases_frames = np.ones(n_phases) 
	for phase in range(sortt[0],sortt[-1]+1):
            n_frames = vmd_cal_parms(vmd_path,psf,'%s/%d/%s_%d.xtc' %(traj_path,traj_idd,traj_name,phase),phase)
 	    phases_frames[phase-sortt[0]] = n_frames
	concat()
        np.savetxt('analysis/traj_%d_number_of_phases_frames.txt' %(traj_idd), phases_frames)
 	os.chdir('../../')

if 1:
 def main2():
    global pdb, psf, traj_name, vmd_path, traj_path
    pdb = sys.argv[1]
    psf = sys.argv[2]
    traj_name = sys.argv[3]
    vmd_path = sys.argv[4]
    traj_path = sys.argv[5]
    for i in range(9):
	run_one(i,'dummy')
#    for i in range(8,9):
#	run_one(i,'dummy')
#    for i in range(60,110):
#	run_one(i,'dummy')

def main():
    global pdb, psf, traj_name, vmd_path, traj_path
    pdb = sys.argv[1]
    psf = sys.argv[2]
    traj_name = sys.argv[3]
    vmd_path = sys.argv[4]
    traj_path = sys.argv[5]
    for i in range(20,30):
        p = multiprocessing.Process(target=run_one,args=(i,'dummy'))
        p.start()


if __name__ == "__main__":
   main2()

    
