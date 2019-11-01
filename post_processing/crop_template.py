##############################################################
#
# This script crops all "template_*" files in the input folder (ifolder),
# between the extreme labels of "template_label_top_spinal_levels.nii.gz".
# Croped files are saved in the output folder (ofolder).
#
# Usage: python crop_template.py -i <ifolder> -o <ofolder>
#
# Example: python crop_template.py -i ~/exvivo_template/ -o ~/exvivo_template/crop/
#
##############################################################

import os
import numpy as np
import argparse

import sys
sys.path.append(os.popen('echo $SCT_DIR').readlines()[0][:-1]+"/scripts")

import sct_crop_image
from spinalcordtoolbox.image import Image, zeros_like


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input folder.")
    parser.add_argument("-o", help="Output folder.")

    return parser


def get_label_z(data):
    dct = {}
    for v in np.unique(data):
        if v:
            dct[v] = np.where(data == v)[2][0]

    return dct


def run_main(args):
    ifolder = args.i
    ofolder = args.o

    # create ofolder if does not exist
    if not os.path.isdir(ofolder):
        os.makedirs(ofolder)

    fname_top_labels = os.path.join(ifolder, 'template_label_top_spinal_levels.nii.gz')
    if os.path.isfile(fname_top_labels):

        # get crop zlim
        im_top = Image(fname_top_labels)
        z_top_dct = get_label_z(im_top.data)
        lb_lst = list(z_top_dct.keys())
        z_min, z_max = str(z_top_dct[min(lb_lst)]+1), str(z_top_dct[max(lb_lst)])
        del im_top

        # crop all images starting with "template_*"
        for f in os.listdir(ifolder):
            if f.startswith("template"):
                fname_in = os.path.join(ifolder, f)
                fname_out = os.path.join(ofolder, f)

                sct_crop_image.main(['-i', fname_in,
                                        '-o', fname_out,
                                        '-zmin', z_min,
                                        '-zmax', z_max])

    else:
        print('Cannot find: '+fname_top_labels)


if __name__ == '__main__':
    parser = get_parser()
    arguments = parser.parse_args()
    run_main(arguments)
