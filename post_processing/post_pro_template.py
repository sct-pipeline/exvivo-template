##############################################################
#
# This script performs post-processing of the template image.
# This includes:
#   - intensity normalisation along (IS) within the spinal cord
#   - intensity smoothing along (IS) within the spinal cord
#
# Usage: python post_pro_template.py -i <i_file>
#                                      -s <sc_file
#                                      -o <ofolder>
#
# Example: python post_pro_template.py -i template.nii.gz
#                                       -s template_sc.nii.gz
#                                       -o template_pp
#
##############################################################

import os
import shutil
import numpy as np
import argparse

import sys
sys.path.append(os.popen('echo $SCT_DIR').readlines()[0][:-1])
sys.path.append(os.popen('echo $SCT_DIR').readlines()[0][:-1]+"/scripts")

import sct_smooth_spinalcord
from spinalcordtoolbox.image import Image, zeros_like


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input file.")
    parser.add_argument("-s", help="SC segmentation filename.")
    parser.add_argument("-o", help="Output folder.")

    return parser


def smooth_spinalcord(i, s):
    os.system("sct_smooth_spinalcord -i "+ i + " -s " + s)


def norm_image(fname_image, fname_mask, fname_out):
    image, mask = Image(fname_image), Image(fname_mask)
    nx, ny, nz, nt, px, py, pz, pt = image.dim
    z_values = list(set(np.where(mask.data)[2]))

    # Compute intensity values
    intensities = []
    for i in z_values:
        img_z, mask_z = image.data[:, :, i], mask.data[:, :, i]
        intensities.append(np.mean(img_z[np.where(mask_z)]))

    # Preparing data for smoothing
    arr_int = [[z_values[i], intensities[i]] for i in range(len(z_values))]
    arr_int.sort(key=lambda x: x[0])  # and make sure it is ordered with z

    def smooth(x, window_len=11, window='hanning'):
        """smooth the data using a window with requested size.
        """

        if x.ndim != 1:
            raise ValueError("smooth only accepts 1 dimension arrays.")

        if x.size < window_len:
            raise ValueError("Input vector needs to be bigger than window size.")

        if window_len < 3:
            return x

        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

        s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
        if window == 'flat':  # moving average
            w = np.ones(window_len, 'd')
        else:
            w = eval('np.' + window + '(window_len)')

        y = np.convolve(w / w.sum(), s, mode='same')
        return y[window_len - 1:-window_len + 1]

    # Smoothing
    intensities = [c[1] for c in arr_int]
    intensity_profile_smooth = smooth(np.array(intensities), window_len=10)

    # set the average image intensity over the entire dataset
    average_intensity = 1000.0

    # normalize the intensity of the image based on spinal cord
    nx, ny, nz, nt, px, py, pz, pt = image.dim

    image_image_new = zeros_like(image)
    image_image_new.change_type(dtype='float32')
    for i, ii in enumerate(z_values):
        data_ii, mask_ii = image.data[:, :, ii], mask.data[:, :, ii]
        data_ii[mask_ii == 0] = 0.0
        data_ii *= average_intensity / intensity_profile_smooth[i]
        image_image_new.data[:, :, ii] = data_ii

    # Save intensity normalized template
    image_image_new.save(fname_out)


def run_main(args):
    ifname = args.i
    sfname = args.s
    ofolder = args.o

    # temp folder
    tmpfolder = os.path.join(ofolder, 'tmp_pp_template')

    # create ofolder if does not exist
    if not os.path.isdir(ofolder):
        os.makedirs(ofolder)
    if not os.path.isdir(tmpfolder):
        os.makedirs(tmpfolder)

    fname_norm = os.path.join(tmpfolder, 'tmp_norm.nii.gz')
    norm_image(fname_image=ifname,
                fname_mask=sfname,
                fname_out=fname_norm)

    print('hey')
    smooth_spinalcord(i=fname_norm,
                        s=sfname)
    print('ah')
    fname_smooth = 'tmp_norm_smooth.nii.gz'
    fname_out = os.path.join(ofolder, 'template_pp.nii.gz')
    shutil.copyfile(fname_smooth, fname_out)
    print(fname_smooth, fname_out, os.getcwd())

if __name__ == '__main__':
    parser = get_parser()
    arguments = parser.parse_args()
    run_main(arguments)
