## Import Libraries
import pandas as pd
import numpy as np
import datetime as dt

def create_davd(YYYY,
                MM,
                DD,
                ail_fa_path,
                ail_fia_path,
                voya_stat_path,
                preparer):
    
    ## Declare list of AIL fields to import
    ail_fields = ['//ck.Plan',
                  'ck.IssAge',
                  'ck.Gender',
                  'ck.IssYear',
                  'ck.IssMon',
                  'PolNo',
                  'Company',
                  'LegalEntity',
                  'DBRiderCodeYN',
                  'RiderCodeYN',
                  'ReportingGroup',
                  'CohortKey',
                  'GroupIndiv',
                  'IssueDate',
                  'LiquidityRider',
                  'NHRElected',
                  'AdminSystem',
                  'ICOSFlag',
                  'QualStatus',
                  'State',
                  'AccumPrem',
                  'AccumPW',
                  'AVIF',
                  'IncRiderAV',
                  'InitGuarCSVwoBAV',
                  'PremiumInforce',
                  'SCPeriod',
                  'Segment',
                  'SNFLVal',
                  'MVAapply',
                  'MortalityTable',
                  'GMWBCharge',
                  'GMWBIncType',
                  'GMWBParRate',
                  'GMWBPayment',
                  'GenAV',
                  'iCurr',
                  'iGuar']
    
    ## Declare list of AIL field data types
    ail_field_dtypes = {'//ck.Plan': str,
                        'ck.IssAge': int,
                        'ck.Gender': str,
                        'ck.IssYear': int,
                        'ck.IssMon': int,
                        'PolNo': str,
                        'Company': str,
                        'LegalEntity': str,
                        'DBRiderCodeYN': str,
                        'RiderCodeYN': str,
                        'ReportingGroup': str,
                        'CohortKey': str,
                        'GroupIndiv': str,
                        'IssueDate': str,
                        'LiquidityRider': str,
                        'NHRElected': str,
                        'AdminSystem': str,
                        'ICOSFlag': str,
                        'QualStatus': str,
                        'State': str,
                        'AccumPrem': float,
                        'AccumPW': float,
                        'AVIF': float,
                        'IncRiderAV': float,
                        'InitGuarCSVwoBAV': float,
                        'PremiumInforce': float,
                        'SCPeriod': int,
                        'Segment': str,
                        'SNFLVal': float,
                        'MVAapply': str,
                        'MortalityTable': str,
                        'GMWBCharge': float,
                        'GMWBIncType': str,
                        'GMWBParRate': float,
                        'GMWBPayment': float,
                        'GenAV': float,
                        'iCurr': float,
                        'iGuar': float}
    
    ## Declare list of Stat result fields to import
    stat_fields = ['ckPlan',
                   'policynumber',
                   'CASHVALUE',
                   'STATRESERVE',
                   'IntCredOpt',
                   'MinIntCredAmt',
                   'WPA1',
                   'WPA2',
                   'Winning_Duration',
                   'DE_WPA1',
                   'DE_WPA2',
                   'DE_Winning_Duration',
                   'DE_STATRESERVE']
    
    ## Declare list of Stat result field data types
    stat_field_dtypes = {'ckPlan': str,
                         'PolicyNumber': str,
                         'CashValue': float,
                         'StatReserve': float,
                         'IntCredOpt': float,
                         'MinIntCredAmt': float,
                         'WPA1': str,
                         'WPA2': str,
                         'Winning_Duration': int,
                         'DE_WPA1': str,
                         'DE_WPA2': str,
                         'DE_Winning_Duration': int,
                         'DE_StatReserve': float}
    
    ## Read AILs
    ail_fa = pd.read_csv(ail_fa_path,
                         sep = '\t', 
                         usecols = ail_fields, 
                         dtype = ail_field_dtypes)
    
    ail_fia = pd.read_csv(ail_fia_path,
                          sep = '\t',
                          usecols = ail_fields,
                          dtype = ail_field_dtypes)
    
    ## Combine two AILs
    ail_total = ail_fa.append(ail_fia)
    
    ## Change column names
    ail_total.columns = ['Plan', # changed
                         'IssueAge', # changed
                         'Sex', # changed
                         'IssueYear', # changed
                         'IssMon', # changed
                         'PolicyNumber', # changed
                         'SourceFile', # changed
                         'LegalEntity',
                         'DBYN', # changed
                         'IRYN', # changed
                         'ReportingGroup',
                         'CohortKey',
                         'GroupIndiv',
                         'IssueDate',
                         'LiquidityRiderYN', # changed
                         'EnhancementStatus', # changed
                         'AdminSystem',
                         'ICOSFlag',
                         'QualCodeQN', # changed
                         'State',
                         'AccumPrem',
                         'AccumPW',
                         'AccountValue', # changed
                         'IncomeAV', # changed
                         'CashValue_AIL', # changed
                         'PremiumInforce',
                         'SCPeriod',
                         'Segment',
                         'SNFLValue', # changed
                         'MVAYN', # changed
                         'MortalityTable',
                         'GMWBCharge',
                         'GMWBIncType',
                         'GMWBParRate',
                         'GMWBPayment',
                         'GenAV',
                         'CurrInt', # changed
                         'GuarInt'] # changed
    
    ## Add columns
    ail_total['SourceFile'] = 'VOYA'
    ail_total['ROPInd'] = np.where(ail_total['LiquidityRiderYN'] == 'ROPN', 'Y', 'N')
    
    ## Edit columns
    ail_total['IssueDate'] = pd.to_datetime(ail_total['IssueDate'].astype(str), format = '%Y%m%d')
    ail_total['LiquidityRiderYN'] = np.where(ail_total['LiquidityRiderYN'] == 'Non', 'N', 'Y') # need review
    ail_total.loc[ail_total['MVAYN'] == 'Yes', 'MVAYN'] = 'Y'
    ail_total.loc[ail_total['MVAYN'] == 'No', 'MVAYN'] = 'N'
    ail_total.loc[ail_total['GMWBPayment'] == 0, 'GMWBIncType'] = ''
    
    ## Add Stat and Tax Reserves
    voya_stat = pd.read_csv(voya_stat_path,
                            sep = '\t',
                            usecols = stat_fields,
                            dtype = stat_field_dtypes)
    
    voya_stat['TaxReserve_Final'] = .9281 * voya_stat['DE_STATRESERVE']
    voya_stat['TaxReserve_Final'] = voya_stat[['TaxReserve_Final', 'CASHVALUE']].max(axis = 1)
    voya_stat = voya_stat[voya_stat['ckPlan'] != 'FHOD']
    
    ## Change column names
    voya_stat.columns = ['ckPlan',
                         'PolicyNumber', # changed
                         'CashValue', # changed
                         'StatReserve', # changed
                         'IntCredOpt',
                         'MinIntCredAmt',
                         'WPA1',
                         'WPA2',
                         'Winning_Duration',
                         'DE_WPA1',
                         'DE_WPA2',
                         'DE_Winning_Duration',
                         'DE_StatReserve', # changed
                         'TaxReserve_Final']
    
    ## Change policy numbers to capital letters
    ail_total['PolicyNumber'] = ail_total['PolicyNumber'].str.upper()
    voya_stat['PolicyNumber'] = voya_stat['PolicyNumber'].str.upper()
    
    ## Check if there are any duplicates
    if not ail_total['PolicyNumber'].is_unique:
        print('There are duplicates in AILs!')
    if not voya_stat['PolicyNumber'].is_unique:
        print('There are duplicates in ALFA results!')
    
    
    ## Merge AILs and ALFA results by PolicyNumber
    davd = pd.merge(ail_total, voya_stat, how = 'inner', on = 'PolicyNumber')
    check_alfa = ail_total[~ail_total['PolicyNumber'].isin(davd['PolicyNumber'])] # policies only in AILs
    check_ail = voya_stat[~voya_stat['PolicyNumber'].isin(davd['PolicyNumber'])] # policies only in ALFA results
    print('Number of policies only in AILs: ' + str(len(check_alfa)))
    print('Number of policies only in ALFA results: ' + str(len(check_ail)))
    
    ## Misc Fields
    davd['PolicyCount'] = 1
    
    davd.loc[davd['LegalEntity'] == 'RLI', 'LegalEntity'] = 'RLIC'
    davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] == 'RLI_TDA_NoIR_AR'), 'LegalEntity'] = 'RLIC'
    davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] != 'VIAC_SA'), 'ALRE_WPA1'] = davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] != 'VIAC_SA'), 'WPA1']
    davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] != 'VIAC_SA'), 'ALRE_WPA2'] = davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] != 'VIAC_SA'), 'WPA2']
    davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] != 'VIAC_SA'), 'ALRE_Winning_Duration'] = davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] != 'VIAC_SA'), 'Winning_Duration']
    davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] == 'VIAC_SA'), 'ALRE_WPA1'] = davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] == 'VIAC_SA'), 'DE_WPA1']
    davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] == 'VIAC_SA'), 'ALRE_WPA2'] = davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] == 'VIAC_SA'), 'DE_WPA2']
    davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] == 'VIAC_SA'), 'ALRE_Winning_Duration'] = davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] == 'VIAC_SA'), 'DE_Winning_Duration']
    davd.loc[davd['LegalEntity'] == 'RLIC', 'ALRE_WPA1'] = davd.loc[davd['LegalEntity'] == 'RLIC', 'DE_WPA1']
    davd.loc[davd['LegalEntity'] == 'RLIC', 'ALRE_WPA2'] = davd.loc[davd['LegalEntity'] == 'RLIC', 'DE_WPA2']
    davd.loc[davd['LegalEntity'] == 'RLIC', 'ALRE_Winning_Duration'] = davd.loc[davd['LegalEntity'] == 'RLIC', 'DE_Winning_Duration']
    
    ## Adjust for Reins pct
    davd['STAT_Reserve_IAPP'] = davd['StatReserve']
    davd['STAT_Reserve_No_IAPP'] = davd['DE_StatReserve']
    davd['VOYA_StatReserve'] = davd['STAT_Reserve_No_IAPP']
    davd['VOYA_TaxReserve'] = davd['TaxReserve_Final']
    davd['VOYA_CashValue'] = davd['CashValue']
    davd['VOYA_AccountValue'] = davd['AccountValue']
    
    davd['AADE_StatReserve'] = davd['STAT_Reserve_No_IAPP'] * .2
    davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] != 'VIAC_SA'), 'ALRE_StatReserve'] = davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] != 'VIAC_SA'), 'STAT_Reserve_IAPP'] * .8
    davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] == 'VIAC_SA'), 'ALRE_StatReserve'] = davd.loc[(davd['LegalEntity'] == 'VIAC') & (davd['ReportingGroup'] == 'VIAC_SA'), 'STAT_Reserve_No_IAPP'] * .8
    davd.loc[davd['LegalEntity'] == 'RLIC', 'ALRE_StatReserve'] = davd.loc[davd['LegalEntity'] == 'RLIC', 'STAT_Reserve_No_IAPP']
    davd.loc[davd['LegalEntity'] == 'RLIC', 'AADE_StatReserve'] = 0
    
    davd['ALRE_TaxReserve'] = davd['TaxReserve_Final'] * .8
    davd.loc[davd['LegalEntity'] == 'RLIC', 'ALRE_TaxReserve'] = davd.loc[davd['LegalEntity'] == 'RLIC', 'TaxReserve_Final']
    
    davd['AADE_TaxReserve'] = davd['TaxReserve_Final'] * .2
    davd.loc[davd['LegalEntity'] == 'RLIC', 'AADE_TaxReserve'] = 0
    
    davd['AADE_CashValue'] = davd['CashValue'] * .2
    davd.loc[davd['LegalEntity'] == 'RLIC', 'AADE_CashValue'] = 0
    
    davd['ALRE_CashValue'] = davd['CashValue'] * .8
    davd.loc[davd['LegalEntity'] == 'RLIC', 'ALRE_CashValue'] = davd.loc[davd['LegalEntity'] == 'RLIC', 'CashValue']
    
    davd['AADE_AccountValue'] = davd['AccountValue'] * .2
    davd.loc[davd['LegalEntity'] == 'RLIC', 'AADE_AccountValue'] = 0
    
    davd['ALRE_AccountValue'] = davd['AccountValue'] * .8
    davd.loc[davd['LegalEntity'] == 'RLIC', 'ALRE_AccountValue'] = davd.loc[davd['LegalEntity'] == 'RLIC', 'AccountValue']
    
    ## Export AVD
    davd = davd.sort_values(['SourceFile', 'PolicyNumber'])
    davd['Preparer'] = preparer + " " + str(dt.datetime.now())
    davd.to_csv('DAVD ' + YYYY + MM + DD + '.csv', index = False)
    
    
    davd_summary = davd.pivot_table(index = ['LegalEntity', 'SourceFile', 'ReportingGroup', 'CohortKey', 'GroupIndiv'], aggfunc = sum)
    davd_summary['Preparer'] = preparer + " " + str(dt.datetime.now())
    
    ## To match the format
    davd_summary['VOYA_ICOS'] = ''
    davd_summary['ALRE_ICOS'] = ''
    davd_summary['AADE_ICOS'] = ''
    davd_summary = davd_summary[['PolicyCount',
                                 'AccountValue',
                                 'VOYA_AccountValue',
                                 'AADE_AccountValue',
                                 'ALRE_AccountValue',
                                 'STAT_Reserve_No_IAPP',
                                 'STAT_Reserve_IAPP',
                                 'VOYA_StatReserve',
                                 'ALRE_StatReserve',
                                 'AADE_StatReserve',
                                 'TaxReserve_Final',
                                 'VOYA_TaxReserve',
                                 'ALRE_TaxReserve',
                                 'AADE_TaxReserve',
                                 'VOYA_ICOS',
                                 'ALRE_ICOS',
                                 'AADE_ICOS',
                                 'CashValue',
                                 'VOYA_CashValue',
                                 'AADE_CashValue',
                                 'ALRE_CashValue',
                                 'Preparer']]
    
    davd_summary.to_csv('DAVD Summary ' + YYYY + MM + DD + '.csv')
    
    ## For risk reporting purpose
    # davd.loc[davd['Plan'] == 'SLCTR2', 'ReportingGroup'] = davd.loc[davd['Plan'] == 'SLCTR2', 'ReportingGroup'].str.replace('FIA', 'FSD')
    # davd.loc[davd['Plan'] == 'SLCTRA', 'ReportingGroup'] = davd.loc[davd['Plan'] == 'SLCTRA', 'ReportingGroup'].str.replace('FIA', 'FSD')
    # davd.loc[davd['Plan'] == 'SLCTR2', 'CohortKey'] = davd.loc[davd['Plan'] == 'SLCTR2', 'CohortKey'].str.replace('FIA', 'FSD')
    # davd.loc[davd['Plan'] == 'SLCTRA', 'CohortKey'] = davd.loc[davd['Plan'] == 'SLCTRA', 'CohortKey'].str.replace('FIA', 'FSD')
    # davd_risk_summary
    
    print('## End of DAVD Reconciliation ##')

