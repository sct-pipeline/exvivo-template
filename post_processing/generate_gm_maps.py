##############################################################
#
# This script generates the GM probabilistic maps.
#
# Note: we expect the input to have a RPI orientation.
#
# Usage: python generate_gm_maps.py -i <ifolder>
#                                   -o <ofolder>
#
# Example: XX
#
##############################################################

import os
import numpy as np
import argparse

import sys
sys.path.append(os.popen('echo $SCT_DIR').readlines()[0][:-1])

from spinalcordtoolbox.image import Image, zeros_like


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input folder.")
    parser.add_argument("-o", help="Output folder.")

    return parser


def run_main(args):
    ifolder = args.i
    ofolder = args.o

    # create ofolder if does not exist
    if not os.path.isdir(ofolder):
        os.makedirs(ofolder)
    """
    # flip data
    for f in os.listdir(ifolder):
        if f.endswith('gmseg.nii.gz'):
            fname_in = os.path.join(ifolder, f)
            fname_out = os.path.join(ifolder, f.split('.nii.gz')[0]+'_flip.nii.gz')
            im_in = Image(fname_in)
            im_out = zeros_like(im_in)
            im_out.data = np.flip(im_out.data, axis=0)
            im_out.save(fname_out)
            del im_in, im_out
    """
    # average data
    fname_out = os.path.join(ofolder, 'template_gm_bis.nii.gz')
    im_lst = [Image(os.path.join(ifolder,f)) for f in os.listdir(ifolder) if 'gmseg.nii.gz' in f]
    im_out = zeros_like(im_lst[0])
    im_data_lst = np.array([i.data for i in im_lst])
    im_data_sum = np.sum(im_data_lst, axis=0)
    print(im_data_lst.shape, im_data_sum.shape)
    for zz in range(im_data_sum.shape[2]):
        if np.sum(im_data_sum[:,:,zz]):
            n_subj = int(np.max(im_data_sum[:,:,zz]))
            n_subj = n_subj if n_subj > 0 else 1
            im_out.data[:,:,zz] = im_data_sum[:,:,zz] / n_subj

    print(im_out.data.shape)
    im_out.save(fname_out)

if __name__ == '__main__':
    parser = get_parser()
    arguments = parser.parse_args()
    run_main(arguments)
