##############################################################
#
# This script applies transformation from raw data to template space.
# For each subject, all these files are registered to the template:
#   - image
#   - SC segmentation
#   - GM segmentation
#   - spinal level labels
# To do so, it uses the transformations:
#   - from the raw space to the preprocesing space
#   - from the preprocessing space to the template space
#
# Note: we expect the ifolder to be organised as follows:
#   subj/
#       t1/
#           t1.nii.gz                   # image
#           t1_seg.nii.gz               # SC seg
#           t1_gmseg.nii.gz             # GM seg
#           t1_labels.nii.gz            # spinal level labels
#           warp_curve2straight.nii.gz  # warping field from raw to prepro space
#           t1_straight.nii.gz          # straighten image
#
# Usage: python apply_transfo.py -i <ifolder>
#                                   -w <warping_field_template_folder>
#                                   -d <destination_file>
#                                   -o <ofolder>
#
# Example: python apply_transfo.py -i ~/data
#                                   -w ~/model_nl_all
#                                   -d ~/template/template.nii.gz
#                                   -o ~/template/subjects/
#
##############################################################

import os
import numpy as np
import argparse

import sys
sys.path.append(os.popen('echo $SCT_DIR').readlines()[0][:-1]+"/scripts")

import sct_utils as sct
import sct_apply_transfo
import sct_convert
import sct_image


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input folder.")
    parser.add_argument("-w", help="Folder containing the warping fields.")
    parser.add_argument("-d", help="Destination filename.")
    parser.add_argument("-o", help="Output folder.")

    return parser


def apply_transfo_sct(i, d, w, o):
    sct_apply_transfo.main(args=[
                                '-i', i,
                                '-d', d,
                                '-w', w,
                                '-o', o,
                                '-x', 'nn',
                                '-v', '0'])


def convert_nii_mnc(nii, mnc):
    sct.run('nii2mnc '+nii+' '+mnc)


def apply_transfo_minc(i, w, o, x):
    cmd = 'mincresample -transformation '+w+' -tfm_input_sampling '+i+' '+o
    if x == 'nn':
        cmd += ' -nearest_neighbour '
    sct.run(cmd)


def convert_mnc_nii(mnc, nii):
    sct_convert.main(args=[
                            '-i', mnc,
                            '-o', nii])


def set_orient(ref, i, i_tmp, o):
    sct_image.main(args=[
                            '-i', ref,
                            '-copy-header', i,
                            '-v', '0'])
    sct_image.main(args=[
                            '-i', i,
                            '-setorient-data', 'IAR',
                            '-o', i_tmp,
                            '-v', '0'])
    sct_image.main(args=[
                            '-i', i_tmp,
                            '-setorient', 'RPI',
                            '-o', o,
                            '-v', '0'])


def run_main(args):
    ifolder = args.i
    wfolder = args.w
    fname_dest = args.d
    ofolder = args.o

    # temp folder
    tmpfolder = os.path.join(ofolder, 'tmp')
    # get last iteration number
    last_it = os.path.basename(os.path.normpath(wfolder))

    # create ofolder if does not exist
    if not os.path.isdir(ofolder):
        os.makedirs(ofolder)
    if not os.path.isdir(tmpfolder):
        os.makedirs(tmpfolder)

    # loop across subjects
    for subj in os.listdir(ifolder)[:1]:
        # straighten image
        fname_im_straight = os.path.join(ifolder, subj, 't1', 't1_straight.nii.gz')
        # warping field from raw to preprocess space
        fname_warp_prepro = os.path.join(ifolder, subj, 't1', 'warp_curve2straight.nii.gz')
        # warping field from preprocess to template space
        fname_warp_template = os.path.join(wfolder, subj+'_t1.mnc_corr.'+last_it.zfill(3)+'_f.xfm')

        # loop across derivative files
        for deriv in ['labels_disk']:  ####, 'gmseg', 'seg']:
            # apply transfo from raw to preprocess space
            fname_in = os.path.join(ifolder, subj, 't1', 't1_'+deriv+'.nii.gz')
            fname_prepro = os.path.join(tmpfolder, subj+'_'+deriv+'_prepro.nii.gz')
            apply_transfo_sct(i=fname_in,
                                d=fname_im_straight,
                                w=fname_warp_prepro,
                                o=fname_prepro)

            # convert from nii to mnc
            fname_prepro_mnc = os.path.join(tmpfolder, subj+'_'+deriv+'_prepro.mnc')
            convert_nii_mnc(nii=fname_prepro,
                            mnc=fname_prepro_mnc)

            # apply tansfo from preprocess to template space
            fname_reg_mnc = os.path.join(tmpfolder, subj+'_'+deriv+'_reg.mnc')
            apply_transfo_minc(i=fname_prepro_mnc,
                                w=fname_warp_template,
                                o=fname_reg_mnc,
                                x='nn' if deriv == 'labels_disk' else False)

            # convert from mnc to nii
            fname_reg = os.path.join(tmpfolder, subj+'_'+deriv+'_reg.nii.gz')
            convert_mnc_nii(mnc=fname_reg_mnc,
                            nii=fname_reg)

            # set-orient-data and set-orient
            fname_reg_dIAR = os.path.join(tmpfolder, subj+'_'+deriv+'_reg_dIAR.nii.gz')
            fname_reg_out = os.path.join(ofolder, subj+'_'+deriv+'.nii.gz')
            set_orient(ref=fname_dest,
                        i=fname_reg,
                        i_tmp=fname_reg_dIAR,
                        o=fname_reg_out)

            # for labels: check that no one vanished
            if deriv == 'labels_disk':
                i_in, i_out = Image(fname_in), Image(fname_reg_out)
                print(' ')
                print(np.unique(i_in.data), np.unique(i_out.data))


if __name__ == '__main__':
    parser = get_parser()
    arguments = parser.parse_args()
    run_main(arguments)
