import pandas as pd
import pyodbc

class example_class(object):
    '''
    This is a template class. Group similar methods together in a class for easier organization
    '''
    def example_method():

        print ("I am example_method from class example_class.")
        
        '''
        A method should
        '''
        return
    
    def second_example_method(parameter):

        print ("I am second_example_method from class example_class.")
        
        '''
        A method should
        '''
        return parameter

    def get_sql_table(valuation_date):

        val_date = valuation_date

        conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=ATHPRODBIDB01;'
                          'Database=AHLDW;'
                          'Trusted_Connection=yes;')

        query = "select top 50 ClientShortName, NewOrSurviving, ValuationDate, Entity, ProductType, ProductName, PolicyNumber, ModelPlan, \
PlanCode, PolicyCount, AccountValueTotal from AHLDW.rpt.AILPlus where ClientShortName='AEL' \
and ValuationDate=\'" + val_date  + "\'" + " and NewOrSurviving='_\'" + " and ActualOrEstimate = 'A\'"
			
        data_frame = pd.read_sql_query(str(query), conn)
        
        return data_frame
	
	
    def write_excel_file(output_file_path, output_data_frame):

        Excelwriter = pd.ExcelWriter(output_file_path, engine="xlsxwriter")
        output_data_frame.to_excel(Excelwriter, sheet_name="Output" ,index=True)
        Excelwriter.close()

        return

    def open_csv_file(connection_string):
    
        data_frame = pd.read_csv( connection_string)

        return data_frame