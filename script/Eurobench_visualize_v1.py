# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:06:00 2021

@author: rschulte
"""

import yaml
import numpy as np
import os
import pandas as pd
import scipy.signal as ss
import matplotlib.pyplot as plt

def emg_envelope(emg,fs=1000,high=20,low=6,order=2):
    bh,ah = ss.butter(order,high/(fs/2),'highpass')
    bl,al = ss.butter(order,low/(fs/2))
    emg_hp = ss.filtfilt(bh,ah,emg,axis=0)
    return ss.filtfilt(bl,al,abs(emg_hp),axis=0)
     

def visualize_joint_run(joint_data,gait_events,resample_len=1000):
    """
    Parameters
    ----------
    joint_data : dict
        Dictonary containing joint data in degrees and a key 'time' in seconds.
    gait_events : dict
        Dictonary containing the gait events for left and right leg, in seconds.
    resample_len : int
        Length for resampling data for visualization. Lower = lower resolution

    Returns
    -------
    None

    """
    sides = ['l','r'] # More dynamic: np.unique([key.rsplit('_')[0] for key in joint_data if not 'time' in key])
    joints = [str(val) for val in np.unique([key.rsplit('_')[1] for key in joint_data if not 'time' in key])]
    joints_order = ['hip','knee','ankle']
    time = np.array(joint_data['time'])
    t_axis = np.linspace(0,100,resample_len)
    fig,ax = plt.subplots(nrows=len(joints),ncols=len(sides),gridspec_kw={'hspace':0.5})
    for i_side,side in enumerate(sides):
        # Convert gait events from seconds to indices corresponding to time
        hc = np.array([np.argmin(abs(ge-time)) for ge in gait_events[side+'_heel_strike']])
        for i in range(len(hc)-1):
            r = range(hc[i],hc[i+1])
            for i_joint,joint in enumerate(joints_order):
                if joint not in joints:
                    continue
                # Only sagital plane (y) of interest
                angle = np.array(joint_data[side+'_'+joint+'_y'])[r]
                angle_rs = ss.resample_poly(angle,resample_len,len(r),padtype='line')
                ax[i_joint][i_side].plot(t_axis,angle_rs)
                ax[i_joint][i_side].set_title(joint)
                
                if i_joint == len(joints_order)-1:
                    ax[i_joint][i_side].set_xlabel('Gait cycle (%)')
                else:
                    ax[i_joint][i_side].set_xticklabels([])

def visualize_emg_run(emg_data,gait_events,resample_len=1000):
    """
    Parameters
    ----------
    joint_data : dict
        Dictonary containing joint data in degrees and a key 'time' in seconds.
    gait_events : dict
        Dictonary containing the gait events for left and right leg, in seconds..

    Returns
    -------
    None

    """
    sides = ['l','r'] # More dynamic: np.unique([key.rsplit('_')[0] for key in joint_data if not 'time' in key])
    muscles = [str(val) for val in np.unique([key.rsplit('_')[0] for key in emg_data if not 'time' in key])]
    time = np.array(joint_data['time'])
    t_axis = np.linspace(0,100,resample_len)
    fig,ax = plt.subplots(nrows=len(muscles),ncols=len(sides),gridspec_kw={'hspace':1})
    for i_side,side in enumerate(sides):
        # Convert gait events from seconds to indices corresponding to time
        hc = np.array([np.argmin(abs(ge-time)) for ge in gait_events[side+'_heel_strike']])
        for i in range(len(hc)-1):
            r = range(hc[i],hc[i+1])
            for i_muscle,muscle in enumerate(muscles):
                # Only sagital plane (y) of interest
                emg = emg_envelope(np.array(emg_data[muscle+'_'+side])[r])
                emg_rs = ss.resample_poly(emg,resample_len,len(r),padtype='line')
                ax[i_muscle][i_side].plot(t_axis,emg_rs)
                ax[i_muscle][i_side].set_title(muscle)
                if i_muscle == len(muscles)-1:
                    ax[i_muscle][i_side].set_xlabel('Gait cycle (%)')
                else:
                    ax[i_muscle][i_side].set_xticklabels([])



#%% Data of 1 run
path_saving = 'Data'
subject = '00'
cond = '5'
run = '01'
for file in os.listdir(path_saving):
    # Check whether it is subject and condition of interest
    file_subj = file.rsplit('subject_')[-1].rsplit('_')[0]
    file_cond = file.rsplit('cond_')[-1].rsplit('_')[0]
    file_run = file.rsplit('run_')[-1].rsplit('_')[0]
    if not (file_subj == subject and file_cond == cond and file_run == run):
        continue
    if 'gaitEvents' in file:
        with open(os.path.join(path_saving,file),'r') as yaml_file:
            gait_events = yaml.safe_load(yaml_file)

    elif 'jointAngle' in file:
        joint_data = pd.read_csv(os.path.join(path_saving,file),sep=';').to_dict('list') # Load joint data to dict of lists
    elif 'emg' in file:
        emg_data = pd.read_csv(os.path.join(path_saving,file),sep=';').to_dict('list')
visualize_joint_run(joint_data,gait_events)
visualize_emg_run(emg_data,gait_events)

#%% Data of all runs
subject_list = [str(val) for val in np.unique([file.rsplit('subject_')[-1].rsplit('_')[0] for file in os.listdir(path_saving)])]
for subj in subject_list:
    file_subj = file.rsplit('subject_')[-1].rsplit('_')[0]
    if not file_subj == subj:
        continue
    run_list 