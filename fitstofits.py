
import numpy as np
from astropy.io import fits
from pathlib import Path
import glob
import os
import datetime

# def fits_to_fits(parent_folder):
parent_folder = '/data/solar_data/raw/2023/05/22/'
# to save the fts file with the specified naming covention
# in the respective folders
# to extract the raw images
# # define parent folder as
# parent_folder = '/data/solar_data/raw/YYYY/MM/DD/'
fits_name = '*.fits'
folder_name_s = 'HC/'
folder_path_s = os.path.join(parent_folder,folder_name_s,fits_name)
# folder_path_s = os.path.join(parent_folder,fits_name)
s_data =  glob.glob(folder_path_s)
# s_data =  glob.glob('/data/solar_data/raw/2022/12/20/HC/*.fits')

for filename in s_data:
    # print(filename)
    scidata = fits.open(filename)
    data = scidata[0].data
    header = scidata[0].header
    data = np.reshape(data,(data.shape[1],data.shape[2]) )
    date = header['DATE-OBS']
    date_only = date.split("T")[0]
    # print(date_only)
    fitsfile=f'S-{header["DATE-OBS"]}-HA.fits'
    # print(header["DATE-OBS"])
    fitsname = fitsfile
    params={'rootfolder': '/data/solar_data/processed/'}
    if Path(params["rootfolder"]).exists():
    # if params['rootfolder'] is None:
        dcf = fitsname.split('-')
        dcf_date = dcf[3].split('T')[0]
        date_obs = datetime.datetime.strptime(date_only, '%Y-%m-%d')
        #currentfolder=f'{params["rootfolder"]}{params["destfolder"]}{dcf[1]}/{dcf[1]}{dcf[2]}{dcf_date}/'
        currentfolder=f'{params["rootfolder"]}{dcf[1]}/{date_obs.strftime("%b").capitalize()}/{dcf[1]}{dcf[2]}{dcf_date}/'
        if not Path(currentfolder).exists():
            Path(currentfolder).mkdir(parents=True,exist_ok=True)
        # return f'{currentfolder}{fitsname}'
        fits.writeto(os.path.join(currentfolder, fitsfile),data,header,overwrite=True)
        
    else:
        raise Exception('Please check rootfolder path')
    
folder_name_s = 'LC/'
folder_path_s = os.path.join(parent_folder,folder_name_s,fits_name)
# folder_path_s = os.path.join(parent_folder,fits_name)
s_data =  glob.glob(folder_path_s)
# s_data =  glob.glob('/data/solar_data/raw/2022/12/20/HC/*.fits')

for filename in s_data:
    # print(filename)
    scidata = fits.open(filename)
    data = scidata[0].data
    header = scidata[0].header
    data = np.reshape(data,(data.shape[1],data.shape[2]) )
    date = header['DATE-OBS']
    date_only = date.split("T")[0]
    # print(date_only)
    fitsfile=f'S-{header["DATE-OBS"]}-HA.fits'
    # print(header["DATE-OBS"])
    fitsname = fitsfile
    params={'rootfolder': '/data/solar_data/processed/'}
    if Path(params["rootfolder"]).exists():
    # if params['rootfolder'] is None:
        dcf = fitsname.split('-')
        dcf_date = dcf[3].split('T')[0]
        date_obs = datetime.datetime.strptime(date_only, '%Y-%m-%d')
        #currentfolder=f'{params["rootfolder"]}{params["destfolder"]}{dcf[1]}/{dcf[1]}{dcf[2]}{dcf_date}/'
        currentfolder=f'{params["rootfolder"]}{dcf[1]}/{date_obs.strftime("%b").capitalize()}/{dcf[1]}{dcf[2]}{dcf_date}/'
        if not Path(currentfolder).exists():
            Path(currentfolder).mkdir(parents=True,exist_ok=True)
        # return f'{currentfolder}{fitsname}'
        fits.writeto(os.path.join(currentfolder, fitsfile),data,header,overwrite=True)
        
    else:
        raise Exception('Please check rootfolder path')


# to extract and save the dark fits files 
folder_name_d = 'DARK/'
folder_path_d = os.path.join(parent_folder,folder_name_d,fits_name)
d_data =  glob.glob(folder_path_d)
dark =  glob.glob(folder_path_d)
# dark = glob.glob('/data/solar_data/raw/2022/12/20/DARK/*.fits')
for filename in dark:

    d_data = fits.open(filename)
    data = d_data[0].data
    header = d_data[0].header
    data = np.reshape(data,(data.shape[1],data.shape[2]) )
    date = header['DATE-OBS']
    fitsfile=f'D-{header["DATE-OBS"]}-HA.fits'
    date_only = date.split("T")[0]
    fitsname = fitsfile
    params={'rootfolder': '/data/solar_data/processed/'}
    if Path(params["rootfolder"]).exists():
    # if params['rootfolder'] is None:
        dcf = fitsname.split('-')
        dcf_date = dcf[3].split('T')[0]
        date_obs = datetime.datetime.strptime(date_only, '%Y-%m-%d')
        #currentfolder=f'{params["rootfolder"]}{params["destfolder"]}{dcf[1]}/{dcf[1]}{dcf[2]}{dcf_date}/'
        currentfolder=f'{params["rootfolder"]}{dcf[1]}/{date_obs.strftime("%b").capitalize()}/{dcf[1]}{dcf[2]}{dcf_date}/'
        if not Path(currentfolder).exists():
            Path(currentfolder).mkdir(parents=True,exist_ok=True)
            # return f'{currentfolder}{fitsname}'
        fits.writeto(os.path.join(currentfolder, fitsfile),data,header,overwrite=True)
        
    else:
        raise Exception('Please check rootfolder path')
    
    # to extract and save the flat fits files 
folder_name_f = 'FLAT/'
folder_path_f = os.path.join(parent_folder,folder_name_f,fits_name)
f_data =  glob.glob(folder_path_f)
flat =  glob.glob(folder_path_f)
# flat = glob.glob('/data/solar_data/raw/2022/12/20/FLAT/*.fits')
for filename in flat:

    f_data = fits.open(filename)
    data = f_data[0].data
    header = f_data[0].header
    data = np.reshape(data,(data.shape[1],data.shape[2]) )
    date = header['DATE-OBS']
    fitsfile=f'F-{header["DATE-OBS"]}-HA.fits'
    date_only = date.split("T")[0]
    fitsname = fitsfile
    params={'rootfolder': '/data/solar_data/processed/'}
    if Path(params["rootfolder"]).exists():
    # if params['rootfolder'] is None:
        dcf = fitsname.split('-')
        dcf_date = dcf[3].split('T')[0]
        date_obs = datetime.datetime.strptime(date_only, '%Y-%m-%d')
        #currentfolder=f'{params["rootfolder"]}{params["destfolder"]}{dcf[1]}/{dcf[1]}{dcf[2]}{dcf_date}/'
        currentfolder=f'{params["rootfolder"]}{dcf[1]}/{date_obs.strftime("%b").capitalize()}/{dcf[1]}{dcf[2]}{dcf_date}/'
        if not Path(currentfolder).exists():
            Path(currentfolder).mkdir(parents=True,exist_ok=True)
            # return f'{currentfolder}{fitsname}'
        fits.writeto(os.path.join(currentfolder, fitsfile),data,header,overwrite=True)
    
    else:
        raise Exception('Please check rootfolder path')    
