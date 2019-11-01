#!/bin/bash
#
# This script resample the PAM50 files to an input resolution.
# Before resampling, a cropping around the region of interest is done
#	in order to speed up the resampling.
#
# Usage:
#   ./resample_PAM50.sh <resolution_mm> <ofolder>
# Note: No / at the end of ofolder
#
# Example:
#	./resample_PAM50.sh 0.08 PAM50_008

# input arguments
resolution="$1"
ofolder="$2"

# create output folder if does not exist
mkdir -p $ofolder

# PAM50 folder path
pam50path="$(echo $SCT_DIR/data/PAM50/template/)"

# create mask
sct_create_mask -i "$pam50path"/PAM50_centerline.nii.gz -p center -size 40 -f box -o "$ofolder"/mask.nii.gz

# loop across PAM50 files
for file in "$pam50path"*.nii.gz; do
    echo "$file"
    ofile="$ofolder"/"$(basename "$file")"
    if [ ! -f $ofile ];
    then
        # Crop around the spinal cord
        sct_crop_image -i $file -o $ofile -m "$ofolder"/mask.nii.gz
        # Crop from T3/T2
        sct_crop_image -i $ofile -o $ofile -zmin 648
        # Resample
        if [[ $file == *m.nii.gz ]] || [[ $(basename "$file") == PAM50_t* ]] ;
        then
            echo linear
            sct_resample -i $ofile -o $ofile -mm "$resolution"x"$resolution"x"$resolution"
        else
            echo nn
            sct_resample -i $ofile -o $ofile -mm "$resolution"x"$resolution"x"$resolution" -x nn
        fi
    fi
done
