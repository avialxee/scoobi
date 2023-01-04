# scoobi
Solar Conventionality-based Organizing Observation data ( SCOOBI )

```bash
usage: scoobi [-h] [-s SOURCE_FOLDER] [-t TIFF_FOLDER] [-o OUTPUT_FILE] [-c CONFIG_FILE] [-mm MONTH] [-dd DAYS] [-rt] [-ct] [-rc] [-cc]

Solar Conventionality-based Organizing Observation data ( SCOOBI )

options:
  -h, --help            show this help message and exit
  -s SOURCE_FOLDER, --source_folder SOURCE_FOLDER
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
  -rt, --read-time      reads time from a tiff file
  -ct, --compare-time   compares time from a fits file to a tiff file
  -rc, --read-config    read config, bool
  -cc, --create-config  create config, bool, if called with rc would modify from and to the CONFIG_FILE path
```

# File Conventions


## ORGANIZED FOLDER 

> Front-end Processed data for access through database

### Folder structure
- archived_data_solar
    - final_data
        > contains thumbnails
        - YEAR (int[4])
            - DATE (int[6]) \
                *ex: 20221231*
                - .fits file
                - thumbnails/
                    - .fits file path.stem + 'jpg'
        
    - processed_data 
        > contains thumbnails
        - YEAR (int[4])
            - DATE (int[6]) \
                *ex: 20221231*
                - .fits file
                - thumbnails/
                    - .fits file path.stem + 'jpg'
    - raw_data

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