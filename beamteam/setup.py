'''
Created on 08 JUN 2013

Maurizio Nagni (at) stfc.ac.uk
'''
# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
import re
import os

base_name='beamteam'
v_file = open(os.path.join(os.path.dirname(__file__), 
                       base_name, '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'",
                     re.S).match(v_file.read()).group(1)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=base_name,
    version=VERSION,
    author=u'Maurizio Nagni',
    author_email='Maurizio.Nagni@stfc.ac.uk',
    package_dir = {base_name:base_name},   
    packages=find_packages(), # include all packages under this directory  
    include_package_data = True,        
    url='git://github.com/kusamau/beamteam.git',  
    license='BSD licence, see LICENCE',
    description='CEDA web site',
    long_description=open('README.txt').read(),
    zip_safe=False,
    # Adds dependencies    
    install_requires = ['django'],
)