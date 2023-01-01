#! /home/avi/Solar_Data/Raw/archival_data_codes/env/py310/bin/python3.10
# Solar Conventionality-based Organizing Observation data ( SCOOBI )

import exifread, subprocess, argparse
from glob import glob
from pathlib import Path
from astropy.io import fits
from astropy.time import Time
import astropy.units as u
from collections import defaultdict
import csv

class SCOOBI():
    def __init__():
        pass

# Helper
def read_tif(tiffile):
    with open(tiffile, 'rb') as f:
        tags=exifread.process_file(f)
    return (tags)

def logger():
    pass

# Folder Structure
def search_file(path='', file_format='.tif', recursive=False):
    files=glob(f'{path}**/*{file_format}',recursive=recursive)
    return files

# Process
def header_dict(tiffile):
    """
    create dict from tiffile metadata read by exifread
    *adds some headers automatically from ImageDescription
    """
    tags=read_tif(tiffile)
    header=defaultdict(list)

    t=Time.strptime(str(tags['Image DateTime'].values),'%m/%d/%Y %I:%M:%S.%f %p',scale='utc', format='fits')
    header['DATE-OBS']=t.value
    desclist = tags['Image ImageDescription'].values.split('\r\n')

    expdef=Time.strptime('00:00:00.000', '%H:%M:%S.%f')
    for desc in desclist:
        if 'Exposure' in desc:
            d=desc.split(':',1)
            exposure=Time.strptime(str(d[1])[2:-5].replace(' ',''),'%H:%M:%S.%f')
            exptime=exposure-expdef
    header['EXPTIME']=round(float(exptime.sec),1)
    return header

def tif_to_fits(tiffile, magick=True, fitsfile=None, header=None, **kwargs):
    tifpath = Path(tiffile)
    if header is None:
        header=header_dict(tiffile)
    if 'telescope' in kwargs: 
        telescope=kwargs['telescope']
    else:
        telescope='HA'
    if not fitsfile:
        # name convention : *S + DATETIME + TELESCOPE*
        fitsfile=f'S-{header["DATE-OBS"].replace("-","_")}-{telescope}.fits'

    if magick:
        print(tiffile)
        subprocess.run(['convert', str(tiffile), fitsfile])
        print(f'created {fitsfile}')
    else:
        pass
    with fits.open(fitsfile, 'update') as f:
        for hdu in f:
            hdu.header.update(header)
            hdu.header['FILENAME'] = tifpath.name
            hdu.header['HISTORY']=f'{tiffile}'
            hdu.header['HISTORY']=f'scooby.py'

# listfile=search_file('/home/avi/archived_data_solar/raw_data/SOLAR_DATA_2012/APR/','fm01360.tif', recursive=True)
# print(f'total files: {len(listfile)}', listfile)
# print(read_tif(listfile[0]))
# for f in listfile:
#     print(f)
#     tif_to_fits(f)

def compare_datetime(searchfolder='/home/avi/archived_data_solar/processed_data/2012/', logfolder='/home/avi/archived_data_solar/raw_data/archival_data_codes/scooby_logs/',
tiffolder='/home/avi/archived_data_solar/raw_data/SOLAR_DATA_2012/'):
    
    # month folder to search in raw_data
    month=['Jan','Feb','Mar', 'Apr','May', 'June','July','Aug','Sep','Oct','Nov','Dec']
    allmonthfolders=glob(f'{searchfolder}*')
    for m in month:
        
        for day in range(1,31):
            i=0
            sfolder=None
            d_str=str(day).zfill(2)
            for mm in allmonthfolders: 
                if m in mm:
                    sfolder=f'{mm}/{d_str}/'
        
            list_fitsfile=search_file(sfolder, '.fits', True)
            csv_data=[]
            for fitsfile in list_fitsfile:
                
                hdul=fits.open(fitsfile)
                try:
                    d=hdul[0].header['DATE-OBS']
                    fl=hdul[0].header['FILENAME']
                except KeyError:
                    d=hdul[1].header['DATE-OBS']
                    fl=hdul[1].header['FILENAME']
                
                
                # build name for dated folder in raw_data
                dm=d.split('-')    
                datedfolder=str(int(dm[2][:2]))+str(month[int(dm[1])-1])
                # csv_file=f"{logfolder}{d_str}_{str(month[int(dm[1])-1]).lower()}_2012_scoobycompare_datetime.csv"
                csv_file=f'{logfolder}2012_scoobycompare_datetime.csv'
                if m in sfolder:
                    list_tiffile=search_file(f'{tiffolder}{m.upper()}/',fl, recursive=True)
                    
                
                # assign header columns
                headerList = [sfolder, 'DATETIME_oldFITS', 'FILENAME', 'DATETIME_rawTIF', 'TIF_PATH']
                for ltf in list_tiffile:
                    if f'/{datedfolder}' in ltf:
                        ltf_datetime=str(Time.strptime(str(read_tif(ltf)['Image DateTime'].values),'%m/%d/%Y %I:%M:%S.%f %p',scale='utc', format='fits'))
                        csv_data.append([Path(fitsfile).name,d,fl,ltf_datetime,ltf])
                
                if i<10:
                    i+=1
                else:
                    break
                    
            if len(csv_data):
                with open(csv_file, 'a') as cfile:
                    dw = csv.DictWriter(cfile, delimiter=',', 
                                        fieldnames=headerList)
                    dw.writeheader()
                    cw=csv.writer(cfile)
                    cw.writerows(csv_data)
                    # print(csv_file)
def _create_folder():
    pass
