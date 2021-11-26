""" Parameters """

## Preparer
preparer = "Dillon Lucas"

## Dates
YYYY = '2021' # Valuation Year
MM   = '06' # Valuation Month
DD   = '30' # Valuation Day

## AILs
ail_fa_path = r'M:\Valuation\GAAP\202106JUN\Files from MDT\AILs\VOYA\FA\fa_day3_alfa_feed_20210630.ail2'
ail_fia_path = r'M:\Valuation\GAAP\202106JUN\Files from MDT\AILs\VOYA\FIA\v3 - Production\fia_day3_alfa_feed_20210630.ail2'

## Stat Tax Reserves Model Output
voya_stat_path = r'M:\Valuation\GAAP\202106JUN\Files from MDT\ALFA Results\VOYA\STAT\06-2021_LiabInv_Stat_EXT_VOYA_BASE_v1014.txt'


""" Execute script """

import create_davd

create_davd.create_davd(YYYY,
                        MM,
                        DD,
                        ail_fa_path,
                        ail_fia_path,
                        voya_stat_path,
                        preparer)
        
