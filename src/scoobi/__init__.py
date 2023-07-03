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
import shutil
from scoobi.config import usemagick, thumbnails, thumbnails_root, rootfolder
from scoobi.config import  dark,dark_cadence,dark_initial,flat,flat_cadence,flat_initial,hc,hc_cadence,hc_initial,lc,lc_cadence,lc_initial


class SCOOBI():
    def __init__():
        pass

# Helper
def read_tif(tiffile):
    with open(tiffile, 'rb') as f:
        tags=exifread.process_file(f)
    return (tags)

def _vitals_check():
    """
    Check if magick is installed or not. Returns 0 if exists else non-zero int.
    """
    a=subprocess.call('magick -version',shell=True, stdout=subprocess.DEVNULL)
    return {'magick':a}

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
    header['EXPTIME']=(round(float(exptime.sec),1), 'Exposure time in unit second')
    return header

def header_dictforfits(fitsfile, **kwargs):
    header_params={
        

    }
    header_params.update(kwargs)
    with fits.open(fitsfile, 'update') as f:
        for hdu in f:
            hdu.header.update(header_params)
            hdu.header['FILENAME'] = tifpath.name

def build_foldername(filename,createdir=True, **kwargs):
    """
    Builds folder name taking input of the fitsfile name i.e
    destfolder + 

    *Parameters*
    
    :filename: 
        (str) (Required)

        This is the conventional name of the fitsfile which will be used to build the folder path.
        Ex. S-2022-11-01T02:02:20.001-HA.fits

    :destfolder: 
        (str) (Optional) (Default:'')

        The destination folder name where all the files will get saved.

    *Return*
    
        (str) complete path for the file.

    """
    params={'destfolder': '',
    }
    params.update(kwargs)
    if not params['destfolder']: params['destfolder']=f"{params['fits_folder']}"
    dbf=filename.split('-') # date-wise build foldername
    dbf_date=dbf[3].split('T')[0]
    # YEAR[int4]/MONTH[str3]/yyyymmdd/S-yyyy-mm-ddTtime.fits
    mm_str=datetime.datetime.strptime(dbf[2],"%m").strftime("%b").capitalize()
    builtfolder=f'{params["destfolder"]}{dbf[1]}/{mm_str}/{dbf[1]}{dbf[2]}{dbf_date}/'
    if not Path(builtfolder).exists() and createdir:
        Path(builtfolder).mkdir(parents=True,exist_ok=True)
    return f'{builtfolder}{filename}'
        
def fits_to_fits(fitsfile_i, header=None, **kwargs):
    """
    *Parameters*
    
    :fitsfile_i:
        (str) (Required)

        Full path of the RAW FITS file as input. This is a 3D FITS file.

    :header:
        (dict) (Optional)

        If provided, it will use headers from FITS as well the supplied parameters to write to FITS.
    
    *kwargs*

    :fitsname: 
        (str) (Optional) (Default=None)

        This is the conventional name of the fitsfile which will be used to build the folder path.
        If not provided will build name according to the timestamp in the FITS header.
        Ex. S-2022-11-01T02:02:20.001-HA.fits
    
    :initial:
        (str) (Optional) (Default='S')
        Convential initial for the type of file in the output filename e.g
        - S: Science
        - F: Flat
        - D: Dark

    :destfolder: 
        (str) (Optional) (Default:see build_foldername())

        The destination folder name where all the files will get saved.

    :telescope:
        (str) (Optional) (Default:HA)
        The Telescope name is used to create the header info and filename
    """
    if header:
        pass
    params={'fitsname':None, 'telescope':'HA', 'initial':'S'}
    params.update(kwargs)
    fitsfile_o=None
    def __writefilefromhdul(hdul,date):
        """
        internal function to read hdul and date to fill headers and generate fitsfile name creating directory where necessary.
        """
        date=date.strftime('%Y-%m-%dT%H:%M:%S.%f')
        for hdu in hdul:
            hdu.header.update(header)
            hdu.header['TELESCOP']=params['telescope']
            hdu.header['FILENAME']=Path(fitsfile_i).name
            
        if params['fitsname'] is None:
            # name convention : *S + DATETIME + TELESCOPE*
            print('building foldername:')

            fitsfile_o=f"{params['initial']}-{date}-{params['telescope']}.fits"
            fitsfile_o=build_foldername(fitsfile_o, **kwargs)
        else:
            fitsfile_o=build_foldername(params['fitsname'])
        hdul.writeto(fitsfile_o, overwrite=True)
        return fitsfile_o
    
    with fits.open(fitsfile_i, 'readonly',) as hdul:
        date=hdul[0].header['DATE-OBS']
        date=datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%S.%f')
        cadence=0
        if dark in fitsfile_i:
            params['initial']=dark_initial
            cadence=dark_cadence
        elif flat in fitsfile_i:
            params['initial']=flat_initial
            cadence=flat_cadence
        elif hc in fitsfile_i:
            params['initial']=hc_initial
            cadence=hc_cadence
        elif lc in fitsfile_i:
            params['initial']=lc_initial
            cadence=lc_cadence
            

        if len(hdul[0].data.shape)==3:                                  # checks if data is cube
            for i, hdul_slice in enumerate(hdul[0].data):
                td=datetime.timedelta(seconds=cadence*i)
                date=date+td
                fitsfile_o=__writefilefromhdul(hdul_slice,date)
        else:
            fitsfile_o=__writefilefromhdul(hdul,date)
    return fitsfile_o
    
def tif_to_fits(tiffile, magick=usemagick, header=None, **kwargs):
    """
    *Parameters*
    
    :tiffile:
        (str) (Required)

        Full path of the TIFF file that needs to be converted to FITS.

    :magick:
        (boolean) (Optional)

        If true will execute convert utility of ImageMagick to convert from tiff to fits (faster)
        Else the python way of conversion will be used.

    :header:
        (dict) (Optional)

        If provided, it will use headers from TIFF as well the supplied parameters to write to FITS.
    
    :telescope:
        (str) (Optional) (Default:HA)
        The Telescope name is used to create the header info and filename

    kwargs
    ------

    :fitsname: 
        (str) (Optional) (Default=None)

        This is the conventional name of the fitsfile which will be used to build the folder path.
        If not provided will build name according to the timestamp in the TIFF header.
        Ex. S-2022-11-01T02:02:20.001-HA.fits

    :destfolder: 
        (str) (Optional) (Default:None)

        The destination folder name where all the files will get saved.
    """
    params={'fitsname':None, 'telescope':'HA'}
    params.update(kwargs)
    tifpath = Path(tiffile)
    if header is None:
        header=header_dictfromtiff(tiffile)
    else:
        header.update(header_dictfromtiff(tiffile))
    if params['fitsname'] is None:
        # name convention : *S + DATETIME + TELESCOPE*
        fitsfile=f'S-{header["DATE-OBS"]}-{params["telescope"]}.fits'
        fitsfile=build_foldername(fitsfile, **kwargs)
    
    if magick:
        #print(tiffile)
        subprocess.run(['convert', str(tiffile), fitsfile])
        print(f'created {fitsfile}')
    else:
        pass
    with fits.open(fitsfile, 'update') as f:
        for hdu in f:
            fitspath = Path(fitsfile)
            hdu.header.update(header)
            hdu.header['TELESCOP']=params['telescope']
            hdu.header['FILENAME']=fitspath.name
            hdu.header['HISTORY']=f'{tiffile}'
            hdu.header['HISTORY']=f'scoobi'

def thumbgen(fitsfile, out_folder=None, thumb_folder=thumbnails, force=False):
    """
    Creates thumbnails for the fits file provided in the fits_folder path.
    depends on build_foldername 
    else if thumb_folder is specified with out_folder jpgfile is created accordingly.
    ex. out_folder,thumb_foler='/data/solardata/','Thumbnails/'

    """
    if fitsfile:        
        jpgfile_name=f"{Path(fitsfile).stem}.jpg"
        if out_folder is None:out_folder=Path(fitsfile).parent
        jpgfile=f'{out_folder}/{thumb_folder}/{jpgfile_name}'
        if not Path(jpgfile).exists(): Path(jpgfile).parent.mkdir(parents=True,exist_ok=True)
        if not Path(jpgfile).exists() or force: subprocess.run(["convert", fitsfile,"-linear-stretch","1x1","-resize", "56%", jpgfile ])
        return jpgfile

def thumbgen_bulk(fits_folder, thumb_folder=thumbnails, thumb_root=thumbnails_root, force=False, **kwargs):
    """
    calls thumb_gen for converting fits to jpg and then copies to a directory specified by :thumb_root:
    """
    
    allfile=search_file(f"{fits_folder}/",'.fits', recursive=True)
    for fitsfile in allfile:
        jpgfile=thumbgen(fitsfile,thumb_folder=thumb_folder,force=force)

        outfolder_root=build_foldername(Path(fitsfile).name,createdir=False, destfolder='/')
        jpgfile_root=f"{thumb_root}/{Path(outfolder_root).parent}/{Path(jpgfile).name}"
        
        if not Path(jpgfile_root).exists() or force: 
            Path(jpgfile_root).parent.mkdir(parents=True,exist_ok=True)
            shutil.copy(str(jpgfile), str(jpgfile_root))

            
def fits2fits_bulk(fitsfolderlist, **kwargs):
    """
    takes input as list of string fits folder paths and executes fits_to_fits() using for loop to each folder path.
    see *fits_to_fits()* for the list of parameters.
    If fits to fits conversion fails, the file is saved in "corrupt/" (can be changed from call) folder at the tiff source folder.
    """
    params={'failed_folder':'corrupt/'}
    params.update(kwargs)
        
    if isinstance(fitsfolderlist,list):
        for fitsfolder in fitsfolderlist:
            listfits=search_file(fitsfolder,'.fits', recursive=True)
            for f in listfits:
                if not 'corrupt' in f:
                    params['failed_folder']=f"{Path(f).parent}/corrupt/"
                    try:
                        fits_to_fits(f, **kwargs)
                    except Exception as e:
                        try:
                            # if Path(f).stat().st_size <= desiredsize:
                            print(e)
                            Path(params['failed_folder']).mkdir(parents=True,exist_ok=True)
                            shutil.copy(str(f), str(f"{params['failed_folder']}/{Path(f).name}"))
                        except:
                            with open('failed.scoobi','+a') as sf:
                                sf.write(f"{f}\n")
    else:
        raise Exception(f'Is "{fitsfolderlist}" a list?')           

def tif2fits_bulk(tiffolderlist, **kwargs):
    """
    takes input as list of string tiff folder paths and executes tif to fits using for loop to each folder path.
    see *tif_to_fits()* for the list of parameters.
    If tif to fits conversion fails, the file is saved in "corrupt/" (can be changed from call) folder at the tiff source folder.
    """
    params={'failed_folder':'corrupt/'}
    params.update(kwargs)
        
    if isinstance(tiffolderlist,list):
        for tifffolder in tiffolderlist:
            listtiff=search_file(tifffolder,'.tif', recursive=True)
            for f in listtiff:
                if not 'corrupt' in f:
                    params['failed_folder']=f"{Path(f).parent}/corrupt/"
                    try:
                        tif_to_fits(f, **kwargs)
                    except:
                        try:
                            # if Path(f).stat().st_size <= desiredsize:
                            Path(params['failed_folder']).mkdir(parents=True,exist_ok=True)
                            shutil.copy(str(f), str(f"{params['failed_folder']}/{Path(f).name}"))
                        except:
                            with open('failed.scoobi','+a') as sf:
                                sf.write(f"{f}\n")
    else:
        raise Exception(f'Is "{tiffolderlist}" a list?')
        
#log generation
def compare_datetime(**kwargs):
    params={
        'fits_folder':'/data/solar_data/processed/', 
        'csv_file':'/data/solar_data/processed/scooby_logs/compare_datetime.csv',
        'tiff_folder':'/data/solar_data/raw/SOLAR_DATA_2012/', 
        'month':['Jan','Feb','Mar', 'Apr','May', 'June','July','Aug','Sept','Oct','Nov','Dec'], 
        'days':range(1,32)
    }
    params.update(kwargs)
    
    sfolder=None
    month_dict=['Jan','Feb','Mar', 'Apr','May', 'June','July','Aug','Sept','Oct','Nov','Dec']
    allmonthfolders=glob(f"{params['fits_folder']}*")

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

def compare_datetime_nofolder(**kwargs):
    params={
        'fits_folder':'/data/solar_data/processed/', 
        'csv_file':'/data/solar_data/processed/scooby_logs/compare_datetime.csv',
        'tiff_folder':'/data/solar_data/raw/SOLAR_DATA_2012/',  
        
    }
    params.update(kwargs)
    
    list_fitsfile=search_file(f'{params["fits_folder"]}/', '.fits', True)
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
        
        list_tiffile=search_file(f'{params["tiff_folder"]}',fl, recursive=True,dontknowfoldername=True)
        ltf_datetime_found,ltf_found='NA',f'missing /{fl}' # init with NA if missing

        if not len(list_tiffile):
            list_tiffile=search_file(f'{params["tiff_folder"]}',fl, recursive=True,dontknowfoldername=False)
        
        for ltf in list_tiffile:
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
