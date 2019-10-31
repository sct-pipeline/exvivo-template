#!/bin/bash
#
# This script crops the resampled PAM50 around the SC,
#	in the axial plane.
#
# Usage:
#   ./crop_PAM50.sh <axial_voxel_size> <ifolder> <ofolder>
# Note: No / at the end of folders
#
# Example:
#       ./crop_PAM50.sh 250 PAM50_008 PAM50_008_crop

# input arguments
size="$1"
ifolder="$2"
ofolder="$3"

# create output folder if does not exist
mkdir -p $ofolder

# create mask
sct_create_mask -i "$ifolder"/PAM50_centerline.nii.gz -p center -size $size -f box -o "$ofolder"/mask.nii.gz

# loop across PAM50 files
for file in "$ifolder"/*.nii.gz; do
    echo "$file"
    ofile="$ofolder"/"$(basename "$file")"
    if [ ! -f $ofile ]; then
        # Crop
        sct_crop_image -i $file -o $ofile -m "$ofolder"/mask.nii.gz
    fi
done

