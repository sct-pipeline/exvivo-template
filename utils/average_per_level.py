##############################################################
#
# This script creates averages axial slices per spinal level
#   and saves them as ".png".
#
# Usage: python average_per_level.py -i <ifile>
#                                   -s <seg_file>
#                                   -l <label_file>
#                                   -p <prob_file> # optional
#                                   -c <color_map> # optional
#                                   -o <ofolder>
#
# Example: python average_per_level.py -i img.nii.gz
#                                   -s img_seg.nii.gz
#                                   -l img_labels.nii.gz
#                                   -p img_gm.nii.gz
#                                   -c Reds
#                                   -o fig
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
    parser.add_argument("-s", help="SC segmentation filename.")
    parser.add_argument("-l", help="Labels filename.")
    parser.add_argument("-p", help="Probability map (optional).")
    parser.add_argument("-c", help="Matplotlib color map (optional).")
    parser.add_argument("-o", help="Output folder.")

    return parser


def save_samples(i_dct, ofolder, p_dct=None, cmap=None):
    for i in i_dct:
        im = i_dct[i]

        plt.figure(figsize=(10, 10))
        plt.subplot(1, 1, 1)
        plt.axis("off")

        if p_dct and cmap:
            fname_out = os.path.join(ofolder, str(i).zfill(2)+'_prob.png')

            prob = p_dct[i]

            i_zero, i_nonzero = np.where(prob==0.0), np.nonzero(prob)
            cm = plt.get_cmap(cmap)
            img_cmap = cm(plt.Normalize(vmin=0, vmax=1)(prob))
            img_cmap[i_zero] = 0.0
            bkg_grey = plt.cm.binary_r(plt.Normalize(vmin=np.amin(im), vmax=np.amax(im))(im))
            img_out = np.copy(bkg_grey)
            img_out[i_nonzero] = img_cmap[i_nonzero]

            plt.imshow(img_out, interpolation='nearest', aspect='auto')

        else:
            fname_out = os.path.join(ofolder, str(i).zfill(2)+'.png')

            plt.imshow(im, interpolation='nearest', aspect='auto', cmap='gray')

        plt.savefig(fname_out, bbox_inches='tight', pad_inches=0)
        plt.close()


def get_label_zlim(data):
    dct = {}
    for v in np.unique(data):
        if v:
            dct[v] = np.where(data == v)[2][0]

    return dct


def get_mid(data, data_sc, z_dct):
    sample_dct = {}
    for i in range(1, 15):
        if i in z_dct and 1+i in z_dct:
            z_mid = int(round((z_dct[i]+1-z_dct[i+1])*1.0/2)) + z_dct[i+1]
            data_zmid = data[:,:,z_mid]
            data_sc_zmid = data_sc[:,:,z_mid]
            data_zmid[np.where(data_sc_zmid == 0)] = 0
            sample_dct[i] = np.rot90(data_zmid)

    return sample_dct


def get_average(data, data_sc, z_dct):
    sample_dct = {}
    for i in range(1, 15):
        if i in z_dct and 1+i in z_dct:
            data_lst, mask_lst = [], []
            for zz in range(z_dct[i+1], z_dct[i]+1):
                if np.sum(data_sc[:, :, zz]):
                    data_lst.append(data[:, :, zz])
                    mask_lst.append(data_sc[:, :, zz])

            if len(mask_lst):
                data_cur, mask_cur = np.stack(data_lst, axis=2), np.stack(mask_lst, axis=2)
                data_cur[np.where(mask_cur == 0)] = 0
                sample = np.mean(data_cur, axis=2)
                sample[sample<0.2]=0
                print(np.unique(sample))
                sample_dct[i] = np.rot90(sample)

    return sample_dct


def run_main(args):
    fname_im = args.i
    fname_sc = args.s
    fname_lb = args.l
    fname_prob = None if 'p' not in args else args.p
    cmap = None if 'c' not in args else args.c
    ofolder = args.o

    # create ofolder if does not exist
    if not os.path.isdir(ofolder):
        os.makedirs(ofolder)

    # load images
    im, mask, lb = Image(fname_im).data, Image(fname_sc).data, Image(fname_lb).data
    prob = Image(fname_prob).data if fname_prob else None
    
    # get zlim of labels
    zlim_dct = get_label_zlim(lb)

    # average data per level
    #sample_dct = get_average(data=im,
    #                            data_sc=mask,
    #                            z_dct=zlim_dct)
    sample_dct = get_mid(data=im,
                                data_sc=mask,
                                z_dct=zlim_dct)
    # save samples
    save_samples(i_dct=sample_dct,
                    ofolder=ofolder)

    # if prob, then overlay image and prob
    if prob is not None:
        prob_dct = get_average(prob, mask, zlim_dct)
        #prob_dct = get_mid(prob, mask, zlim_dct)
        save_samples(i_dct=sample_dct,
                        ofolder=ofolder,
                        p_dct=prob_dct,
                        cmap=cmap)

if __name__ == '__main__':
    parser = get_parser()
    arguments = parser.parse_args()
    run_main(arguments)
