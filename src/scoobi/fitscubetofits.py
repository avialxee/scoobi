# # program to convert fits data cube to fits and save that dta cube to the 
# # final one

import numpy as np
from astropy.io import fits
from pathlib import Path
import matplotlib.pyplot as plt
import glob
import os
import datetime

# def fits_to_fits(parent_folder):
parent_folder = '/data/solar_data/raw/2023/06/01/'
sub_folder = 'DARK/'
# fits_name = '2022 June 02 09_44_28 10.fits'
fits_pattern = '*.fits'
# folder_path_s = os.path.join(parent_folder,fits_name)
folder_path_s = os.path.join(parent_folder,sub_folder,fits_pattern)
fits_files =  glob.glob(folder_path_s)

# open the fits data cube
# loop through each fits files
for fits_file in fits_files:
    # open the fita data cube
    data_cube = fits.open(fits_file)
    header =  data_cube[0].header
    date = header['DATE-OBS']
# Loop through each slice of the data cube and save it as a separate fits file
    for i, data_slice in enumerate(data_cube[0].data, start=1):
        # Get the header for this slice from the data cube
        header = data_cube[0].header
        # Convert the header DATE-OBS value to datetime object
        date_obs_str = header['DATE-OBS']
        date_obs_time = datetime.datetime.strptime(date_obs_str, '%Y-%m-%dT%H:%M:%S')

        # Add cadence to datetime object
        # cadence = int(header['PI CAMERA SHUTTERTIMING DELAYRESOLUTION'])/1000
        cadence = 1 #cadence is kept one sec for Dark and Flat
        date_obs_time_cadence = date_obs_time + datetime.timedelta(seconds=cadence)

        # Convert back to string format
        date_obs_str_cadence = date_obs_time_cadence.strftime('%Y-%m-%dT%H:%M:%S')

        # Update header with new DATE-OBS value
        header['DATE-OBS'] = date_obs_str_cadence
        date_only = date.split("T")[0]
        fitsfile=f'D-{header["DATE-OBS"]}-HA.fits'
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
            fits.writeto(os.path.join(currentfolder, fitsfile),data_slice,header,overwrite=True)

# # def fits_to_fits(parent_folder):
sub_folder = 'FLAT/'
# fits_name = '2022 June 02 09_44_28 10.fits'
fits_pattern = '*.fits'
# folder_path_s = os.path.join(parent_folder,fits_name)
folder_path_s = os.path.join(parent_folder,sub_folder,fits_pattern)
fits_files =  glob.glob(folder_path_s)

# open the fits data cube
# loop through each fits files
for fits_file in fits_files:
    # open the fita data cube
    data_cube = fits.open(fits_file)
    header =  data_cube[0].header
    date = header['DATE-OBS']
# Loop through each slice of the data cube and save it as a separate fits file
    for i, data_slice in enumerate(data_cube[0].data, start=1):
        # Get the header for this slice from the data cube
        header = data_cube[0].header
        # Convert the header DATE-OBS value to datetime object
        date_obs_str = header['DATE-OBS']
        date_obs_time = datetime.datetime.strptime(date_obs_str, '%Y-%m-%dT%H:%M:%S')

        # Add cadence to datetime object
        # cadence = int(header['PI CAMERA SHUTTERTIMING DELAYRESOLUTION'])/1000
        cadence = 1 #cadence is kept one sec for Dark and Flat
        date_obs_time_cadence = date_obs_time + datetime.timedelta(seconds=cadence)

        # Convert back to string format
        date_obs_str_cadence = date_obs_time_cadence.strftime('%Y-%m-%dT%H:%M:%S')

        # Update header with new DATE-OBS value
        header['DATE-OBS'] = date_obs_str_cadence
        date_only = date.split("T")[0]
        fitsfile=f'F-{header["DATE-OBS"]}-HA.fits'
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
            fits.writeto(os.path.join(currentfolder, fitsfile),data_slice,header,overwrite=True)

# def fits_to_fits(parent_folder):
sub_folder = 'HC/'
# fits_name = '2022 June 02 09_44_28 10.fits'
fits_pattern = '*.fits'
# folder_path_s = os.path.join(parent_folder,fits_name)
folder_path_s = os.path.join(parent_folder,sub_folder,fits_pattern)
fits_files =  glob.glob(folder_path_s)

# open the fits data cube
# loop through each fits files
for fits_file in fits_files:
    # open the fita data cube
    data_cube = fits.open(fits_file)
    header =  data_cube[0].header
    date = header['DATE-OBS']
    date_only = date.split("T")[0]
    # Loop through each slice of the data cube and save it as a separate fits file
    for i, data_slice in enumerate(data_cube[0].data, start=1):
        # Get the header for this slice from the data cube
        header = data_cube[0].header
    #   Convert the header DATE-OBS value to datetime object
        date_obs_str = header['DATE-OBS']
        date_obs_time = datetime.datetime.strptime(date_obs_str, '%Y-%m-%dT%H:%M:%S')

    #   Add cadence to datetime object
    #   cadence = int(header['PI CAMERA SHUTTERTIMING DELAYRESOLUTION'])/1000
        cadence = 5 #cadence is kept five sec for HC
        date_obs_time_cadence = date_obs_time + datetime.timedelta(seconds=cadence)

    #   Convert back to string format
        date_obs_str_cadence = date_obs_time_cadence.strftime('%Y-%m-%dT%H:%M:%S')

    #   Update header with new DATE-OBS value
        header['DATE-OBS'] = date_obs_str_cadence

        fitsfile=f'S-{header["DATE-OBS"]}-HA.fits'
        fitsname = fitsfile
        params={'rootfolder': '/data/solar_data/processed/'}
        if Path(params["rootfolder"]).exists():
    #   if params['rootfolder'] is None:
            dcf = fitsname.split('-')
            dcf_date = dcf[3].split('T')[0]
            date_obs = datetime.datetime.strptime(date_only, '%Y-%m-%d')
            #currentfolder=f'{params["rootfolder"]}{params["destfolder"]}{dcf[1]}/{dcf[1]}{dcf[2]}{dcf_date}/'
            currentfolder=f'{params["rootfolder"]}{dcf[1]}/{date_obs.strftime("%b").capitalize()}/{dcf[1]}{dcf[2]}{dcf_date}/'
            if not Path(currentfolder).exists():
                Path(currentfolder).mkdir(parents=True,exist_ok=True)
            # return f'{currentfolder}{fitsname}'
            fits.writeto(os.path.join(currentfolder, fitsfile),data_slice,header,overwrite=True)

# def fits_to_fits(parent_folder):
sub_folder = 'LC/'
# fits_name = '2022 June 02 09_44_28 10.fits'
fits_pattern = '*.fits'
# folder_path_s = os.path.join(parent_folder,fits_name)
folder_path_s = os.path.join(parent_folder,sub_folder,fits_pattern)
fits_files =  glob.glob(folder_path_s)

# open the fits data cube
# loop through each fits files
for fits_file in fits_files:
    # open the fita data cube
    data_cube = fits.open(fits_file)
    header =  data_cube[0].header

# Loop through each slice of the data cube and save it as a separate fits file
    for i, data_slice in enumerate(data_cube[0].data, start=1):
        # Get the header for this slice from the data cube
        header = data_cube[0].header
    #   Convert the header DATE-OBS value to datetime object
        date_obs_str = header['DATE-OBS']
        date_obs_time = datetime.datetime.strptime(date_obs_str, '%Y-%m-%dT%H:%M:%S')

    #   Add cadence to datetime object
    #   cadence = int(header['PI CAMERA SHUTTERTIMING DELAYRESOLUTION'])/1000
        cadence =  30 #ensure to keep cadence of 30 sec for Low cadence data
        date_obs_time_cadence = date_obs_time + datetime.timedelta(seconds=cadence)

    #   Convert back to string format
        date_obs_str_cadence = date_obs_time_cadence.strftime('%Y-%m-%dT%H:%M:%S')

    #   Update header with new DATE-OBS value
        header['DATE-OBS'] = date_obs_str_cadence

        fitsfile=f'S-{header["DATE-OBS"]}-HA.fits'
        fitsname = fitsfile
        params={'rootfolder': '/data/solar_data/processed/'}
        if Path(params["rootfolder"]).exists():
    # if params['rootfolder'] is None:
            dcf = fitsname.split('-')
            dcf_date = dcf[3].split('T')[0]
            date_obs = datetime.datetime.strptime(date_only, '%Y-%m-%d')
        #   currentfolder=f'{params["rootfolder"]}{params["destfolder"]}{dcf[1]}/{dcf[1]}{dcf[2]}{dcf_date}/'
            currentfolder=f'{params["rootfolder"]}{dcf[1]}/{date_obs.strftime("%b").capitalize()}/{dcf[1]}{dcf[2]}{dcf_date}/'
            if not Path(currentfolder).exists():
                 Path(currentfolder).mkdir(parents=True,exist_ok=True)
         # return f'{currentfolder}{fitsname}'
            fits.writeto(os.path.join(currentfolder, fitsfile),data_slice,header,overwrite=True)
