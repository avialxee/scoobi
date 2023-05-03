# scoobi
Solar Conventionality-based Organizing Observation data ( SCOOBI )

```bash
usage: scoobi [-h] [-f FITS_FOLDER] [-t TIFF_FOLDER] [-o OUTPUT_FILE] [-c CONFIG_FILE] [-hdr HEADER] [-hf HEADER_FILE]
              [-hfo HEADER_FILE_OUTPUT] [-mm MONTH] [-dd DAYS] [--no-datedfolder] [-rt] [-ct] [-rc] [-cc] [-do] [-th]

Solar Conventionality-based Organizing Observation data ( SCOOBI )

optional arguments:
  -h, --help            show this help message and exit
  -f FITS_FOLDER, --fits_folder FITS_FOLDER
                        source
  -t TIFF_FOLDER, --tiff_folder TIFF_FOLDER
                        tiff folder path
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        complete path for output csv or log file.
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        complete path for config file with inputs
  -mm MONTH, --month MONTH
                        comma separated month names
  -dd DAYS, --days DAYS
                        comma separated month names for range(a,b) Ex --days='1,32'
  --no-datedfolder      if not needed to create dated folder
  -rt, --read-time      reads time from a tiff file
  -ct, --compare-time   compares time from a fits file to a tiff file
  -rc, --read-config    read config, bool
  -cc, --create-config  create config, if called with rc would modify from and to the CONFIG_FILE path
  -do, --do-conversion  create fits from tiff file and take care of the folder structure. Requires tiff_folder path
  -th, --thumbnail      True/False for creating thumbnails; The fits folder path is required but should be more specific
                        e.g atleaset including the /processed; should not be used with -do

header:
  Parameters for injecting and printing headers.
  [[Work in Progress]]

  -hdr HEADER, --header HEADER
                        Comma separated input headers to inject to the raw file.
  -hf HEADER_FILE, --header-file HEADER_FILE
                        Input header from path to inject to the raw file.
  -hfo HEADER_FILE_OUTPUT, --header-file-output HEADER_FILE_OUTPUT
                        Header output with the correct padding.
```

# File Conventions


## ORGANIZED FOLDER 

> Front-end Processed data for access through database

### Folder structure

- solar_data
    - final
        > contains fits files and thumbnails
        - YEAR (int[4])
          - MONTH (int[2])
             - DAY (int[2])
                - .fits file
                - thumbnails/
                    - .fits file path.stem + 'jpg'
        
    - processed
        > contains fits files
        - YEAR (int[4])
           - MONTH (int[2])
             - DAY (int[2])
                - .fits file
                    
    - raw
        > raw telescope data
      - YEAR (int[4])
          - Month (int[2])
              - Day (int[2])


### Naming Convention suggested by committee

*S + DATETIME + TELESCOPE*

*Example : S-2022-11-01T02:02:20.001-HA.fits*



- S : Science data
- F : Flats data
- D : Dark data
- '-' : Separator
- 2022-11-01 : YEAR + Separator + MONTH + Separator + DAY
- T02:02:20.001 : T + hour + minute +seconds +millisecond
- HA : H- alpha telescope
