#!/bin/bash
#
# XX
#
# Usage:
#   ./resample_PAM50.sh <resolution_mm> <ofolder>
# Note: No "/" at the end of ofolder
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

# loop across PAM50 files
for file in "$pam50path"*.nii.gz; do
    echo "$file"
    ofile="$ofolder"/"$(basename "$file")"
    if [ ! -f $ofile ]; then
        # Crop from T3/T2
        sct_crop_image -i $file -o $ofile -zmin 648
        # Resample
        sct_resample -i $ofile -o $ofile -mm "$resolution"x"$resolution"x"$resolution"
    fi
done