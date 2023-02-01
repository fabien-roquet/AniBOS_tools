#!/usr/bin/env python
from setuptools import setup, find_packages

DISTNAME = "AniBOS_tools"
VERSION = "0.0.1"
LICENSE = "MIT"
AUTHOR = "Fabien Roquet"
AUTHOR_EMAIL = "fabien.roquet@gu.se"
DESCRIPTION = "Tools for AniBOS data (anibos.com)."
LONG_DESCRIPTION = "Library used to read and create AniBOS data file. Include tools to execute matlab code in python."

setup(
    name=DISTNAME,
    version=VERSION,
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['dataclasses','netCDF4','numpy','pandas','scipy','xarray','gsw','matplotlib','cmocean'], #'matlabengine','cartopy'
)
