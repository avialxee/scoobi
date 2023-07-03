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
hc_initial='S'
hc_cadence='5'

lc=f'LC/'                                               # low cadence files
lc_initial='S'
lc_cadence='30'

dark=f'DARK/'                                           # DARK frame files
dark_initial='D'
dark_cadence='1'

flat=f'FLAT/'                                           # FLAT frame files
flat_initial='F'
flat_cadence='1'

corrupted_folder='corrupt/'                   # The folder name for corrupted raw files inside the current directory of processed fits file when conversion fails.

# SETTINGS --------------------------------------------------------
usemagick=True
uselogging=False
logfile='scoobi.logs'
logfolder='.'

# HEADER DEFAULT --------------------------------------------------
telescope_name='HA'

# -----------------------------------------------------------------
config = {key: value for key, value in locals().items() if not key.startswith('__')}
