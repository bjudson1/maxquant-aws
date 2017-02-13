from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='maxquant-aws-script',
    version='0.1',
    description='',
    long_description=long_description,
    url='https://github.com/bjudson1/maxquant-aws-script',
    author='Brenden Judson',
    author_email='bjudson1@nd.edu',
    keywords='maxquant aws script',
    install_requires=['boto3'],
    entry_points={
        'console_scripts': [
            'maxquant-aws=maxquant-aws.script:main'
        ]
    }
)
