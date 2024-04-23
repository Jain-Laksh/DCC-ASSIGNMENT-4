import fitz
import pandas as pd

def convert_pdf_to_dataframe(pdf):

    pg_no = 1
    for page in pdf:
        table=page.find_tables()
        tab = table[0]
        if pg_no==1:
            df = tab.to_pandas()
        else:
            df_temp = tab.to_pandas()
            df = pd.concat([df,df_temp])
        pg_no += 1

    print('Conversion of pdf to dataframe successful!')
    return df
  
print('CONVERSION OF PDF TO CSV PROGRAM SUCCESSFULLY STARTED!')

pdf1 = fitz.open('Bonds encashed by political parties.pdf')
pdf2 = fitz.open('Bonds purchased by Individuals and Companies.pdf')

pdf1_df = convert_pdf_to_dataframe(pdf1)
pdf2_df = convert_pdf_to_dataframe(pdf2)


pdf1_df.rename(columns = {'''Date of
Encashment''':'Date_of_Encashment','''Bond
Number''':'Bond_Number','Pay Branch Code':'Pay_Branch_Code','Pay Teller':'Pay_Teller'}, inplace = True) 
print('Renaming of columns in pdf1 successful!')

pdf2_df.rename(columns = {'Reference No (URN)':'Reference_No_(URN)','Journal Date':'Journal_Date','''Date of
Purchase''':'Date_of_Purchase','Date of Expiry':'Date_of_Expiry','Name of the Purchaser':'Name_of_the_Purchaser','''Bond
Number''':'Bond_Number','Issue Branch Code':'Issue_Branch_Code','tIssue Tellerest':'Issue_Teller'}, inplace = True)
print('Renaming of columns in pdf2 successful!')

pdf1_df.to_csv('Bonds encashed by political parties.csv', index=False)
print('PDF successfully converted to CSV!')
pdf2_df.to_csv('Bonds purchased by Individuals and Companies.csv', index=False)
print('PDF successfully converted to CSV!')