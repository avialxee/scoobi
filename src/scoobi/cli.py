import argparse
from scoobi import compare_datetime, read_tif, Time, tif2fits_bulk, tif_to_fits, compare_datetime_nofolder, thumb_gen,fits2fits_bulk,fits_to_fits
from collections import defaultdict
from pathlib import Path

def read_configfile(filepath):
    with open(filepath,'r') as f:
        params = defaultdict(list)
        pr=f.read().splitlines()
        for i in range(len(pr)):
            if '#' in pr[i]:
                continue
            elif '=' in pr[i]:
                k,v=pr[i].split('=')
                if 'month' in k:
                    params[k]=v.split(',')
                elif 'days' in k:
                    dd=v.split(',')
                    params[k]=range(int(dd[0]),int(dd[1])) 
                else:
                    params[k]=v
    return params

def default_params():
    return {'fits_folder':'/data/solar_data/processed', 
        'csv_file':'/data/solar_data/raw/log.csv',
        'tiff_folder':'/data/solar_data/raw/',
        'raw_folder':'/data/solar_data/raw/', 
        'month':'Jan,Feb,Mar,Apr,May,June,July,Aug,Sept,Oct,Nov,Dec', 
        'days':'1,32'}

def create_config(params, out='.config'):
    with open(out, 'w') as o:
        for k,v in params.items():
            if isinstance(v,list) : 
                o.write(f'{k}={",".join(v)}\n')
            elif isinstance(v, range):
                o.write(f'{k}={v.start},{v.stop}\n')
            else:
                o.write(f'{k}={v}\n')
    return f'configfile:{out}'

parser = argparse.ArgumentParser('scoobi',description="""
Solar Conventionality-based Organizing Observation data ( SCOOBI )""", formatter_class=argparse.RawDescriptionHelpFormatter)

# pa = parser.add_subparsers(help='compare datetimes') # subparser is used like $pip "install"

parser.add_argument('-f','--fits_folder', help='source') #positionals
parser.add_argument('-t','--tiff_folder', help='RAW TIFF folder path')
parser.add_argument('-r','--raw_folder', help='RAW FITS folder path')
parser.add_argument('-o','--output_file', help='complete path for output csv or log file.')
parser.add_argument('-c','--config_file', help='complete path for config file with inputs', default='.config')
# parser.add_argument('-hdr','--header', help='Input header to inject to the FITS file.')

headers=parser.add_argument_group('header', """Parameters for injecting and printing headers.
[[Work in Progress]]""")
headers.add_argument('-hdr','--header', type=str, help="Comma separated input headers to inject to the raw file.", required=False)
headers.add_argument('-hf', '--header-file', type=str, help="Input header from path to inject to the raw file.", required=False)
headers.add_argument('-hfo', '--header-file-output', type=str, help="Header output with the correct padding.", required=False)

parser.add_argument('-mm', '--month', type=str, help="""comma separated month names""")
parser.add_argument('-dd', '--days', type=str, default='1,32', help="""comma separated month names for range(a,b) 
Ex --days='1,32'""")

parser.add_argument('--no-datedfolder', action='store_true', dest='no_datedfolder',help='if not needed to create dated folder') 
parser.add_argument('-rt','--read-time', action='store_true', dest='rt',help='reads time from a tiff file') 
parser.add_argument('-ct','--compare-time', action='store_true', dest='ct',help='compares time from a fits file to a tiff file') 
parser.add_argument('-rc','--read-config',action='store_true',dest='rc', help=" read config, bool")
parser.add_argument('-cc','--create-config',action='store_true',dest='cc', help=" create config, if called with rc would modify from and to the CONFIG_FILE path")
parser.add_argument('-do','--do-conversion',action='store_true',dest='do', help=" create fits from tiff/fits raw file and take care of the folder structure. Requires tiff_folder or raw_folder path")
parser.add_argument('-th','--thumbnail', action='store_true', dest='th',help='True/False for creating thumbnails; The fits folder path is required but should be more specific e.g atleaset including the /processed; should not be used with -do')

args=parser.parse_args()
def cli():
    params=default_params()
    header = defaultdict(list)
    if args.fits_folder: params['fits_folder']=args.fits_folder
    if args.output_file: params['csv_file']=args.output_file
    if args.tiff_folder: params['tiff_folder']=args.tiff_folder
    if args.raw_folder: params['raw_folder']=args.raw_folder
    if args.header_file_output: print(args.header_file_output)
    if args.header: 
        hdrin=str(args.header).replace(' ','')
        hdrdict=hdrin.split(',')
        for i in range(len(hdrdict)):
            if '=' in hdrdict[i]:
                hdrk,hdrv=hdrdict[i].split('=')
                try:
                    hdrv=int(hdrv)
                except:
                    try:
                        hdrv=float(hdrv)
                    except:
                        hdrv=str(hdrv).strip()
                header[hdrk]=hdrv  
        print(header)

    mm=args.month or params['month']
    dd=args.days #already has default values
    configfile=args.config_file or '.config'

    if dd: dd=str(dd).split(',')
    if mm: params['month']=mm.split(',')
    params['days']=range(int(dd[0]),int(dd[1]))    
    params={k: v for k, v in params.items() if v is not None}
    if Path(configfile).exists() and args.rc: params.update(read_configfile(configfile))

    if args.ct and not args.no_datedfolder: compare_datetime(**params)
    if args.no_datedfolder and args.ct: compare_datetime_nofolder(**params)
    if args.rc: print(read_configfile(configfile))
    if args.cc: print(create_config(params,configfile))
    if args.rt: print(str(read_tif(params['tiff_folder'])['Image DateTime'].values))
    if args.do: 
        if args.tiff_folder:
            if '.tif' not in params['tiff_folder']: 
                print(tif2fits_bulk(params['tiff_folder'].split(','), destfolder=params['fits_folder']))
            else:
                print(tif_to_fits(params['tiff_folder'], destfolder=params['fits_folder']))
        if args.raw_folder:
            if not any(fts in params['raw_folder'] for fts in ['.fits', '.fts']): 
                print(fits2fits_bulk(params['raw_folder'].split(','), destfolder=params['fits_folder']))
            else:
                print(fits_to_fits(params['raw_folder'], destfolder=params['fits_folder']))
    if args.th: thumb_gen(params['fits_folder'])
        
if __name__=='__main__':
    cli()
