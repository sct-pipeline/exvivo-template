"""
Run this script with the following command (replace N by the number of subjects):

python -m scoop -n N -vvv generate_template.py

"""

from scoop import futures, shared

import iplScoopGenerateModel as gm

if __name__ == '__main__':
    # setup data for parallel processing
    gm.generate_nonlinear_model_csv('subjects.csv',
                                    work_prefix='../../data_nvme_chgroc/template_midLvl',
                                    options={'symmetric': True,
                                             'protocol': [ {'iter': 6, 'level': 32},
                                                           {'iter': 4, 'level': 24},
                                                           {'iter': 4, 'level': 16},
                                                           {'iter': 2, 'level': 8},
                                                           {'iter': 6, 'level': 4},
                                                           {'iter': 3, 'level': 2},
                                                           {'iter': 3, 'level': 1}],
                                             'refine': True,
                                             'qc': True,
                                             'cleanup': True,
                                             'debug':  True
                                             }
                                    )
