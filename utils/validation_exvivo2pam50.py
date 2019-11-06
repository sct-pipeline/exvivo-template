##############################################################
#
# This script computes the validation metrics. XX
#
# Usage: python validation_exvivo2PAM50.py -i <i_file>
#                                           -t <t_file>
#
# Example: python validation_exvivo2PAM50.py XX
#
##############################################################

import os
import numpy as np
import argparse
import pandas as pd

import sys
sys.path.append(os.popen('echo $SCT_DIR').readlines()[0][:-1])

from spinalcordtoolbox.image import Image


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input file.")
    parser.add_argument("-t", help="Template file.")

    return parser


def compare_sc(i, i_ref):
    dice_lst = []
    for z in list(np.unique(np.where(i_ref)[2])):
        if np.sum(i[:,:,z]) >= 0.5 * np.sum(i_ref[:,:,z]):
            im1 = np.asarray(i[:,:,z]).astype(np.bool)
            im2 = np.asarray(i_ref[:,:,z]).astype(np.bool)

            if im1.shape != im2.shape:
                raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

            im_sum = im1.sum() + im2.sum()

            intersection = np.logical_and(im1, im2)
            dice_lst.append((2. * intersection.sum())/ im_sum)

    return dice_lst


def compute_metrics(vals):
    vals = [v for v in vals if v != -1]
    print('\tMedian: '+str(round(np.median(vals),3)))
    print('\tIQR: '+str(round(np.percentile(vals,25),3))+' - '+str(round(np.percentile(vals,75),3)))


def run_main(args):
    ifile = args.i
    tfile = args.t

    i_exvivo, i_pam50 = Image(ifile), Image(tfile)
    d_exvivo, d_pam50 = (i_exvivo.data > 0.5).data.astype(np.int), (i_pam50.data > 0.5).astype(np.int)

    # compute Dice scores between masks
    dice_res = compare_sc(d_exvivo, d_pam50)

    print('\nDice score:')
    compute_metrics(dice_res)

if __name__ == '__main__':
    parser = get_parser()
    arguments = parser.parse_args()
    run_main(arguments)
