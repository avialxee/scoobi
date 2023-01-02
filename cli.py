import argparse
from do import compare_datetime

parser = argparse.ArgumentParser('scoobi',description="""
Solar Conventionality-based Organizing Observation data ( SCOOBI )""", formatter_class=argparse.RawDescriptionHelpFormatter)

# cd = parser.add_mutually_exclusive_group(required=True)
# cd.add_argument('-sf', '--searchfolder', help='sfolder path')
# cd.add_argument('-lf','--logfolder', help='helpfolder path')
# cd.add_argument('-tf','--tiffolder', help='tiffolder path')

# cd2 = parser.add_mutually_exclusive_group(required=True)
# cd2.add_argument('-cd2', '--searchfolder2', help='sfolder path')

cd0 = parser.add_subparsers(help='compare datetimes')
cd1 = cd0.add_parser( 'c',help='compare datetime')
sf = cd1.add_argument('sfolder', help='sfolder path')
lf = cd1.add_argument('logfolder', help='helpfolder path')
tf = cd1.add_argument('tiffolder', help='tiffolder path')


args=parser.parse_args()
def cli():
    sf=args.sfolder
    lf=args.logfolder
    tf=args.tiffolder
    print([sf,lf,tf])
    compare_datetime(sf,lf,tf)
    
if __name__=='__main__':
    cli()