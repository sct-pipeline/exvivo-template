# exvivo-template
Repository for generating high resolution ex-vivo MRI template.

![pipeline](https://github.com/sct-pipeline/exvivo-template/raw/master/images/exvivo_pipeline.png)

## How to cite
Gros, C., Asiri, A., De Leener, B., Watson, C., Cowin, G., Ruitenberg, M., Kurniawan, N., Cohen-Adad, J., 2020. Ex vivo MRI template of the human cervical cord at 80μm isotropic resolution, in: Proceedingsof the 28th Annual Meeting of ISMRM. Presented at the ISMRM.

## Data

The ex-vivo template is available in the `data` folder of this repository. This folder contains:
- `template.nii.gz`: ex-vivo template.
- `mask_spinalcord.nii.gz`: binary spinalcord mask.
- `map_greymatter.nii.gz`: probabilistic grey matter map.
- `mask_spinalsegments.nii.gz`: mask of spinal segments, the value corresponds to the cervical segment, e.g. voxel value of 5 corresponds to C5 spinal level.
- `mask_motortracts.nii.gz`: mask of spinal motor tracts, the value corresponds to a specific motor tract, see [Labels sub-section](#labels) for details.

### Labels

Motor tracts value in `mask_motortracts.nii.gz`:
- 01 - Anterior corticospinal tract
- 02 - Central canal
- 03 - Epaxial motor column
- 04 - Trapezius and sternomastoid motor neurons of lamina 9
- 05 - Hypaxial motor column
- 06 - Lateral corticospinal tract
- 07 - Lamina 2 of the spinal gray (substantia gelatinosa)
- 08 - Cuneate fasciculus
- 09 - Gracile fasciculus
- 10 - Phrenic motor neurons of lamina 9
- 11 - Biceps motor neurons of lamina 9
- 12 - Supraspinatus and infraspinatus motor neurons of lamina 9
- 13 - Deltoid motor neurons of lamina 9
- 14 - Triceps motor neurons of lamina 9
- 15 - Forearm extensor motor neurons of lamina 9
- 16 - Forearm flexor motor neurons of lamina 9
- 17 - Latissimus dorsi motor neurons of lamina 9
- 18 - Pectoral muscle motor neurons of lamina 9

## Installation

To install, run:

```
git clone https://github.com/sct-pipeline/exvivo-template.git
cd ivadomed
pip install -e .
```

To use the tools to generate the template, you will need to install additional dependecies, as described [here](https://github.com/neuropoly/template#dependencies).

## Getting started

### Data labelling

#### Spinal level labelling

Manual labelling of the rostral and caudal extent of each nerve root was performed using `fsleyes`. Each spinal level was then identified by orthogonal projection of these labels onto the spinal cord centerline, using `sct_label_utils -create-seg`.

#### Grey matter and spinal cord segmentation

Spinal cord and grey matter tissues were automatically segmented using a deep learning model trained and applied using [IVADOMED](https://github.com/ivadomed/ivadomed). For each subject, the network was trained on 20 randomly picked and manually segmented slices, then inferred on the ~1,000 remaining slices. Results were reviewed and manually corrected when needed (~5%). The trained model is available [here](https://github.com/ivadomed/sc-gm_t2star_exvivo).

### Preprocessing

Preprocessing pipeline has been adapted from this [project](https://github.com/neuropoly/template). The code is available under `generate_template/`. To run it:
```
source sct_launcher
python generate_template/pipeline.py
```

### Tempalte generation

To generate the template with N (here N=13) subjects:
```
python -m scoop -n 13 -vvv generate_template/generate_template.py
```

## Contributors
Charley Gros, [Nyoman Kurniawan](https://cai.centre.uq.edu.au/profile/110/nyoman-kurniawan), Benjamin De Leener, Charles Watson and Julien Cohen-Adad.

