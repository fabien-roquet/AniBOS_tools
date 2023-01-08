# function to create a netCDF file for Argo data

import netCDF4 as nc
from netCDF4 import num2date
import numpy as np
import datetime


def open_ncArgo(fname, mode='r'):
    ncid = nc.Dataset(fname, mode)
    return ncid


def close_ncArgo(ncid):
    ncid.close()


def init_ncArgo(ncid, Nprof=5, Nlevels=20, isfluo=0, isoxy=0, islight=0, issalcor=0):

    # Define dimensions
    DATE_TIME = ncid.createDimension('DATE_TIME', 14)
    STRING256 = ncid.createDimension('STRING256', 256)
    STRING64 = ncid.createDimension('STRING64', 64)
    STRING32 = ncid.createDimension('STRING32', 32)
    STRING16 = ncid.createDimension('STRING16', 16)
    STRING8 = ncid.createDimension('STRING8', 8)
    STRING4 = ncid.createDimension('STRING4', 4)
    STRING2 = ncid.createDimension('STRING2', 2)
    N_PROF = ncid.createDimension('N_PROF', Nprof)
    N_PARAM = ncid.createDimension('N_PARAM', 3 + isfluo + isoxy + islight)
    N_LEVELS = ncid.createDimension('N_LEVELS', Nlevels)
    N_CALIB = ncid.createDimension('N_CALIB', 1)
    N_HISTORY = ncid.createDimension('N_HISTORY', None)

    # Define variables and set attributes
    varid = ncid.createVariable('DATA_TYPE', 'c', ('STRING4',))
    varid.setncattr('comment', 'Data type')

    varid = ncid.createVariable('FORMAT_VERSION', 'c', ('STRING4',))
    varid.setncattr('comment', 'File format version')

    varid = ncid.createVariable('HANDBOOK_VERSION', 'c', ('STRING4',))
    varid.setncattr('comment', 'Data handbook version')

    varid = ncid.createVariable('REFERENCE_DATE_TIME', 'c', ('DATE_TIME',))
    varid.setncattr('comment', 'Date of reference for Julian days')
    varid.setncattr('conventions', 'YYYYMMDDHHMISS')

    varid = ncid.createVariable('DATE_CREATION', 'c', ('DATE_TIME',))
    varid.setncattr('comment', 'Date of file creation')
    varid.setncattr('conventions', 'YYYYMMDDHHMISS')

    varid = ncid.createVariable('DATE_UPDATE', 'c', ('DATE_TIME',))
    varid.setncattr('long_name', 'Date of update of this file')
    varid.setncattr('conventions', 'YYYYMMDDHHMISS')

    varid = ncid.createVariable('PLATFORM_NUMBER', 'c', ('STRING8', 'N_PROF'))
    varid.setncattr('long_name', 'Float unique identifier')
    varid.setncattr('conventions', 'WMO float identifier : A9IIIII')

    varid = ncid.createVariable('PROJECT_NAME', 'c', ('STRING64', 'N_PROF'))
    varid.setncattr('comment', 'Name of the project')

    varid = ncid.createVariable('PI_NAME', 'c', ('STRING64', 'N_PROF'))
    varid.setncattr('comment', 'Name of the principal investigator')

    varid = ncid.createVariable(
        'STATION_PARAMETERS', 'c', ('STRING16', 'N_PARAM', 'N_PROF'))
    varid.setncattr(
        'long_name', 'List of available parameters for the station')
    varid.setncattr('conventions', 'Argo reference table 3')

    varid = ncid.createVariable(
        'CYCLE_NUMBER', 'i4', ('N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'Float cycle number')
    varid.setncattr('units', '1')
    varid.setncattr(
        'conventions', '0..N, 0 : launch cycle (if exists), 1 : first complete cycle')

    varid = ncid.createVariable('DIRECTION', 'c', ('N_PROF'))
    varid.setncattr('long_name', 'Direction of the station profiles')
    varid.setncattr(
        'conventions', 'A: ascending profiles, D: descending profiles')

    varid = ncid.createVariable('DATA_CENTRE', 'c', ('STRING2', 'N_PROF'))
    varid.setncattr(
        'long_name', 'Data centre in charge of float data processing')
    varid.setncattr('conventions', 'Argo reference table 4')

    varid = ncid.createVariable('DC_REFERENCE', 'c', ('STRING32', 'N_PROF'))
    varid.setncattr('long_name', 'Station unique identifier in data centre')
    varid.setncattr('conventions', 'Data centre convention')

    varid = ncid.createVariable(
        'DATA_STATE_INDICATOR', 'c', ('STRING4', 'N_PROF'))
    varid.setncattr(
        'long_name', 'Degree of processing the data have passed through')
    varid.setncattr('conventions', 'Argo reference table 6')

    varid = ncid.createVariable('DATA_MODE', 'c', ('N_PROF'))
    varid.setncattr('long_name', 'Delayed mode or real time data')
    varid.setncattr(
        'conventions', 'R : real time; D : delayed mode; A : real time with adjustment')

    varid = ncid.createVariable('INST_REFERENCE', 'c', ('STRING64', 'N_PROF'))
    varid.setncattr('long_name', 'Instrument type')
    varid.setncattr('conventions', 'Brand, type, serial number')

    varid = ncid.createVariable('WMO_INST_TYPE', 'c', ('STRING4', 'N_PROF'))
    varid.setncattr('long_name', 'Coded instrument type')
    varid.setncattr('conventions', 'Argo reference table 8')

    varid = ncid.createVariable('JULD', 'f8', ('N_PROF'), fill_value=99999)
    varid.setncattr(
        'long_name', 'Julian day (UTC) of the station relative to REFERENCE_DATE_TIME')
    varid.units = 'days since 1950-01-01 00:00:00 UTC'
    varid.calendar = 'julian'
    varid.setncattr(
        'conventions', 'Relative julian days with decimal part (as parts of day)')

    varid = ncid.createVariable('JULD_QC', 'c', ('N_PROF'))
    varid.setncattr('long_name', 'Quality on Date and Time')
    varid.setncattr('conventions', 'Argo reference table 2')

    varid = ncid.createVariable(
        'JULD_LOCATION', 'f8', ('N_PROF'), fill_value=99999)
    varid.setncattr(
        'long_name', 'Julian day (UTC) of the location relative to REFERENCE_DATE_TIME')
    varid.units = 'days since 1950-01-01 00:00:00 UTC'
    varid.calendar = 'julian'
    varid.setncattr(
        'conventions', 'Relative julian days with decimal part (as parts of day)')

    varid = ncid.createVariable('LATITUDE', 'f8', ('N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'Latitude of the station, best estimate')
    varid.setncattr('units', 'degree_north')
    varid.setncattr('valid_min', -90)
    varid.setncattr('valid_max', 90)

    varid = ncid.createVariable(
        'LONGITUDE', 'f8', ('N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'Longitude of the station, best estimate')
    varid.setncattr('units', 'degree_east')
    varid.setncattr('valid_min', -180)
    varid.setncattr('valid_max', 180)

    varid = ncid.createVariable('POSITION_QC', 'c', ('N_PROF'))
    varid.setncattr(
        'long_name', 'Quality on position (latitude and longitude)')
    varid.setncattr('conventions', 'Argo reference table 2')

    varid = ncid.createVariable(
        'POSITIONING_SYSTEM', 'c', ('STRING8', 'N_PROF'))
    varid.setncattr('long_name', 'Positioning system')

    varid = ncid.createVariable('PROFILE_PRES_QC', 'c', ('N_PROF'))
    varid.setncattr('long_name', 'Global quality flag of PRES profile')
    varid.setncattr('conventions', 'Argo reference table 2a')

    varid = ncid.createVariable('PROFILE_PSAL_QC', 'c', ('N_PROF'))
    varid.setncattr('long_name', 'Global quality flag of PSAL profile')
    varid.setncattr('conventions', 'Argo reference table 2a')

    varid = ncid.createVariable('PROFILE_TEMP_QC', 'c', ('N_PROF'))
    varid.setncattr('long_name', 'Global quality flag of TEMP profile')
    varid.setncattr('conventions', 'Argo reference table 2a')

    varid = ncid.createVariable(
        'PRES', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'SEA PRESSURE')
    varid.setncattr('units', 'decibar')
    varid.setncattr('valid_min', 0)
    varid.setncattr('valid_max', 12000)
    varid.setncattr('comment', 'In situ measurement, sea surface = 0')

    varid = ncid.createVariable('PRES_QC', 'c', ('N_LEVELS', 'N_PROF'))
    varid.setncattr('long_name', 'quality flag')
    varid.setncattr('conventions', 'Argo reference table 2')

    varid = ncid.createVariable(
        'PRES_ADJUSTED', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'SEA PRESSURE')
    varid.setncattr('units', 'decibar')
    varid.setncattr('valid_min', 0)
    varid.setncattr('valid_max', 12000)
    varid.setncattr('comment', 'In situ measurement, sea surface = 0')

    varid = ncid.createVariable(
        'PRES_ADJUSTED_QC', 'c', ('N_LEVELS', 'N_PROF'))
    varid.setncattr('long_name', 'quality flag')
    varid.setncattr('conventions', 'Argo reference table 2')

    varid = ncid.createVariable(
        'PRES_ADJUSTED_ERROR', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'SEA PRESSURE')
    varid.setncattr('units', 'decibar')
    varid.setncattr(
        'comment', 'Contains the error on the adjusted values as determined by the delayed mode QC process.')

    varid = ncid.createVariable(
        'TEMP', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'SEA TEMPERATURE IN SITU ITS-90 SCALE')
    varid.setncattr('units', 'degree_Celsius')
    varid.setncattr('valid_min', -2)
    varid.setncattr('valid_max', 40)
    varid.setncattr('comment', 'In situ measurement')

    varid = ncid.createVariable('TEMP_QC', 'c', ('N_LEVELS', 'N_PROF'))
    varid.setncattr('long_name', 'quality flag')
    varid.setncattr('conventions', 'Argo reference table 2')

    varid = ncid.createVariable(
        'TEMP_ADJUSTED', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'SEA TEMPERATURE IN SITU ITS-90 SCALE')
    varid.setncattr('units', 'degree_Celsius')
    varid.setncattr('valid_min', -2)
    varid.setncattr('valid_max', 40)
    varid.setncattr('comment', 'In situ measurement')

    varid = ncid.createVariable(
        'TEMP_ADJUSTED_QC', 'c', ('N_LEVELS', 'N_PROF'))
    varid.setncattr('long_name', 'quality flag')
    varid.setncattr('conventions', 'Argo reference table 2')

    varid = ncid.createVariable(
        'TEMP_ADJUSTED_ERROR', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'SEA TEMPERATURE ERROR IN SITU ITS-90 SCALE')
    varid.setncattr('units', 'degree_Celsius')
    varid.setncattr(
        'comment', 'Contains the error on the adjusted values as determined by the delayed mode QC process.')

    varid = ncid.createVariable(
        'PSAL', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'PRACTICAL SALINITY')
    varid.setncattr('units', '1e-3')
    varid.setncattr('valid_min', 0)
    varid.setncattr('valid_max', 42)
    varid.setncattr('comment', 'In situ measurement')

    varid = ncid.createVariable('PSAL_QC', 'c', ('N_LEVELS', 'N_PROF'))
    varid.setncattr('long_name', 'quality flag')
    varid.setncattr('conventions', 'Argo reference table 2')

    varid = ncid.createVariable(
        'PSAL_ADJUSTED', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'ADJUSTED PRACTICAL SALINITY')
    varid.setncattr('units', '1e-3')
    varid.setncattr('valid_min', 0)
    varid.setncattr('valid_max', 42)
    varid.setncattr('comment', 'In situ measurement')

    varid = ncid.createVariable(
        'PSAL_ADJUSTED_QC', 'c', ('N_LEVELS', 'N_PROF'))
    varid.setncattr('long_name', 'quality flag')
    varid.setncattr('conventions', 'Argo reference table 2')

    varid = ncid.createVariable(
        'PSAL_ADJUSTED_ERROR', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
    varid.setncattr('long_name', 'PRACTICAL SALINITY ERROR')
    varid.setncattr('units', '1e-3')
    varid.setncattr(
        'comment', 'Contains the error on the adjusted values as determined by the delayed mode QC process.')

    if issalcor:
        varid = ncid.createVariable(
            ncid, 'PSAL_CORRECTED', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
        varid.setncattr(
            'long_name', 'CORRECTED PRACTICAL SALINITY WITH TIMELAPS')
        varid.setncattr('units', '1e-3')
        varid.setncattr('valid_min', 0)
        varid.setncattr('valid_max', 42)
        varid.setncattr('comment', 'In situ measurement')

    if isfluo:

        varid = ncid.createVariable(
            ncid, 'PROFILE_CHLA_QC', 'c', ('N_PROF'))
        varid.setncattr('long_name', 'Global quality flag of CHLA profile')
        varid.setncattr('conventions', 'Argo reference table 2a')

        varid = ncid.createVariable(
            ncid, 'CHLA', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
        varid.setncattr('long_name', 'CHLOROPHYLL-A')
        varid.setncattr('units', 'mg/m3')
        varid.setncattr('valid_min', 0)
        varid.setncattr('valid_max', 10)
        varid.setncattr('comment', 'In situ measurement')

        varid = ncid.createVariable(
            ncid, 'CHLA_QC', 'c', ('N_LEVELS', 'N_PROF'))
        varid.setncattr('long_name', 'quality flag')
        varid.setncattr('conventions', 'Argo reference table 2')

        varid = ncid.createVariable(
            ncid, 'CHLA_ADJUSTED', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
        varid.setncattr('long_name', 'CHLOROPHYLL-A')
        varid.setncattr('units', 'mg/m3')
        varid.setncattr('valid_min', 0)
        varid.setncattr('valid_max', 10)
        varid.setncattr('comment', 'In situ measurement')

        varid = ncid.createVariable(
            ncid, 'CHLA_ADJUSTED_QC', 'c', ('N_LEVELS', 'N_PROF'))
        varid.setncattr('long_name', 'quality flag')
        varid.setncattr('conventions', 'Argo reference table 2')

        varid = ncid.createVariable(
            ncid, 'CHLA_ADJUSTED_ERROR', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
        varid.setncattr('long_name', 'CHLOROPHYLL-A')
        varid.setncattr('units', 'mg/m3')
        varid.setncattr(
            'comment', 'Contains the error on the adjusted values as determined by the delayed mode QC process.')

    if isoxy:

        varid = ncid.createVariable(
            ncid, 'PROFILE_DOXY_QC', 'c', ('N_PROF'))
        varid.setncattr('long_name', 'Global quality flag of DOXY profile')
        varid.setncattr('conventions', 'Argo reference table 2a')

        varid = ncid.createVariable(
            ncid, 'DOXY', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
        varid.setncattr('long_name', 'DISSOLVED OXYGEN')
        varid.setncattr('units', 'micromole/kg')

        varid.setncattr('valid_min', 0)
        varid.setncattr('valid_max', 600)
        varid.setncattr('comment', 'In situ measurement')

        varid = ncid.createVariable(
            ncid, 'DOXY_QC', 'c', ('N_LEVELS', 'N_PROF'))
        varid.setncattr('long_name', 'quality flag')
        varid.setncattr('conventions', 'Argo reference table 2')

        varid = ncid.createVariable(
            ncid, 'DOXY_ADJUSTED', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
        varid.setncattr('long_name', 'DISSOLVED OXYGEN')
        varid.setncattr('units', 'micromole/kg')

        varid.setncattr('valid_min', 0)
        varid.setncattr('valid_max', 600)
        varid.setncattr('comment', 'In situ measurement')

        varid = ncid.createVariable(
            ncid, 'DOXY_ADJUSTED_QC', 'c', ('N_LEVELS', 'N_PROF'))
        varid.setncattr('long_name', 'quality flag')
        varid.setncattr('conventions', 'Argo reference table 2')

        varid = ncid.createVariable(
            ncid, 'DOXY_ADJUSTED_ERROR', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
        varid.setncattr('long_name', 'DISSOLVED OXYGEN')
        varid.setncattr('units', 'micromole/kg')
        varid.setncattr(
            'comment', 'Contains the error on the adjusted values as determined by the delayed mode QC process.')

    if islight:

        varid = ncid.createVariable(
            ncid, 'PROFILE_LIGHT_QC', 'c', ('N_PROF'))
        varid.setncattr('long_name', 'Global quality flag of LIGHT profile')
        varid.setncattr('conventions', 'Argo reference table 2a')

        varid = ncid.createVariable(
            ncid, 'LIGHT', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
        varid.setncattr('long_name', 'ln(PPFD)')
        varid.setncattr('units', 'ln(�mol/m�/s)')
        varid.setncattr('valid_min', 0)
        varid.setncattr('valid_max', 600)
        varid.setncattr('comment', 'In situ measurement')

        varid = ncid.createVariable(
            ncid, 'LIGHT_QC', 'c', ('N_LEVELS', 'N_PROF'))
        varid.setncattr('long_name', 'quality flag')
        varid.setncattr('conventions', 'Argo reference table 2')

        varid = ncid.createVariable(
            ncid, 'LIGHT_ADJUSTED', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
        varid.setncattr('long_name', 'ln(PPFD)')
        varid.setncattr('units', 'ln(�mol/m�/s)')

        varid.setncattr('valid_min', 0)
        varid.setncattr('valid_max', 600)
        varid.setncattr('comment', 'In situ measurement')

        varid = ncid.createVariable(
            ncid, 'LIGHT_ADJUSTED_QC', 'c', ('N_LEVELS', 'N_PROF'))
        varid.setncattr('long_name', 'quality flag')
        varid.setncattr('conventions', 'Argo reference table 2')

        varid = ncid.createVariable(
            ncid, 'LIGHT_ADJUSTED_ERROR', 'f4', ('N_LEVELS', 'N_PROF'), fill_value=99999)
        varid.setncattr('long_name', 'ln(PPFD)')
        varid.setncattr('units', 'ln(�mol/m�/s)')
        varid.setncattr(
            'comment', 'Contains the error on the adjusted values as determined by the delayed mode QC process.')

    varid = ncid.createVariable(
        'PARAMETER', 'c', ('STRING16', 'N_PARAM', 'N_CALIB', 'N_PROF'))
    varid.setncattr(
        'long_name', 'List of parameters with calibration information')
    varid.setncattr('conventions', 'Argo reference table 3')

    varid = ncid.createVariable('SCIENTIFIC_CALIB_EQUATION',
                                'c', ('STRING256', 'N_PARAM', 'N_CALIB', 'N_PROF'))
    varid.setncattr('long_name', 'Calibration equation for this parameter')

    varid = ncid.createVariable('SCIENTIFIC_CALIB_COEFFICIENT',
                                'c', ('STRING256', 'N_PARAM', 'N_CALIB', 'N_PROF'))
    varid.setncattr('long_name', 'Calibration coefficients for this equation')

    return ncid


def write_ncArgo(ncid, Nprof=5, Nlevels=20, isfluo=0, isoxy=0, islight=0, issalcor=0):

    # Write metadata to the file
    ncid.DATA_TYPE = 'Argo profile    '
    ncid.FORMAT_VERSION = '3.0 '
    ncid.HANDBOOK_VERSION = '3.0 '
    ncid.REFERENCE_DATE_TIME = '19500101000000'
    ncid.DATE_CREATION = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    ncid.DATE_UPDATE = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    ncid.PLATFORM_NUMBER = [' ' * 8] * Nprof
    ncid.PROJECT_NAME = [' ' * 64] * Nprof
    ncid.PI_NAME = [' ' * 64] * Nprof

    # Update the STATION_PARAMETERS variable
    for kk in range(Nprof):
        ncid.variables['STATION_PARAMETERS'][:, 0, kk] = '%-16s' % 'PRES'
        ncid.variables['STATION_PARAMETERS'][:, 1, kk] = '%-16s' % 'TEMP'
        ncid.variables['STATION_PARAMETERS'][:, 2, kk] = '%-16s' % 'PSAL'
        if isfluo:
            ncid.variables['STATION_PARAMETERS'][:, 3, kk] = '%-16s' % 'CHLA'
        if isoxy:
            ncid.variables['STATION_PARAMETERS'][:, 3 + isfluo, kk] = '%-16s' % 'DOXY'
        if islight:
            ncid.variables['STATION_PARAMETERS'][:, 3 + isfluo + isoxy, kk] = '%-16s' % 'LIGHT'

    # Write the updated STATION_PARAMETERS variable to the file

    ncid.variables['CYCLE_NUMBER'][:] = np.full((Nprof, 1), np.nan)
    ncid.variables['DIRECTION'][:] = ['A'] * Nprof
    ncid.variables['DATA_MODE'][:] = ['D'] * Nprof
    for kk in range(Nprof):
        ncid.variables['DATA_CENTRE'][:,kk] = 'IF'
        ncid.variables['DC_REFERENCE'][:,kk] = ' ' * 32
        ncid.variables['WMO_INST_TYPE'][:,kk] = '995 '
    ncid.variables['JULD'][:] = np.full((Nprof, 1), 0)
    ncid.variables['JULD_LOCATION'][:] = np.full((Nprof, 1), 0)
    ncid.variables['JULD_QC'][:] = ['1'] * Nprof
    ncid.variables['LATITUDE'][:] = np.full((Nprof, 1), np.nan)
    ncid.variables['LONGITUDE'][:] = np.full((Nprof, 1), np.nan)
    ncid.variables['POSITION_QC'][:] = ['1'] * Nprof
    for kk in range(Nprof):
        ncid.variables['POSITIONING_SYSTEM'][:,kk] = 'ARGOS   '
    ncid.variables['PROFILE_PRES_QC'][:] = ['A'] * Nprof
    ncid.variables['PROFILE_PSAL_QC'][:] = ['A'] * Nprof
    ncid.variables['PROFILE_TEMP_QC'][:] = ['A'] * Nprof
    if isfluo:
        ncid.variables['PROFILE_CHLA_QC'][:] = ['A'] * Nprof
    if isoxy:
        ncid.variables['PROFILE_DOXY_QC'][:] = ['A'] * Nprof
    if islight:
        ncid.variables['PROFILE_LIGHT_QC'][:] = ['A'] * Nprof

    # Write the PARAMETER, SCIENTIFIC_CALIB_EQUATION, and SCIENTIFIC_CALIB_COEFFICIENT variables
    for kk in range(Nprof):
        ncid.variables['PARAMETER'][:, 0, 0, kk] = '%-16s' % 'PRES'
        ncid.variables['PARAMETER'][:, 1, 0, kk] = '%-16s' % 'TEMP'
        ncid.variables['PARAMETER'][:, 2, 0, kk] = '%-16s' % 'PSAL'
        ncid.variables['SCIENTIFIC_CALIB_EQUATION'][:, 0, 0,
                                kk] = '%-256s' % 'Pc = P - ( p1 [dbar/km] * P  * 1e-3 + p2 [dbar] )'
        ncid.variables['SCIENTIFIC_CALIB_EQUATION'][:, 1, 0,
                                kk] = '%-256s' % 'Tc = T - ( t1 [degC/km] * Pc * 1e-3 + t2 [degC] )'
        ncid.variables['SCIENTIFIC_CALIB_EQUATION'][:, 2, 0,
                                kk] = '%-256s' % 'Sc = S - ( s1 [ psu/km] * Pc * 1e-3 + s2 [ psu] )'
        ncid.variables['SCIENTIFIC_CALIB_COEFFICIENT'][:, 0, 0, kk] = '%-256s' % ' '
        ncid.variables['SCIENTIFIC_CALIB_COEFFICIENT'][:, 1, 0, kk] = '%-256s' % ' '
        ncid.variables['SCIENTIFIC_CALIB_COEFFICIENT'][:, 2, 0, kk] = '%-256s' % ' '
        if isfluo:
            ncid.variables['PARAMETER'][:, 3, 0, kk] = '%-16s' % 'CHLA'
            ncid.variables['SCIENTIFIC_CALIB_COEFFICIENT'][:, 3, 0, kk] = '%-256s' % 'Fc = f1 * F + f2'
            ncid.variables['SCIENTIFIC_CALIB_COEFFICIENT'][:, 3, 0, kk] = '%-256s' % ' '
        if isoxy:
            ncid.variables['PARAMETER'][:, 3 + isfluo, 0, kk] = '%-16s' % 'DOXY'
            ncid.variables['SCIENTIFIC_CALIB_COEFFICIENT'][:, 3 + isfluo, 0, kk] = '%-256s' % ' '
            ncid.variables['SCIENTIFIC_CALIB_COEFFICIENT'][:, 3 + isfluo, 0, kk] = '%-256s' % ' '
        if islight:
            ncid.variables['PARAMETER'][:, 3 + isfluo + isoxy, 0, kk] = '%-16s' % 'LIGHT'
            ncid.variables['SCIENTIFIC_CALIB_COEFFICIENT'][:, 3 +
                                    isfluo + isoxy, 0, kk] = '%-256s' % ' '
            ncid.variables['SCIENTIFIC_CALIB_COEFFICIENT'][:, 3 +
                                        isfluo + isoxy, 0, kk] = '%-256s' % ' '


    return ncid


def main():

    # delete test.nc if it exists
    import os
    if os.path.exists('test.nc'):
        os.remove('test.nc')

    # Create a netCDF file using the function init_ncArgo
    Nprof=100
    Nlevels=20
    ncid = open_ncArgo('test.nc', 'w')
    ncid = init_ncArgo(ncid, Nprof=Nprof, Nlevels=Nlevels)
    ncid = write_ncArgo(ncid, Nprof=Nprof, Nlevels=Nlevels)
    close_ncArgo(ncid)

    # Open test.nc using Dataset
    ncid = nc.Dataset('test.nc', 'r+')
    print(ncid)
    ncid.close()

    # Open test.nc using read_ncArgo
    import read_ncArgo as meop
    ds = meop.open_dataset('test.nc')
    print(ds)


if __name__ == '__main__':
    main()
