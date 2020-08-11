from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

#Get README
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='exvivo-template',
    version=ivadomed.__version__,
    description='Feature conditioning for exvivo-template project.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sct-pipeline/exvivo-template',
    author='NeuroPoly and CAI-UQ',
    author_email='none@none.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True,
    install_requires=requirements
)
