from AniBOS_tools.create_ncArgo import create_ncArgo
import xarray as xr


Nprof=100
Nlevels=20
create_ncArgo('test.nc',Nprof=Nprof,Nlevels=Nlevels)

with xr.open_dataset('test.nc') as ds:
    print(ds)

