import argparse
from do import compare_datetime, read_tif, Time
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
    return {'source_folder':'/home/avi/archived_data_solar/processed_data/2012/', 
        'csv_file':'/home/avi/archived_data_solar/raw_data/archival_data_codes/scooby_logs/2012all_compare_datetime.csv',
        'tiff_folder':'/home/avi/archived_data_solar/raw_data/SOLAR_DATA_2012/', 
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

parser.add_argument('-s','--source_folder', help='source') #positionals
parser.add_argument('-t','--tiff_folder', help='tiff folder path')
parser.add_argument('-o','--output_file', help='complete path for output csv or log file.')
parser.add_argument('-c','--config_file', help='complete path for config file with inputs', default='.config')

parser.add_argument('-mm', '--month', type=str, help="""comma separated month names""")
parser.add_argument('-dd', '--days', type=str, default='1,32', help="""comma separated month names for range(a,b) 
Ex --days='1,32'""")

parser.add_argument('-rt','--read-time', action='store_true', dest='rt',help='reads time from a tiff file') 
parser.add_argument('-ct','--compare-time', action='store_true', dest='ct',help='compares time from a fits file to a tiff file') 
parser.add_argument('-rc','--read-config',action='store_true',dest='rc')
parser.add_argument('-cc','--create-config',action='store_true',dest='cc')

args=parser.parse_args()
def cli():
    params=default_params()
    
    if args.source_folder: params['source_folder']=args.source_folder
    if args.output_file: params['csv_file']=args.output_file
    if args.tiff_folder: params['tiff_folder']=args.tiff_folder

    mm=args.month or params['month']
    dd=args.days #already has default values
    configfile=args.config_file or '.config'

    if dd: dd=str(dd).split(',')
    if mm: params['month']=mm.split(',')
    params['days']=range(int(dd[0]),int(dd[1]))    
    params={k: v for k, v in params.items() if v is not None}
    if Path(configfile).exists() and args.rc: params.update(read_configfile(configfile))

    if args.ct: compare_datetime(**params)
    if args.rc: print(read_configfile(configfile))
    if args.cc: print(create_config(params,configfile))
    if args.rt: print(str(read_tif(params['tiff_folder'])['Image DateTime'].values))
    
if __name__=='__main__':
    cli()