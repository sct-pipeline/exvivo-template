##############################################################
#
# This script computes the validation metrics. XX
#
# Usage: python validation_exvivo.py -i <ifolder>
#                                   -t <template_folder>
#                                   -o <ofolder>
#
# Example: python validation_exvivo.py XX
#
##############################################################

import os
import numpy as np
import argparse
import pandas as pd
import maths
from scipy.ndimage.measurements import center_of_mass

import sys
sys.path.append(os.popen('echo $SCT_DIR').readlines()[0][:-1])

from spinalcordtoolbox.image import Image


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input folder.")
    parser.add_argument("-t", help="Template folder.")
    parser.add_argument("-o", help="Output folder.")

    return parser


def compare_ctrl(i, i_ref, px):
    dist_lst = []

    for z in list(np.unique(np.where(i_ref)[2])):
        if np.sum(i[:,:,z]):
            x_ref, y_ref = center_of_mass(i_ref[:,:,z])
            x, y = center_of_mass(i[:,:,z])
            dist = math.sqrt( ((x-x_ref)**2)+((y-y_ref)**2) ) * px
            dist_lst.append(dist)

    return mean(dist_lst), max(dist_lst)


def compare_gm(i, i_ref):
    dice_lst = []
    for z in list(np.unique(np.where(i_ref)[2])):
        if np.sum(i[:,:,z]):
            im1 = np.asarray(i[:,:,z]).astype(np.bool)
            im2 = np.asarray(i_ref[:,:,z]).astype(np.bool)

            if im1.shape != im2.shape:
                raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

            im_sum = im1.sum() + im2.sum()

            intersection = np.logical_and(im1, im2)
            dice_lst.append((2. * intersection.sum())/ im_sum)

    return mean(dice_lst)


def compute_metrics(vals):
    vals = [v for v in vals if v != -1]
    print('\tMedian: '+str(round(np.median(vals),3)))
    print('\tIQR: '+str(round(np.percentile(vals,25),3))+' - '+str(round(np.percentile(vals,75),3)))


def run_main(args):
    ifolder = args.i
    tfolder = args.t
    ofolder = args.o

    # create ofolder if does not exist
    if not os.path.isdir(ofolder):
        os.makedirs(ofolder)

    subj_lst = list(set([f.split('_')[0] for f in os.listdir(ifolder) if os.path.isfile(os.path.join(ifolder, f))]))

    # init pandas
    df = pd.DataFrame(columns=['subject', 'ctr_mean_dist', 'ctr_max_dist', 'gm_mean_dice'])

    # open template files
    fname_template_sc = os.path.join(tfolder, 'template_sc.nii.gz')
    fname_template_gm = os.path.join(tfolder, 'template_gm.nii.gz')
    i_t_sc, i_t_gm = Image(fname_template_sc), Image(fname_template_gm)
    d_t_sc, d_t_gm = i_t_sc.data.astype(np.int), (i_t_gm.data > 0.5).astype(np.int)
    px = i_t_sc.dim[4]
    del i_t_sc, i_t_gm

    # loop across subjects
    for idx, subj in enumerate(subj_lst):
        fname_sc = os.path.join(ifolder, subj+'_seg.nii.gz')
        fname_gm = os.path.join(ifolder, subj+'_gmseg.nii.gz')

        if os.path.isfile(fname_sc):
            i_sc = Image(fname_sc)
            # compute mean and max distance between centerlines
            mean_dist, max_dist = compare_ctrl(i_sc.data, d_t_sc, px)
            del i_sc
        else:
            mean_dist, max_dist = -1, -1

        if os.path.isfile(fname_gm):
            i_gm = Image(fname_gm)
            # compute Dice scores between gm masks
            dice_gm = compare_gm((i_gm.data > 0.5).astype(np.int), d_t_gm)
            del i_gm
        else:
            dice_gm = -1

        df.loc[idx, 'subject'] = subj
        df.loc[idx, 'ctr_mean_dist'] = mean_dist
        df.loc[idx, 'ctr_max_dist'] = max_dist
        df.loc[idx, 'gm_mean_dice'] = dice_gm

    compute_metrics()

    print(df)

    print('\nCenterline Mean Distance:')
    compute_metrics(df['ctr_mean_dist'].values)
    print('\nCenterline Max Distance:')
    compute_metrics(df['ctr_max_dist'].values)
    print('\nGM Dice score:')
    compute_metrics(df['gm_mean_dice'].values)

if __name__ == '__main__':
    parser = get_parser()
    arguments = parser.parse_args()
    run_main(arguments)
