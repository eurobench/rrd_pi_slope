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

def visualize_emg_run(emg_data, gait_events,resample_len=1000):
    """
    Parameters
    ----------
    emg_data : dict
        Dictonary containing emg data and a key 'time' in seconds.
    gait_events : dict
        Dictonary containing the gait events for left and right leg, in seconds..

    Returns
    -------
    None

    """
    sides = ['l','r'] # More dynamic: np.unique([key.rsplit('_')[0] for key in joint_data if not 'time' in key])
    muscles = [str(val) for val in np.unique([key.rsplit('_')[0] for key in emg_data if not 'time' in key])]
    time = np.array(emg_data['time'])
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

def main(fn_emg, fn_gait_event, fn_joint, folder_out):

    emg_data = pd.read_csv(fn_emg, sep=';').to_dict('list')
    # TODO check file is read correctly
    with open(fn_gait_event,'r') as yaml_file:
        gait_events = yaml.safe_load(yaml_file)

    visualize_emg_run(emg_data, gait_events)
