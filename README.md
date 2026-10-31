# ev-market-explorer

# Data Sources:

## Data file 1: Electric Vehicle Title and Registration Activity

URL
````https://data.wa.gov/d/rpr4-cgyd````

````
Columns:
    "Clean Alternative Fuel Vehicle Type"
    ,"VIN (1-10)"
    ,"DOL Vehicle ID"
    ,"Model Year"
    ,"Make"
    ,"Model"
    ,"Primary Use"
    ,"Electric Range"
    ,"Odometer Reading"
    ,"Odometer Reading Description"
    ,"New or Used Vehicle"
    ,"Sale Price"
    ,"Sale Date"
    ,"Transaction Type"
    ,"Transaction Date"
    ,"Year"
    ,"County"
    ,"City"
    ,"State"
    ,"Postal Code"
    ,"2019 HB 2042: Clean Alternative Fuel Vehicle (CAFV) Eligibility"
    ,"Meets 2019 HB 2042 Electric Range Requirement"
    ,"Meets 2019 HB 2042 Sale Date Requirement"
    ,"Meets 2019 HB 2042 Sale Price/Value Requirement"
    ,"2019 HB 2042: Battery Range Requirement"
    ,"2019 HB 2042: Purchase Date Requirement"
    ,"2019 HB 2042: Sale Price/Value Requirement"
    ,"Electric Vehicle Fee Paid"
    ,"Transportation Electrification Fee Paid"
    ,"Hybrid Vehicle Electrification Fee Paid"
    ,"2020 GEOID"
    ,"Legislative District"
    ,"Electric Utility"
````

## Data file 2: Zip to lat and long data :

Source: US Census

URL: ````https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2026_Gazetteer/2026_Gaz_zcta_national.zip````

Columns: GEOID|GEOIDFQ|ALAND|AWATER|ALAND_SQMI|AWATER_SQMI|INTPTLAT|INTPTLONG
GEOID = ZipCode
INTPTLAT - Latitude
INTPTLONG - Longitude
Column Separator: Tab



