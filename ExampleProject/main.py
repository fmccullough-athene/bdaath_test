#  This Example script reads a valuation date from the local.conf configuration file.  It then uses that date to retrieve 10 columns of data for 
#  cedent AEL.   That information is then output to an Excel file - example_output.xlsx.

import pyodbc
import pandas as pd
import configparser as cfg


#  python methods called from the main code

def load_config():
    global Config
    '''
    Load the config files here:
    '''
    Config = cfg.ConfigParser()

    Config.read(r'.\\local.conf')
 
    return Config

def get_sql_table(valuation_date):

    val_date = valuation_date

    conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ATHPRODBIDB01;'
                              'Database=AHLDW;'
                              'Trusted_Connection=yes;')

    query = "select top 10 ClientShortName, NewOrSurviving, ValuationDate, Entity, ProductType, ProductName, PolicyNumber, ModelPlan, PlanCode, PolicyCount, AccountValueTotal from AHLDW.rpt.AILPlus where ClientShortName='AEL' \
and ValuationDate=\'" + val_date  + "\'" + " and NewOrSurviving='_\'" + " and ActualOrEstimate = 'A\'"

    print("SQL query: ", query)

    data_frame = pd.read_sql_query(str(query), conn)
        
    return data_frame
	
	
def write_excel_file(output_file_path, output_data_frame):

    Excelwriter = pd.ExcelWriter(output_file_path, engine="xlsxwriter")
    output_data_frame.to_excel(Excelwriter, sheet_name="Output" ,index=True)
    Excelwriter.close()

    return


'''
This section is the main method that calls the defined methods above
'''
#Load values from your config.

print("Load Configuration")

Config = load_config()

valuation_date = Config['Settings']['valuation_date']

print("Valuation date from config file: ", valuation_date)
df = get_sql_table(valuation_date)

print(df)
print("Writing to Excel example_output.xlsx")

write_excel_file(".\output\example_output.xlsx", df)

