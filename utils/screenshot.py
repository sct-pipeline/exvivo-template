##############################################################
#
# This script creates quality controls, by saving axial slices as ".png".
#
# Note: we expect the input to have a RPI orientation.
#
# Usage: python screenshot.py -i <ifile>
#                                   -s <seg_file>  # optional
#                                   -c <color_map> # optional
#                                   -z <z_slice_idxes>
#                                   -o <ofolder>
#
# Example: python screenshot.py -i img.nii.gz
#                                   -s img_seg.nii.gz
#                                   -c Reds
#                                   -z 26,51
#                                   -o qc
#
##############################################################

import os
import numpy as np
import argparse
import matplotlib.pyplot as plt

import sys
sys.path.append(os.popen('echo $SCT_DIR').readlines()[0][:-1])

from spinalcordtoolbox.image import Image


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input filename.")
    parser.add_argument("-z", help="Index(es) of axial slice, separated by comma.")
    parser.add_argument("-s", help="Segmentation filename (optional).")
    parser.add_argument("-c", help="Matplotlib color map (optional).")
    parser.add_argument("-o", help="Output filename.")

    return parser


def screenshot_w_seg(im_lst, seg_lst, cmap, fname_out_lst):
    for im, seg, fname_out in zip(im_lst, seg_lst, fname_out_lst):
        plt.figure()
        plt.subplot(1, 1, 1)
        plt.axis("off")

        i_zero, i_nonzero = np.where(seg==0.0), np.nonzero(seg)
        cm = plt.get_cmap(cmap)
        img_jet = cm(plt.Normalize(vmin=0, vmax=1)(seg))
        img_jet[i_zero] = 0.0
        bkg_grey = plt.cm.binary_r(plt.Normalize(vmin=np.amin(im), vmax=np.amax(im))(im))
        img_out = np.copy(bkg_grey)
        img_out[i_nonzero] = img_jet[i_nonzero]

        plt.imshow(img_out, interpolation='nearest', aspect='auto')

        plt.savefig(fname_out, bbox_inches='tight', pad_inches=0)
        plt.close()


def screenshot(im_lst, fname_out_lst):
    for i, f in zip(im_lst, fname_out_lst):
        plt.figure()
        plt.subplot(1, 1, 1)
        plt.axis("off")

        plt.imshow(i, interpolation='nearest', aspect='auto', cmap='gray')

        plt.savefig(f, bbox_inches='tight', pad_inches=0)
        plt.close()


def run_main(args):
    im_fname = args.i
    z_lst = [int(z) for z in args.z.split(',')]
    seg_fname = args.s if 's' in args else None
    cmap = args.c if 'c' in args else None
    ofolder = args.o

    # create ofolder if does not exist
    if not os.path.isdir(ofolder):
        os.makedirs(ofolder)

    im_lst, fname_out_lst = [], []
    im = Image(im_fname)

    for z in z_lst:
        im_lst.append(im.data[:, :, z])
        fname_out_lst.append(os.path.join(ofolder, str(z).zfill(3)+'.png'))
    del im

    if seg_fname and cmap:
        seg_lst = []
        seg = Image(seg_fname)
        for z in z_lst:
            seg_lst.append(seg.data[:, :, z])
        del seg

        screenshot_w_seg(im_lst, seg_lst, cmap, fname_out_lst)

    else:
        screenshot(im_lst, fname_out_lst)

if __name__ == '__main__':
    parser = get_parser()
    arguments = parser.parse_args()
    run_main(arguments)
