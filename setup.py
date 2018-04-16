from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='im-gafp',
    version='1.0.0',
    description='Residential energy use disaggregation using the Ampds dataset',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/enmyj/gafp',
    author='Ian Myjer',
    classifiers=[ 
        'Development Status :: 3 - Alpha'
        , 'Intended Audience :: Students'
        , 'Programming Language :: Python :: 3.5'
    ],
    packages=find_packages(),
    install_requires=[
        'pandas'
        , 'numpy'
        , 'sklearn'
        , 'matplotlib'
        , 'seaborn'
        , 'collections'], 
    package_data={
        'elec': ['electric_data_with_weather.zip'],
    },
    project_urls={
        'Data Source': 'http://ampds.org/'
        , 'Course': 'https://generalassemb.ly/education/data-science'
    }
)