from pathlib import Path
pwd=Path().absolute()

# This is a default configuration value file, 
# Where you can hardcode the following variables


# INPUTS ---------------------------------------------------------
rootfolder='/data/solar_data/'
processed='processed/'
thumbnails='Thumbnails/'

processedfolder=f'{rootfolder}{processed}'
thumbnails_root=f'{rootfolder}{thumbnails}'       # Thumbnails in the root folder has all thumbnails from processed fits folder


rawfolder=f'{rootfolder}raw/'                           # Parent RAW Folder
hc=f'HC/'                                               # high cadence files
lc=f'LC/'                                               # low cadence files
darks=f'DARK/'                                          # DARK frame files
flat=f'FLAT/'                                           # FLAT frame files

corrupted_folder='corrupt/'                   # The folder name for corrupted raw files inside the current directory of processed fits file when conversion fails.

# SETTINGS --------------------------------------------------------
usemagick=True
uselogging=False
logfile='scoobi.logs'
logfolder=pwd

# HEADER DEFAULT --------------------------------------------------
telescope_name='HA'

# -----------------------------------------------------------------