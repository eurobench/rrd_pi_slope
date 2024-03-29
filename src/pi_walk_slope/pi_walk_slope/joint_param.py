# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 12:51:22 2021

@author: rschulte
"""

import yaml
import numpy as np
import os
import pandas as pd

def get_joint_params(joint_data,gait_events):
    """
    Parameters
    ----------
    joint_data : dict
        Dictonary containing joint data in degrees and a key 'time' in seconds.
    gait_events : dict
        Dictonary containing the gait events for left and right leg, in seconds..

    Returns
    -------
    joint_params : dict
        Dictonary containing joint parameters of interest.

    """
    joint_params = {}
    sides = ['l','r'] # More dynamic: np.unique([key.rsplit('_')[0] for key in joint_data if not 'time' in key])
    joints = [str(val) for val in np.unique([key.rsplit('_')[1] for key in joint_data if not 'time' in key])]
    time = np.array(joint_data['time'])
    for side in sides:
        # Convert gait events from seconds to indices corresponding to time
        to_ = [np.argmin(abs(ge-time)) for ge in gait_events[side+'_toe_off']]
        hc_ = [np.argmin(abs(ge-time)) for ge in gait_events[side+'_heel_strike']]
        
        # Check order of to/hc for missing samples
        to,hc = check_order(to_,hc_)
        to,hc = np.array(to),np.array(hc) # Convert to arrays
        
        if hc[0] < to[0]:
            # Starts with heel strike
            stance_range = [range(hc[i],to[i]) for i in range(np.min([len(to),len(hc)]))]
            swing_range = [range(to[i],hc[i+1]) for i in range(np.min([len(to),len(hc)-1]))]
        else:
            # Starts with toe off
            stance_range = [range(hc[i],to[i+1]) for i in range(np.min([len(to)-1,len(hc)]))]
            swing_range = [range(to[i],hc[i]) for i in range(np.min([len(to),len(hc)]))]

        for joint in joints:
            # Only sagital plane (y) of interest
            angle = np.array(joint_data[side+'_'+joint+'_y'])

            # Angle at initial contact
            joint_params[side+'_'+joint+'_ic'] = [angle[i] for i in hc]

            # Angle at toe off
            joint_params[side+'_'+joint+'_to'] = [angle[i] for i in to]

            # Maximal angle during swing
            joint_params[side+'_'+joint+'_max_swing'] = [angle[r].max() for r in swing_range]

            # Maximal angle during stance
            joint_params[side+'_'+joint+'_max_stance'] = [angle[r].max() for r in stance_range]

    return joint_params

def print_joint_params(params):
    for key in params:
        if key.startswith('l'):
            print('Left {}: {:.1f} +/- {:.1f} deg'.format(key[2:],np.mean(params[key]),np.std(params[key])))
        elif key.startswith('r') and not 'gait_cycle' in key:
            print('Right {}: {:.1f} +/- {:.1f} deg'.format(key[2:],np.mean(params[key]),np.std(params[key])))

def check_order(list_a: list,list_b: list):
    """
    This function checks whether the order of the combined lists matches the
    pattern [a0,b0,a1,b1..an,bn]. If not, it finds the longest occurence of 
    the pattern and returns the new lists.
    
    Parameters
    ----------
    list_a : list
        list containing ordered values of a
    list_b : list
        list containing ordered values of b

    Returns
    -------
    list_a_new : list
    list_b_new: list
        
    """
    combined = np.sort(list_a+list_b)
    
    # Find where pattern is a,b,a,b,etc
    arr = abs(np.diff(np.array([x in list_a for x in combined]).astype(int)))
    
    # If the difference between subsequent values is not 1, the pattern does not match
    pattern_arr = np.split(combined,np.where(arr!=1)[0]+1)
    
    # Find longest occurence of pattern
    longest_arr = pattern_arr[np.argmax([arr.size for arr in pattern_arr])]
    
    # Reconstruct list_a & list_b
    if longest_arr[0] in list_a: # If a0 is earlier than b0
        list_a_new = longest_arr[::2]
        list_b_new = longest_arr[1:][::2]
    else: 
        list_a_new = longest_arr[1:][::2]
        list_b_new = longest_arr[::2]
    return list_a_new, list_b_new


def store_values(params, filename):

    with open(filename, 'w') as my_file:
        my_file.write('type: vector\n')

        labels = []
        values = []
        for key in params:
            if key.startswith('l'):
                labels.append('left {}'.format(key[2:]))
                values.append(np.mean(params[key]))
            elif key.startswith('r') and not 'gait_cycle' in key:
                labels.append('right {}'.format(key[2:]))
                values.append(np.mean(params[key]))

        labels = ', '.join(str(x) for x in labels)
        values = ', '.join('{:.1f}'.format(x) for x in values)
        my_file.write('label: [{}]\n'.format(labels))
        my_file.write('value: [{}]\n'.format(values))

    return True

def main(fn_gait, fn_joint, folder_out):

    # al is fine, continue

    # TODO check file is read correctly
    with open(fn_gait,'r') as yaml_file:
        gait_events = yaml.safe_load(yaml_file)

    # Load joint data to dict of lists
    joint_data = pd.read_csv(fn_joint, sep=';').to_dict('list')

    # Get joint parameters
    joint_params = get_joint_params(joint_data, gait_events)
    print_joint_params(joint_params)
    filename = "{}/pi_joint_kinematics.yaml".format(folder_out)
    store_values(joint_params, filename)
    return 0

if __name__ == '__main__':
    #%% Load data
    path_saving = 'Data'
    subject = '00'
    cond = '5'
    run = '00'
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

    # Get joint parameters
    joint_params = get_joint_params(joint_data,gait_events)
    print_joint_params(joint_params)
