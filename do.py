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
import datetime


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
def search_file(path='', file_format='.tif', recursive=False, dontknowfoldername=False):
    if dontknowfoldername:
        files=glob(f'{path}*/**/*{file_format}',recursive=True)
    else:
        files=glob(f'{path}**/*{file_format}',recursive=recursive)
    return files

# Process
def header_dictfromtiff(tiffile):
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

def header_dictforfits(fitsfile, **kwargs):
    header_params={
        

    }
    header_params.update(kwargs)
    with fits.open(fitsfile, 'update') as f:
        for hdu in f:
            hdu.header.update(header_params)
            hdu.header['FILENAME'] = tifpath.name

def tif_to_fits(tiffile, magick=True, fitsfile=None, header=None, **kwargs):
    tifpath = Path(tiffile)
    if header is None:
        header=header_dictfromtiff(tiffile)
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

def build_foldername(cfitsname, archived_data_solar_path='/home/avi/archived_data_solar/', final=False):
    """
    Ex S-2022-11-01T02:02:20.001-HA.fits
    """
    if Path(archived_data_solar_path).exists():
        dcf=cfitsname.split('-')
        if final:
            destfolder='final_data/'
        else:
            destfolder='processed_data/'
        currentfolder=Path(f'{archived_data_solar_path}{destfolder}{dcf[1]}/{dcf[1]}{dcf[2]}{dcf[3]}/')
        if not currentfolder.exists():
            currentfolder.mkdir(parents=True,exist_ok=True)
        return currentfolder
            


        
    else:
        raise Exception('Please check folder path "{archived_data_solar_path}"')

def tif2fits_bulk(tiffolderlist):
    if isinstance(tiffolderlist,list):
        for tifffolder in tiffolderlist:
            listtiff=search_file(tifffolder,'.tif', recursive=True)
            print(f'total files: {len(listtiff)}')
    else:
        raise Exception(f'Is "{tiffolderlist}" a list?')
        # print(read_tif(listfile[0]))
        # for f in listfile:
        #     print(f)
        #     tif_to_fits(f)

def compare_datetime(**kwargs):
    params={
        'source_folder':'/home/avi/archived_data_solar/processed_data/2012/', 
        'csv_file':'/home/avi/archived_data_solar/raw_data/archival_data_codes/scooby_logs/2012all_compare_datetime.csv',
        'tiff_folder':'/home/avi/archived_data_solar/raw_data/SOLAR_DATA_2012/', 
        'month':['Jan','Feb','Mar', 'Apr','May', 'June','July','Aug','Sept','Oct','Nov','Dec'], 
        'days':range(1,32)
    }
    params.update(kwargs)
    
    sfolder=None
    month_dict=['Jan','Feb','Mar', 'Apr','May', 'June','July','Aug','Sept','Oct','Nov','Dec']
    allmonthfolders=glob(f"{params['source_folder']}*")

    for m in params['month']:
        for mm in allmonthfolders: 
                if m in mm:
                    sfolder=f'{mm}'
        
        for day in params['days']:
            
            d_str=str(day).zfill(2)
        
            list_fitsfile=search_file(f'{sfolder}/{d_str}/', '.fits', True)
            tlist_fitsfile=len(list_fitsfile)
            
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
                datedfolder=str(int(dm[2][:2]))+str(month_dict[int(dm[1])-1])
                list_tiffile=search_file(f'{params["tiff_folder"]}{m}/{datedfolder}',fl, recursive=True,dontknowfoldername=True)
                ltf_datetime_found,ltf_found='NA',f'missing /{datedfolder.lower()}' # init with NA if missing

                if not len(list_tiffile):
                    list_tiffile=search_file(f'{params["tiff_folder"]}{m.upper()}/{datedfolder}',fl, recursive=True,dontknowfoldername=True)
                if not len(list_tiffile):
                    list_tiffile=search_file(f'{params["tiff_folder"]}{m.upper()}/{datedfolder.lower()}',fl, recursive=True,dontknowfoldername=True)
                
                
                for ltf in list_tiffile:
                    if f'/{datedfolder.lower()}' in ltf.lower():
                        # try:
                        #     ltf_datetime=str(Time.strptime(str(read_tif(ltf)['Image DateTime'].values),'%m/%d/%Y %I:%M:%S.%f %p',scale='utc', format='fits'))
                        # except:
                        try:
                            ltf_datetime=str(read_tif(ltf)['Image DateTime'].values)
                        except:
                            ltf_datetime='NA'
                        ltf_datetime_found,ltf_found=ltf_datetime,ltf
                csv_data.append([Path(fitsfile).name,d,fl,ltf_datetime_found,ltf_found])
                
            tcsv_data=len(csv_data)
            if tcsv_data:
                with open(params['csv_file'], 'a') as cfile:
                    cw=csv.writer(cfile)
                    cw.writerows(csv_data)
                    # print(f"ww={tcsv_data}/tt={tlist_fitsfile}")
                    
def _create_folder():
    pass
print(tif2fits_bulk(['/home/avi/archived_data_solar/raw_data/SOLAR_DATA_2012/APR/']))