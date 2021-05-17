# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:00:13 2021

@author: rschulte
"""

import yaml
import numpy as np
import os

def get_gait_spatiotemporal_params(gait_events):
    """
    Parameters
    ----------
    gait_events : dict
        Dictonary containing the gait events for left and right leg, in seconds.

    Returns
    -------
    params : dict.
        Dictonary containing the gait phases of interest:
            As fraction of gait cycle for left and right:
            - Stance phase
            - Swing phase
            - Single Support phase
            - Double support phase 1
            - Double support phase 2
            In seconds for left and right:
            - Gait cycle
            In steps per minute:
            - Cadence
    """
     # Initialize params
    sides = ['l','r']
    params = {}


    # Determine single leg gait phases
    for side in sides:
        hc = gait_events[side+'_heel_strike']
        to = gait_events[side+'_toe_off']
        t_gc = [float(val) for val in np.diff(hc)]
        params[side+'_t_gait_cycle'] = t_gc
        if hc[0] < to[0]:
            # Starts with heel strike
            params[side+'_t_stance'] = [(to[i]-hc[i])/t_gc[i] for i in range(np.min([len(to),len(hc)]))]
        else:
            # Starts with toe-off
            params[side+'_t_stance'] = [(to[i+1]-hc[i])/t_gc[i] for i in range(np.min([len(to)-1,len(hc)]))]
        params[side+'_t_swing'] = [1 - val for val in params[side+'_t_stance']]

    # Double support phases
    l_hc, l_to = gait_events['l_heel_strike'],gait_events['l_toe_off']
    r_hc, r_to = gait_events['r_heel_strike'],gait_events['r_toe_off']

    all_gait_events = np.sort(np.concatenate([l_hc,l_to,r_hc,r_to]))
    ds = {side:[] for side in sides}
    for i in range(len(all_gait_events)-1):
        if all_gait_events[i] in l_hc and all_gait_events[i+1] in r_to:
            ds['l'].append(all_gait_events[i+1]-all_gait_events[i])
        elif all_gait_events[i] in r_hc and all_gait_events[i+1] in l_to:
            ds['r'].append(all_gait_events[i+1]-all_gait_events[i])
    for i_side,side in enumerate(sides):
        other_side = sides[abs(i_side-1)]
        t_gc = params[side+'_t_gait_cycle']
        ds_1 = [ds[side][i]/t_gc[i] for i in range(np.min([len(t_gc),len(ds[side])]))]
        ds_2 = [ds[other_side][i]/t_gc[i] for i in range(np.min([len(t_gc),len(ds[other_side])]))]
        params[side+'_t_double_support1'] = ds_1
        params[side+'_t_double_support2'] = ds_2
        # single support
        t_stance = params[side+'_t_stance']
        params[side+'_t_single_support'] = [t_stance[i]-ds_1[i]-ds_2[i] for i in range(np.min([len(t_stance),len(ds_1),len(ds_2)]))]

    # Cadence
    all_hc = np.sort(np.concatenate([l_hc,r_hc])) # steps
    params['cadence'] = 60/np.diff(all_hc) # steps per minute

    return params

def print_spatiotemporal_params(params):
    for key in params:
        if key.startswith('l') and not 'gait_cycle' in key:
            print('Left {}: {:.1f} +/- {:.1f}%'.format(key[2:],np.mean(params[key])*100,np.std(params[key])*100))
        elif key.startswith('r') and not 'gait_cycle' in key:
            print('Right {}: {:.1f} +/- {:.1f}%'.format(key[2:],np.mean(params[key])*100,np.std(params[key])*100))
        elif 'cadence' in key:
            print('Cadence: {:.1f} +/- {:.1f} SPM'.format(np.mean(params[key]),np.std(params[key])))
    print("All data:\n {}".format(params))

def store_gait_values(params, filename):

    with open(filename, 'w') as my_file:
        my_file.write('type: vector\n')

        labels = []
        values = []
        for key in params:
            if key.startswith('l') and not 'gait_cycle' in key:
                labels.append('left {}'.format(key[4:]))
                values.append(np.mean(params[key])*100)
            elif key.startswith('r') and not 'gait_cycle' in key:
                labels.append('right {}'.format(key[4:]))
                values.append(np.mean(params[key])*100)

        labels = ', '.join(str(x) for x in labels)
        values = ', '.join('{:.1f}'.format(x) for x in values)
        my_file.write('label: [{}]\n'.format(labels))
        my_file.write('value: [{}]\n'.format(values))
    return True

def store_cadence_value(params, filename):

    with open(filename, 'w') as my_file:
        my_file.write('type: scalar\n')
        my_file.write('value: {:.1f}\n'.format(np.mean(params['cadence'])))
    return True

def main(fn_gait, folder_out):

    # al is fine, continue

    # TODO check file is read correctly
    with open(fn_gait,'r') as yaml_file:
        gait_events = yaml.safe_load(yaml_file)

    # Determine gait phases
    params = get_gait_spatiotemporal_params(gait_events)
    print_spatiotemporal_params(params)
    filename = "{}/pi_gait_phase_duration.yaml".format(folder_out)
    store_gait_values(params, filename)
    filename = "{}/pi_cadence.yaml".format(folder_out)
    store_cadence_value(params, filename)

    return 0

if __name__ == '__main__':
    #%% Load data
    path_saving = 'Data'
    subject = '00'
    cond = '5'
    for file in os.listdir(path_saving):
        # Check whether it is subject and condition of interest
        file_subj = file.rsplit('subject_')[-1].rsplit('_')[0]
        file_cond = file.rsplit('cond_')[-1].rsplit('_')[0]
        if not (file_subj == subject and file_cond == cond):
            continue
        if 'gaitEvents' in file:
            with open(os.path.join(path_saving,file),'r') as yaml_file:
                gait_events = yaml.safe_load(yaml_file)
            # Determine gait phases
            params = get_gait_spatiotemporal_params(gait_events)
            print_spatiotemporal_params(params)