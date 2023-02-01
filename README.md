# AniBOS_tools
*Authors: Fabien Roquet

Scripts used to process AniBOS data (anibos.com)

Since 2004, several hundred thousands profiles of temperature and salinity have been 
collected by instrumented animals. The use of elephant seals has been particularly 
effective to sample the Southern Ocean and the North Pacific. These hydrographic data 
have been assembled in a quality-controlled database, the MEOP-CTD database, that can 
be accessed through this website.
For more information, visit the website meop.net
For any questions, contact info@meop.net or fabien.roquet@gu.se

## DATA FORMATS

Data are provided in several formats. 
* _DATA_ncARGO:_ For a thourough scientific use of the data, or for oceanographic data centers, it is advised to use the 
marine mammal netCDF format (files in DATA_ncARGO) as it serves as the reference. This format can be 
easily read in Ocean Data View, using the Import/ARGO profiles/Float profiles menu, or using your 
favorite data processing software (e.g. Python, Matlab, IDL). 
* _DATA_ncARGO_interp:_ For ease of use, the DATA_ncARGO_interp provides the same data as in DATA_ncARGO, except it has
been interpolated on a regular vertical grid (1dbar spacing).

## Content

* lib_ncArgo/  
  Source to create and read netCDF files in the ncArgo format
* lib_matlab/  
  Source to execute matlab code within python. Use matlabengine pip package, that requires MATLAB R2022b or more recent.
* test/  
  Testing of modules
* Pipfile*  
  Environment files for python's pipenv
* setupy.py  
  Installation script for AniBOS_tools


### Clone this directory

```
git clone https://github.com/fabien-roquet/AniBOS_tools
cd AniBOS_tools
```

### Install the virtual environment

If you haven't already installed pipenv:
```
pip3 install --user pipenv
```

You need a working matlab installation. If you use MATLAB R2022b or more recent, you do not need to install anything further.
For older versions, check out https://se.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html

And then (in the base directory):
```
pipenv install
```

### Run the tests

