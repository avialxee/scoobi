# scoobi
Solar Conventionality-based Organizing Observation data ( SCOOBI )



# File Conventions


## ORGANIZED FOLDER 

> Front-end Processed data for access through database

### Folder structure
- archived_data_solar
    - final_data
        > contains thumbnails
        
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