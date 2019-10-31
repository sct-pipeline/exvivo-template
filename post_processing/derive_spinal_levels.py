##############################################################
#
# This script generates:
#   - template_centerline_spinal_levels.nii.gz --> continuous
#   - template_label_spinal_levels.nii.gz --> discrete, mid spinal level
# from:
#   - template_label_top_spinal_levels.nii.gz --> discrete, top spinal level
#
# Usage: python derive_spinal_levels.py -i <ifolder>
#
# Example: python derive_spinal_levels.py -i ~/exvivo_template/
#
##############################################################

import os
import numpy as np
import argparse

from spinalcordtoolbox.image import Image, zeros_like


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input folder.")

    return parser


def get_label_z(data):
    dct = {}
    for v in np.unique(data):
        if v:
            dct[v] = np.where(data == v)[2][0]

    return dct


def run_main(args):
    ifolder = args.i

    fname_top = os.path.join(ifolder, 'template_label_top_spinal_levels.nii.gz')
    fname_mid = os.path.join(ifolder, 'template_label_spinal_levels.nii.gz')
    fname_continuous = os.path.join(ifolder, 'template_centerline_spinal_levels.nii.gz')
    fname_ctrl = os.path.join(ifolder, 'template_centerline.nii.gz')

    if all([os.path.isfile(f) for f in [fname_top, fname_ctrl]]):
        im_top, im_ctrl = Image(fname_top), Image(fname_ctrl)
        im_mid, im_continuous = zeros_like(im_top), zeros_like(im_top)

        # get z coordinate of the labels at the top of each level
        z_top_dct = get_label_z(im_top.data)
        lb_lst = list(z_top_dct.keys())
        del im_top

        # fill im_continuous and im_mid
        for lb in lb_lst:
            if (lb+1) in lb_lst:
                z_min_lb, z_max_lb = z_top_dct[lb+1]+1, z_top_dct[lb]
                im_continuous.data[:,:,z_min_lb:z_max_lb+1] = lb * im_ctrl.data[:,:,z_min_lb:z_max_lb+1]

                z_mid_lb = z_min_lb+int(round((z_max_lb-z_min_lb)*1.0 / 2))
                im_mid.data[:,:,z_mid_lb] = lb * im_ctrl.data[:,:,z_mid_lb]

        # save outputs
        im_continuous.save(fname_continuous)
        im_mid.save(fname_mid)
        del im_ctrl, im_continuous, im_mid


if __name__ == '__main__':
    parser = get_parser()
    arguments = parser.parse_args()
    run_main(arguments)
