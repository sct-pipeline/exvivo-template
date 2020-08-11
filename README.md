# exvivo-template
Repository for generating high resolution ex-vivo MRI template.

![pipeline](https://github.com/sct-pipeline/exvivo-template/raw/master/images/exvivo_pipeline.png)

## Installation

### Dependencies

TO ADD: minc install

## Getting started

### Data labelling

#### Spinal level labelling

Manual labelling of the rostral and caudal extent of each nerve root was performed using `fsleyes`. Each spinal level was then identified by orthogonal projection of these labels onto the spinal cord centerline, using `sct_label_utils -create-seg`.

#### Grey matter and spinal cord segmentation

Spinal cord and grey matter tissues were automatically segmented using a deep learning model trained and applied using [IVADOMED](https://github.com/ivadomed/ivadomed). For each subject, the network was trained on 20 randomly picked and manually segmented slices, then inferred on the ~1,000 remaining slices. Results were reviewed and manually corrected when needed (~5%). The trained model is available [here](https://github.com/ivadomed/sc-gm_t2star_exvivo).


## Labels
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

## Contributors
Charley Gros, [Nyoman Kurniawan](https://cai.centre.uq.edu.au/profile/110/nyoman-kurniawan), Benjamin De Leener, Charles Watson and Julien Cohen-Adad.

